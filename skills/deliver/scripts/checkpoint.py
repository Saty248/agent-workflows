#!/usr/bin/env python3
"""Record a local delivery checkpoint; host tools verify external evidence."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

TRANSITIONS = {
    "awaiting_approval": set(),
    "implementing": {"validating"},
    "validating": {"implementing", "documenting"},
    "documenting": {"implementing", "reviewing"},
    "reviewing": {"implementing", "publishing"},
    "publishing": {"implementing", "watching"},
    "watching": {"implementing", "reviewing", "ready"},
    "ready": {"implementing", "reviewing", "watching"},
}


def nonblank(value):
    if not value.strip():
        raise argparse.ArgumentTypeError("A nonempty value is required")
    return value


def plan_text(state):
    value = Path(state["plan"]).read_bytes()
    if not value.strip():
        raise ValueError("The plan must be nonempty")
    return value


def digest(value):
    return hashlib.sha256(value).hexdigest()


def git(project, *args):
    return subprocess.run(["git", "-C", str(project), *args], check=True,
                          text=True, capture_output=True).stdout.strip()


def atomic_write(path, text):
    fd, temp = tempfile.mkstemp(prefix=".checkpoint-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


@contextmanager
def locked(directory):
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(directory, 0o700)
    fd = os.open(directory / ".lock", os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, "w") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def require_current_approval(state):
    if not state.get("approval"):
        raise ValueError("Actual user approval must be recorded first")
    if digest(plan_text(state)) != state["plan_sha256"]:
        raise ValueError("Plan changed; record an amendment or obtain renewed approval")


def event(state, action, evidence=""):
    state["history"].append({
        "at": datetime.now(timezone.utc).isoformat(),
        "action": action, "phase": state["phase"], "evidence": evidence,
    })


def run(args, project, directory):
    path = directory / "checkpoint.json"
    if args.command == "init":
        if path.exists():
            raise ValueError("Checkpoint exists; use status or resume")
        state = {"version": 1, "project": str(project), "task": args.task,
                 "plan": str(args.plan.expanduser().resolve()),
                 "thread_ref": args.thread_ref, "phase": "awaiting_approval",
                 "approval": None, "history": [], "pr": None, "head": None}
        state["plan_sha256"] = digest(plan_text(state))
    else:
        state = json.loads(path.read_text())
        if state["project"] != str(project) or state["task"] != args.task:
            raise ValueError("Checkpoint identity mismatch")
    if args.command == "status":
        state["plan_matches"] = digest(plan_text(state)) == state["plan_sha256"]
        return state
    if args.command == "approve":
        if state["phase"] != "awaiting_approval":
            raise ValueError("Approval must refer to a plan awaiting approval")
        text = plan_text(state)
        state["plan_sha256"] = digest(text)
        state["approval"] = {"user_ref": args.user_ref,
                             "plan_sha256": state["plan_sha256"]}
        atomic_write(directory / "approved-plan.md", text.decode("utf-8"))
        state["phase"] = "implementing"
    elif args.command == "amend":
        if args.within_scope:
            if not state.get("approval"):
                raise ValueError("A scoped amendment requires prior approval")
            state["phase"] = "implementing"
        else:
            state["approval"] = None
            state["phase"] = "awaiting_approval"
        state["plan_sha256"] = digest(plan_text(state))
        state["head"] = None
        state.pop("last_evidence", None)
        state.pop("resume_phase", None)
    elif args.command == "phase":
        require_current_approval(state)
        if args.name not in TRANSITIONS.get(state["phase"], set()):
            raise ValueError("Invalid phase transition: " + state["phase"] + " -> " + args.name)
        if args.name in {"watching", "ready"}:
            if not args.evidence or not args.head:
                raise ValueError("Watching/ready require evidence and a full current head SHA")
            if not re.fullmatch(r"[a-f0-9]{40}|[a-f0-9]{64}", args.head):
                raise ValueError("Use a full head SHA")
            if args.head != git(project, "rev-parse", "HEAD"):
                raise ValueError("Recorded head does not match the current checkout")
            pr = args.pr or state.get("pr")
            if not pr or not re.fullmatch(r"https://[^/\s\\]+/[^/\s\\]+/[^/\s\\]+/pull/[1-9][0-9]*", pr):
                raise ValueError("A full HTTPS PR URL is required")
            state["head"], state["pr"] = args.head, pr
        if args.name == "implementing":
            state["head"] = None
            state.pop("last_evidence", None)
        state["phase"] = args.name
        if args.evidence:
            state["last_evidence"] = args.evidence
    elif args.command == "block":
        if state["phase"] != "blocked":
            state["resume_phase"] = state["phase"]
        state["phase"] = "blocked"
    elif args.command == "resume":
        if state["phase"] != "blocked":
            raise ValueError("Only a blocked checkpoint needs resume")
        previous = state["resume_phase"]
        if previous != "awaiting_approval":
            require_current_approval(state)
        state["phase"] = state.pop("resume_phase")
    evidence = getattr(args, "reason", "") or getattr(args, "evidence", "")
    if args.command == "approve":
        evidence = args.user_ref
    event(state, args.command, evidence)
    atomic_write(path, json.dumps(state, indent=2) + "\n")
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--task", required=True)
    parser.add_argument("--state-root", type=Path,
                        default=Path(os.environ.get("XDG_STATE_HOME",
                                                    str(Path.home() / ".local/state"))) / "agent-workflows")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("path")
    init = commands.add_parser("init")
    init.add_argument("--plan", type=Path, required=True)
    init.add_argument("--thread-ref", type=nonblank, required=True)
    approve = commands.add_parser("approve")
    approve.add_argument("--user-ref", type=nonblank, required=True)
    amend = commands.add_parser("amend")
    amend.add_argument("--reason", type=nonblank, required=True)
    amend.add_argument("--within-scope", action="store_true")
    phase = commands.add_parser("phase")
    phase.add_argument("name", choices=sorted(set(TRANSITIONS) - {"awaiting_approval"}))
    phase.add_argument("--evidence", type=nonblank)
    phase.add_argument("--head")
    phase.add_argument("--pr")
    block = commands.add_parser("block")
    block.add_argument("--reason", type=nonblank, required=True)
    commands.add_parser("resume")
    commands.add_parser("status")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.task) or len(args.task) > 64:
        parser.error("Task must be a lowercase slug of at most 64 characters")
    try:
        project = Path(git(args.project.expanduser().resolve(), "rev-parse", "--show-toplevel")).resolve()
        directory = args.state_root.expanduser().resolve() / digest(str(project).encode())[:16] / args.task
        if args.command == "path":
            print(directory)
            return
        with locked(directory):
            result = run(args, project, directory)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
