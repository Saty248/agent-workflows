---
name: document
description: "Write or update accurate human-facing technical documentation from the actual repository state. Use for README updates, setup guides, architecture docs, operational runbooks, feature documentation, or developer onboarding."
---

# Document

Produce documentation that matches the code that actually exists.

## Documentation rules

- Verify facts in the repository before writing them.
- Do not document planned behavior as already implemented.
- Do not expose secrets or real credentials.
- Prefer copy-pasteable commands that actually exist in the project.
- Separate required configuration from optional configuration.
- Keep setup order executable from a clean environment.
- Match terminology used by the product/codebase.
- Avoid internal implementation detail in end-user documentation unless useful.

## Ordered workflow

### 1. Identify audience

Choose one or more:
- new developer
- existing developer
- operator/SRE
- API consumer
- end user
- administrator
- contributor

Write for the actual audience.

### 2. Define document purpose

Examples:
- quickstart
- architecture overview
- local development
- deployment
- troubleshooting
- API usage
- feature behavior
- runbook
- migration guide

One document may contain multiple sections, but each section should have a clear purpose.

### 3. Audit current truth

Verify:
- commands
- versions
- ports
- environment variables
- directory paths
- service names
- dependencies
- startup order
- API routes
- architecture
- deployment process
- known limitations

### 4. Identify stale or missing content

Compare existing docs against current repository behavior.

Classify:
- correct
- outdated
- missing
- misleading
- duplicated

### 5. Design information order

For setup guides use:
1. purpose
2. prerequisites
3. installation
4. configuration
5. run
6. verify
7. test
8. common problems

For architecture docs use:
1. purpose
2. system context
3. major components
4. request/data flow
5. persistence
6. integrations
7. deployment/runtime
8. observability
9. constraints

### 6. Write commands safely

Commands must:
- come from project configuration/docs
- use placeholders for secrets
- mention working directory if ambiguous
- distinguish development from production

### 7. Document environment variables

For each variable include:
- name
- required/optional
- purpose
- safe example format where useful
- default if verified

Never include production values.

### 8. Document verification

Readers should know how to tell setup/action succeeded.

Examples:
- expected health endpoint
- expected log
- expected UI route
- expected test output

### 9. Document failure recovery

For operational docs include:
- common failure
- likely cause
- diagnostic command
- remediation
- rollback where relevant

### 10. Cross-check against code

Before completion, verify every concrete:
- filename
- command
- route
- environment variable
- port
- service name
- dependency

### 11. Keep documentation maintainable

Prefer:
- links to authoritative internal docs rather than duplicating large content
- stable conceptual explanations
- generated references only when generation is reliable

Avoid repeating the same configuration in many files.

## Required completion report

### Documentation changed
Files and audience.

### Content added/updated
Major sections.

### Repository facts verified
Commands/configuration/behavior checked.

### Known gaps
Anything that could not be verified.
