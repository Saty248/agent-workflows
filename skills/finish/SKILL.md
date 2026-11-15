---
name: finish
description: "Perform the final pre-PR, pre-merge, or pre-release gate by reconciling scope, diff, tests, documentation, migration/deployment concerns, and repository cleanliness."
---

# Finish

Run the final engineering gate before the work is handed off, merged, or released.

This skill does not replace CI or human approval. It ensures the change is internally coherent and nothing obvious was left behind.

## Ordered workflow

### 1. Re-read acceptance criteria

Verify every criterion against the final implementation.

### 2. Review final diff

Check for:
- unrelated edits
- generated junk
- debug logs
- temporary files
- commented code
- accidental dependency changes
- accidental lockfile churn
- secrets
- hardcoded local paths

### 3. Verify validation status

Collect the final status of:
- formatting
- lint
- type checks
- unit tests
- integration tests
- E2E tests
- build
- migration checks

Never say a check passed unless it was run successfully.

### 4. Verify tests match behavior

Confirm:
- new behavior is covered
- bug fixes have regression coverage where practical
- important errors/permissions are covered
- changed tests are not merely weakening assertions

### 5. Verify data safety

If schema/data changed:
- migration is reversible or rollback impact is documented
- backfill behavior is defined
- no destructive operation is accidental
- indexes/constraints are appropriate
- deployment ordering is safe

### 6. Verify configuration

Check:
- new environment variables are documented
- `.env.example` is updated where appropriate
- defaults are safe
- secrets are not committed
- production/development behavior is intentionally different

### 7. Verify operational behavior

When relevant:
- logs are useful
- metrics exist for critical new behavior
- health checks remain valid
- retries/timeouts are bounded
- rollout steps are clear
- rollback path is understood

### 8. Verify documentation/context

If the change modifies how developers or agents should work:
- README updated
- architecture docs updated
- `AGENTS.md` updated
- Codex rules updated
- relevant skills/context synced

Use `/sync` if substantial context drift exists.

### 9. Verify repository cleanliness

Ensure:
- no unresolved conflict markers
- no temporary diagnostic files
- no accidentally modified fixtures
- no unnecessary binary artifacts
- no local-only configuration committed

### 10. Produce handoff

## Required output format

### Completion status
State whether the requested acceptance criteria are verified, partially verified, or blocked.

### Final changes
Short summary.

### Validation
Exact commands/checks and results.

### Known limitations
Anything not verified.

### Migration/deployment notes
Only if applicable.

### Documentation/context updates
What was updated or remains to be updated.

### Ready for next step
Use factual language, for example:
- ready for PR review based on executed checks
- blocked by listed issue
- ready for staging verification, with listed production checks still pending
