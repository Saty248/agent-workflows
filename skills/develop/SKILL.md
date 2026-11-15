---
name: develop
description: "Implement an approved technical plan carefully and incrementally, following the repository's existing architecture, conventions, and tests. Use after scope/design is sufficiently clear."
---

# Develop

Implement the approved change with minimal unnecessary deviation.

## Core rules

- Read relevant project instructions before editing.
- Inspect existing neighboring code before creating new patterns.
- Follow the approved scope and architecture.
- Do not silently expand scope.
- Do not rewrite unrelated code.
- Do not invent commands, dependencies, environment variables, schemas, or APIs.
- Preserve existing public behavior unless a change is explicitly required.
- Prefer small, reviewable changes.
- Keep the repository runnable throughout the work where practical.

## Ordered workflow

### 1. Load the implementation contract

Before editing, identify:
- objective
- acceptance criteria
- architecture decisions
- expected files/modules
- constraints
- non-goals
- validation steps

If a critical decision is missing, resolve it before broad implementation.

### 2. Verify repository state

Check:
- current branch/status when available
- whether relevant files have uncommitted changes
- package/tool versions
- applicable instructions
- existing tests

Never overwrite user changes.

### 3. Inspect the nearest implementation pattern

Find analogous code and mirror its:
- structure
- naming
- error handling
- dependency injection
- data access
- logging
- tests
- formatting

Prefer consistency over introducing a personal preference.

### 4. Implement foundations first

Follow dependency order.

Typical order:
1. types/interfaces
2. schema/migrations
3. repository/data layer
4. domain/service logic
5. API/event layer
6. frontend/client
7. observability
8. tests
9. docs

Adjust only when the architecture requires another order.

### 5. Keep changes cohesive

For each change:
- make one logical unit
- verify references/compile impact
- avoid unrelated cleanup
- avoid broad renames unless required

If a refactor is necessary to enable the feature, keep it narrowly scoped and explain why.

### 6. Handle errors deliberately

Do not swallow exceptions.

Follow project conventions for:
- validation errors
- domain errors
- transport errors
- external service failures
- retries
- timeouts
- logging

Avoid logging secrets, tokens, credentials, or unnecessary personal data.

### 7. Preserve compatibility

Check:
- API consumers
- event consumers
- database readers
- serialized payloads
- old application versions during rollout
- environment variables
- migration ordering

If compatibility cannot be preserved, call out the break clearly.

### 8. Add/update tests with implementation

Do not leave all tests until the end.

For each meaningful behavior:
- update an existing test if it covers the same contract
- add a focused test if behavior is new
- avoid duplicate tests with no new coverage

### 9. Run targeted validation early

After each major layer, run the narrowest relevant checks.

Examples:
- affected unit tests
- type check for package
- targeted integration test
- compile/build for touched package

Discover actual commands from the project.

### 10. Integrate end to end

Once layers are complete:
- verify data passes across boundaries
- verify errors map correctly
- verify UI/client state
- verify permissions
- verify side effects
- verify async processing where relevant

### 11. Perform implementation self-review

Inspect the diff for:
- accidental unrelated changes
- dead code
- debug logging
- TODOs
- missing null/error handling
- duplicated logic
- naming inconsistencies
- performance regressions
- security mistakes
- missing tests

### 12. Run final validation

Run applicable:
- formatter
- lint
- type check
- unit tests
- integration tests
- build
- E2E tests

If a command cannot be run, state why. Never claim a check passed if it was not executed.

## When implementation diverges from the plan

Stop and explain when:
- repository evidence contradicts the architecture
- a required dependency is unavailable
- the schema is materially different from expectations
- implementation would require a breaking change
- scope grows substantially
- there is a data-loss risk
- user-owned changes conflict with the plan

Update the design rather than improvising a hidden alternative.

## Required completion report

### Implemented
Concise summary of behavior added or changed.

### Files changed
File/module and purpose.

### Validation run
Exact checks performed and outcomes.

### Not run
Checks that could not be performed, with reason.

### Deviations
Any differences from the approved plan.

### Remaining work
Only real follow-up items, not speculative improvements.

## Handoff

After `/develop`, run:
- `/check`
- `/test` if test coverage needs expansion
- `/review`
- `/document` when docs changed
- `/finish` before merge/release
