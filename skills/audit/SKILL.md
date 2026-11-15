---
name: audit
description: "Build an evidence-based understanding of a repository or subsystem before making changes. Use when entering unfamiliar code, investigating architecture, preparing a substantial change, or refreshing stale project context."
---

# Audit

Understand the current system before changing it.

This skill produces a factual map of the relevant codebase, data flow, dependencies, runtime behavior, and risks. It should reduce guesswork for later architecture and implementation work.

## Core rule

**Observe first, conclude second.**

Never describe repository behavior from filenames alone. Trace actual references, call paths, configuration, tests, and runtime wiring where possible.

## Ordered workflow

### 1. Read repository instructions

Start with:
- root `AGENTS.md`
- nested `AGENTS.md` files
- applicable `.cursor/rules/*`
- README
- architecture docs
- contributor/development docs

Extract:
- required conventions
- prohibited patterns
- build/test commands
- architecture boundaries
- naming conventions
- environment expectations

### 2. Establish repository shape

Identify:
- language(s)
- framework(s)
- package manager
- workspace/monorepo structure
- primary applications/services
- shared packages/libraries
- infrastructure/deployment files
- test frameworks

Do not yet deep-read unrelated directories.

### 3. Find the target subsystem

Search from concepts in the task.

Use:
- symbols
- route names
- table/model names
- UI labels
- events/topics
- environment variables
- service names
- error messages

Build a shortlist of relevant files.

### 4. Trace entry points

Determine where execution begins.

Examples:
- HTTP route/controller
- GraphQL resolver
- websocket/SSE handler
- CLI command
- scheduled job
- queue consumer
- event listener
- UI route/page
- React/Vue component
- worker
- webhook

Record the entry point and how control flows from it.

### 5. Trace the call graph

Follow the behavior through:
- controller/handler
- validation
- service/domain logic
- repositories/data access
- integrations
- events/queues
- serializers/mappers
- response/UI state

Record important branches and side effects.

### 6. Trace data flow

For each important piece of data, identify:
- source
- transformations
- validation
- persistence
- cache behavior
- transport
- consumers
- deletion/expiry behavior

For database-backed behavior, inspect:
- schema/model
- indexes
- constraints
- migrations
- query patterns
- transaction boundaries

### 7. Inspect configuration and environment

Find relevant:
- environment variables
- feature flags
- secrets references
- ports
- URLs
- connection pools
- cache configuration
- queue configuration
- retry settings
- timeouts
- deployment-specific overrides

Do not expose secret values. Record names and purpose only.

### 8. Inspect tests

Determine:
- existing unit coverage
- integration coverage
- E2E coverage
- fixtures/factories
- mocks
- test setup
- missing important cases

Use tests as evidence of intended behavior, but verify against implementation.

### 9. Inspect observability

Look for:
- logs
- metrics
- traces
- health endpoints
- dashboards/configuration references
- error reporting
- audit logs

Record whether the target behavior is diagnosable in production.

### 10. Identify architecture boundaries

Document:
- ownership of business logic
- module boundaries
- synchronous vs asynchronous communication
- shared abstractions
- forbidden dependencies
- external systems

Call out boundary violations if they are directly observed.

### 11. Identify hotspots and risks

Check specifically for:
- duplicated business logic
- oversized modules/functions
- hidden coupling
- circular dependencies
- repeated database calls
- N+1 patterns
- unbounded queries
- synchronous blocking work
- missing pagination
- fragile retries
- no idempotency
- global mutable state
- insufficient authorization checks
- stale documentation
- configuration drift

Only report issues supported by evidence.

### 12. Produce the audit

## Required output format

### Repository/subsystem summary
What this part of the system does.

### Relevant structure
Key directories and files with responsibilities.

### Entry points
How the behavior is initiated.

### Execution flow
Ordered control flow from entry point to completion.

### Data flow
Where important data originates, moves, and persists.

### Dependencies
Internal and external dependencies.

### Configuration
Relevant configuration and environment variables.

### Tests
Existing coverage and meaningful gaps.

### Observability
How the behavior can be inspected at runtime.

### Risks/findings
Evidence-backed concerns.

### Unknowns
Anything that could not be proven from repository evidence.

### Files most likely to change
A concise shortlist, with why.

## Handoff

The audit should be usable by:
- `/scope` to refine change boundaries
- `/architect` to design the change
- `/debug` to investigate failures
- `/document` to refresh stale technical documentation
