---
name: test
description: "Design, add, and run focused tests that prove requested behavior and protect against regressions. Use for new functionality, bug fixes, refactors, or when current coverage is insufficient."
---

# Test

Create useful tests, not merely more tests.

The goal is to prove contracts, important edge cases, and regressions at the cheapest reliable test level.

## Testing principles

- Test observable behavior rather than implementation details.
- Prefer the lowest test level that can reliably prove the behavior.
- Reuse existing test conventions and helpers.
- Do not over-mock the unit under test.
- Avoid brittle assertions on incidental details.
- Every bug fix should have a regression test when practical.
- Do not change production behavior merely to satisfy a poorly designed test.
- Avoid snapshot tests when explicit assertions communicate behavior better.

## Ordered workflow

### 1. Read acceptance criteria

Translate each relevant acceptance criterion into one or more test cases.

### 2. Inspect existing test architecture

Identify:
- framework
- directory convention
- fixtures
- factories
- database setup
- API test helpers
- mocking conventions
- async helpers
- browser/E2E framework
- CI execution

### 3. Build a test matrix

For the target behavior include, where relevant:

#### Happy path
Normal expected operation.

#### Validation
Missing, malformed, boundary, and invalid inputs.

#### Authorization
Allowed and denied actors.

#### State transitions
Creation, update, deletion, retry, expiry, cancellation.

#### Persistence
Data written/read correctly.

#### Idempotency
Repeated request/event does not create unintended duplicates.

#### Concurrency
Relevant races or simultaneous updates.

#### External dependency failure
Timeout, error, malformed response, unavailable service.

#### Regression
Exact scenario that previously failed.

#### Compatibility
Existing consumers/behaviors remain intact.

### 4. Choose the right test level

Use:

**Unit tests**
for deterministic business logic with narrow dependencies.

**Integration tests**
for database, queue, cache, framework wiring, or service boundaries.

**Contract tests**
for stable interfaces between independently changing components.

**E2E tests**
for critical user journeys spanning the system.

Do not test the same behavior at every level without a clear reason.

### 5. Implement tests in priority order

Recommended order:
1. regression case
2. core happy path
3. important errors
4. permissions
5. boundaries/edge cases
6. less likely cases

### 6. Keep test setup explicit

Avoid excessive hidden magic.

A reader should understand:
- starting state
- action
- expected outcome

Use Arrange, Act, Assert conceptually even if the project uses another naming style.

### 7. Run narrow tests first

Run the exact test file or suite.

Fix:
- test failures
- flaky timing
- incorrect fixtures
- missing cleanup

### 8. Run surrounding suite

Once focused tests pass, run the relevant package/module suite.

### 9. Check test quality

Confirm tests would fail if the implementation were removed or regressed.

Watch for:
- assertions that always pass
- mocks returning the exact asserted value without exercising logic
- tests that do not await async behavior
- order-dependent tests
- shared mutable fixtures
- reliance on real time without control
- external network dependencies unless intentionally integration-tested

### 10. Report coverage gaps

If an important scenario cannot reasonably be automated, state:
- scenario
- reason
- manual validation method

## Required output format

### Test strategy
What behaviors are being protected and at what levels.

### Tests added/updated
File and scenario.

### Commands run
Exact test commands and outcomes.

### Coverage of acceptance criteria
Mapped criteria to tests.

### Remaining gaps
Important untested behavior and why.
