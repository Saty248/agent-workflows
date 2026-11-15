#!/usr/bin/env python3
"""Link the workflow skills into user-level discovery directories."""
import argparse
import os
from pathlib import Path
import sys

BUNDLE = Path(__file__).resolve().parent / "skills"
DEFAULT_TARGETS = "shared,cursor,claude"


def install(home, targets, mode):
    roots = {
        "shared": home / ".agents/skills",
        "codex": Path(os.environ.get("CODEX_HOME", str(home / ".codex"))) / "skills",
        "cursor": home / ".cursor/skills",
        "claude": home / ".claude/skills",
    }
    unknown = set(targets) - roots.keys()
    if unknown:
        raise ValueError("Unknown targets: " + ", ".join(sorted(unknown)))
    sources = sorted(p for p in BUNDLE.iterdir() if p.is_dir())
    if not sources or not (BUNDLE / "deliver/SKILL.md").is_file():
        raise ValueError("Incomplete skill bundle")
    actions = []
    errors = []
    for target in dict.fromkeys(targets):
        for source in sources:
            if not (source / "SKILL.md").is_file():
                raise ValueError("Missing SKILL.md: " + str(source))
            dest = roots[target] / source.name
            owned = dest.is_symlink() and dest.resolve() == source.resolve()
            exists = dest.exists() or dest.is_symlink()
            if mode == "uninstall":
                if owned:
                    actions.append(("remove", dest, source))
                continue
            if owned:
                actions.append(("linked", dest, source))
            elif exists:
                if not (dest / "SKILL.md").is_file():
                    errors.append("Invalid existing skill: " + str(dest))
                elif source.name == "deliver":
                    errors.append("Existing deliver preserved; choose another target: " + str(dest))
                else:
                    actions.append(("preserved", dest, source))
            elif mode == "check":
                errors.append("Missing skill: " + str(dest))
            else:
                actions.append(("create", dest, source))
    if errors:
        raise ValueError("\n".join(errors))
    # Preflight every target before creating or removing any links.
    for action, dest, source in actions:
        if action == "create":
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(source, target_is_directory=True)
        elif action == "remove":
            dest.unlink()
        print(action + ": " + str(dest))
    print("Checked " + str(len(actions)) + " skill locations.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(),
                        help="Home directory to install into (also useful for a trial)")
    parser.add_argument("--targets", default=DEFAULT_TARGETS)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    targets = [v.strip() for v in args.targets.split(",") if v.strip()]
    if not targets:
        parser.error("Select at least one target")
    mode = "check" if args.check else "uninstall" if args.uninstall else "install"
    try:
        install(args.home.expanduser().resolve(), targets, mode)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
