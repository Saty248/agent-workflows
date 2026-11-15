# Local checkpoints

Run the bundled helper using its absolute skill-relative path:
`python3 <deliver-skill>/scripts/checkpoint.py --help`.

Every command takes `--project PATH --task SLUG` before its subcommand.
The default root is `$XDG_STATE_HOME/agent-workflows` or
`~/.local/state/agent-workflows`. The helper prints the checkpoint as JSON.

Examples (replace paths, slug, and user references with real values):

```bash
python3 <deliver-skill>/scripts/checkpoint.py --project /path/to/project --task retry-fix path
python3 <deliver-skill>/scripts/checkpoint.py --project /path/to/project --task retry-fix init --plan /path/to/plan.md --thread-ref current-thread-link
python3 <deliver-skill>/scripts/checkpoint.py --project /path/to/project --task retry-fix approve --user-ref approving-user-message
python3 <deliver-skill>/scripts/checkpoint.py --project /path/to/project --task retry-fix phase validating --evidence "Regression test passed"
python3 <deliver-skill>/scripts/checkpoint.py --project /path/to/project --task retry-fix status
```

Use the path command to locate a task directory for a local fallback plan.
Initialization requires an existing nonempty plan and starts awaiting_approval.
Approval stores a snapshot of the exact approved plan and the real user-message
reference. The helper cannot independently verify that reference.

After editing the plan:
- `amend --reason "..."` revokes approval and returns to awaiting_approval.
- `amend --within-scope --reason "..."` keeps the original scope approval and
  records the revision, but returns to implementing and clears old final evidence.
  Use it only for a correction already authorized by the original scope.

A changed plan is rejected by phase changes until an amendment or actual new
approval is recorded. Implementation always needs approval. Successful commands
write atomically under a local process lock. The lock serializes checkpoint
writes; it is not a cross-machine or whole-task execution lock.

Normal phases are implementing, validating, documenting, reviewing, publishing,
watching, and ready. Repair paths return to implementing. Mark blocked with
`block --reason "..."`; `resume` restores the previous phase but still checks
the plan and approval. Watching and ready require evidence and a full head SHA;
ready also requires a PR URL. The host must verify those claims against GitHub.

Checkpoint JSON and approved-plan snapshots are private local state, outside the
application and skill repositories. They contain no credentials. They are a
progress record, not a sandbox or an independently authenticated approval gate.
