---
name: architect
description: "Convert an approved scope and repository evidence into a concrete technical design and implementation specification. Use for non-trivial features, refactors, integrations, migrations, or changes crossing module boundaries."
---

# Architect

Design the implementation before code is changed.

This skill decides **how the requested behavior should fit into the existing system**.

## Preconditions

Before designing:
1. read applicable project instructions
2. understand the approved scope
3. inspect the relevant implementation
4. verify existing patterns
5. identify constraints

If these are missing, perform the minimum audit needed before proceeding.

## Architecture principles

- Prefer existing project patterns.
- Minimize new abstractions.
- Keep responsibilities at the correct layer.
- Avoid leaking infrastructure concerns into domain logic.
- Avoid making shared abstractions for a single speculative future use case.
- Prefer explicit contracts at system boundaries.
- Design failure behavior, not only happy paths.
- Preserve backwards compatibility unless the scope explicitly allows a break.
- Consider rollout and rollback before implementation.
- Never choose a technology simply because it is fashionable or familiar.

## Ordered workflow

### 1. Normalize the problem

State:
- current behavior
- desired behavior
- gap between them
- constraints
- non-goals

### 2. Define system boundaries

Identify which component should own:
- validation
- business rules
- persistence
- caching
- authorization
- orchestration
- external communication
- presentation

Explicitly say what should **not** own each responsibility when ambiguity exists.

### 3. Evaluate existing patterns

Find the nearest existing implementation.

Compare:
- interfaces
- naming
- folder placement
- lifecycle
- dependency direction
- error handling
- testing style

Reuse the established pattern unless there is a concrete reason not to.

### 4. Define contracts

Specify contracts before internals.

As applicable define:
- function signatures
- service interfaces
- request/response DTOs
- event payloads
- database fields
- queue messages
- websocket/SSE messages
- error types
- status codes
- permissions

For each contract define:
- inputs
- outputs
- required fields
- optional fields
- validation
- error semantics
- compatibility requirements

### 5. Design state and data

If persistent data changes are required, define:
- tables/collections
- fields
- types
- nullability
- defaults
- indexes
- unique constraints
- foreign keys
- lifecycle
- migration/backfill strategy
- rollback implications

If caching is involved, define:
- key
- value
- TTL
- invalidation
- source of truth
- stale-data behavior
- concurrency behavior

### 6. Design execution flow

Describe the end-to-end flow in order.

Include:
1. trigger
2. validation
3. authorization
4. business logic
5. reads/writes
6. external calls
7. asynchronous work
8. response/event
9. observability

Add alternate flows for major failures.

### 7. Design failure handling

For each external or fallible operation define:
- timeout
- retry behavior
- idempotency
- partial failure handling
- user-visible error
- logging
- metrics
- dead-letter behavior where applicable

Avoid unbounded retries.

### 8. Design security boundaries

Check:
- authentication
- authorization
- tenant isolation
- input validation
- secret handling
- data exposure
- logging of sensitive values
- SSRF/injection risks
- path traversal
- unsafe deserialization
- privilege escalation

Only add security mechanisms relevant to the system.

### 9. Design performance behavior

Consider:
- expected request/event volume
- database query count
- indexes
- payload size
- pagination
- batching
- caching
- concurrency
- connection use
- memory growth
- CPU-heavy work

For performance-sensitive changes, define a measurable target if one is known.

### 10. Design tests

Specify what should be covered by:
- unit tests
- integration tests
- E2E tests
- migration tests
- contract tests
- performance tests

Tie tests to acceptance criteria.

### 11. Design observability

Specify:
- useful log events
- stable fields/correlation IDs
- metrics
- alerts if applicable
- traces if applicable
- health checks

Do not log secrets or sensitive payloads unnecessarily.

### 12. Design rollout

Define:
- migration order
- deployment order
- compatibility window
- feature flag strategy if required
- backfill
- rollback
- post-deploy verification

### 13. Produce file-level implementation spec

List files to:
- add
- modify
- delete only when necessary

For every file/module describe the intended change.

Do not fabricate exact filenames if the repository evidence does not establish them. Use module/location descriptions instead.

## Required output format

### Decision summary
The core design in a few sentences.

### Existing behavior
How the system currently works.

### Proposed architecture
Responsibilities and boundaries.

### Contracts
Interfaces, payloads, APIs, or events.

### Data model
Schema/state/cache changes.

### Execution flow
Ordered happy path and important failure paths.

### Security considerations
Only relevant security impacts.

### Performance considerations
Expected impact and protections.

### Testing strategy
Required tests by level.

### Observability
Logs, metrics, traces, or health checks.

### Rollout and rollback
Safe deployment sequence.

### File-level implementation plan
Ordered list of code changes.

### Decisions and tradeoffs
Important choices and alternatives considered.

### Open decisions
Only unresolved choices that block implementation.

## Handoff

The resulting specification should be executable by `/develop` with minimal interpretation.
