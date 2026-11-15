---
name: scope
description: "Turn an idea, feature request, bug report, or vague task into a precise, ordered implementation plan before coding. Use when requirements are incomplete, broad, ambiguous, or need decomposition."
---

# Scope

Convert a request into a clear, bounded, implementation-ready plan.

This skill is for deciding **what should be done**, in what order, and how success will be measured. It is not an implementation skill.

## Primary goals

1. Understand the user's actual objective.
2. Identify the smallest correct scope.
3. Separate requirements from assumptions.
4. Discover the parts of the repository likely to be affected.
5. Identify unknowns and risks before implementation.
6. Produce an ordered plan that another agent can execute without reinterpreting the request.
7. Define explicit acceptance criteria.

## Operating rules

- Do not start implementation while using this skill unless the user explicitly asks you to continue into implementation.
- Do not invent project conventions, architecture, commands, APIs, schemas, or dependencies.
- Prefer evidence from the repository over assumptions.
- Read project instructions before planning:
  - `AGENTS.md`
  - nested `AGENTS.md` files relevant to the target area
  - applicable `.cursor/rules/*`
  - README and architecture documentation
  - package manifests and build configuration when relevant
- Reuse existing patterns unless the request specifically requires a new pattern.
- Keep the proposed change as small as possible while fully satisfying the requirement.
- Clearly distinguish:
  - confirmed facts
  - assumptions
  - open questions
  - recommendations

## Ordered workflow

### 1. Restate the objective

Rewrite the request as a concise engineering objective.

Capture:
- user-visible outcome
- business or technical intent
- affected actor or system
- expected behavior
- explicit non-goals

Do not merely repeat the prompt. Normalize it into an actionable objective.

### 2. Extract requirements

Create a requirement inventory.

Classify each requirement as:
- functional
- non-functional
- compatibility
- performance
- security
- observability
- data or migration
- UX
- deployment or operational

Mark every requirement as one of:
- confirmed
- inferred
- unknown

### 3. Inspect repository context

Locate the minimum repository context required to scope the work.

Look for:
- entry points
- existing related features
- service boundaries
- relevant models and schemas
- API routes
- frontend components
- background workers
- queues or event handlers
- tests
- migrations
- configuration
- infrastructure definitions
- documentation

Prefer targeted searches over reading the entire repository.

### 4. Map the change surface

List the likely areas affected.

For each area state:
- why it is affected
- expected type of change
- whether the change is required or conditional

Example categories:
- frontend
- backend/API
- database
- cache
- queue/eventing
- authentication/authorization
- third-party integrations
- infrastructure
- tests
- documentation

### 5. Identify dependencies and constraints

Document:
- upstream dependencies
- downstream consumers
- compatibility constraints
- current architectural conventions
- deployment dependencies
- environment/configuration requirements
- data migration requirements
- feature flag requirements
- external API limitations

Do not assume external systems behave a certain way if the repository does not establish it.

### 6. Identify risks

Explicitly check for:
- breaking API changes
- data loss
- race conditions
- concurrency issues
- duplicate processing
- backwards compatibility
- performance regressions
- N+1 queries
- unbounded reads
- missing indexes
- cache invalidation
- authorization gaps
- leaking sensitive information
- retry/idempotency problems
- rollout and rollback risk

Rank risks only as:
- high
- medium
- low

Explain the reason for each rating.

### 7. Resolve ambiguity

If a missing decision materially changes implementation, ask a focused question.

Ask only questions that block a good plan.

If a reasonable default can safely be inferred from existing project patterns, state the inference instead of interrupting the workflow.

### 8. Produce the implementation sequence

Create an ordered plan.

Each step must contain:
1. objective
2. files/modules likely involved
3. exact type of change
4. dependencies on previous steps
5. validation method

Prefer dependency order, for example:

1. data model/schema
2. domain/service logic
3. API/interface
4. frontend/client integration
5. tests
6. observability
7. documentation
8. rollout verification

Do not order by convenience if dependencies require a different sequence.

### 9. Define acceptance criteria

Write observable acceptance criteria.

Good criteria:
- describe externally verifiable behavior
- include error behavior
- include permissions where relevant
- include persistence/state behavior
- include important edge cases

Avoid vague criteria such as:
- "works correctly"
- "is performant"
- "handles errors"

### 10. Define validation

Specify how the completed work should be verified.

Include applicable:
- unit tests
- integration tests
- E2E tests
- type checks
- linting
- build
- migration validation
- manual UI verification
- logs/metrics
- load/performance checks

Never invent command names. Discover commands from project configuration.

## Required output format

### Objective
A short description of the desired end state.

### Confirmed requirements
Only requirements directly supported by the request or repository.

### Assumptions
Any safe assumptions being made.

### Open questions
Only questions that materially affect implementation.

### Change surface
Affected systems, modules, or layers.

### Risks
High, medium, and low risks with explanations.

### Ordered implementation plan
Numbered, dependency-aware implementation steps.

### Acceptance criteria
Concrete completion conditions.

### Validation plan
How the implementation will be proven correct.

### Out of scope
Anything intentionally excluded.

## Handoff

The output of `/scope` should be suitable input for `/architect`.

If architecture is already obvious and the task is small, it may be suitable input directly for `/develop`.
