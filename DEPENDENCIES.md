# Bundled skills

The eight dependency skills were copied from the owner's existing
`~/.agents/skills` on 2026-11-16: audit, scope, architect, develop, test,
document, autopilot, and finish.

Their instruction bodies are retained as supplied. Packaged frontmatter uses
portable name/description fields; provider-specific icon, color, and invocation
metadata are omitted. Existing installed versions are
preserved rather than replaced. Project rules and the coordinator's T3 lifecycle
reference take precedence where a generic dependency suggests a different
runtime mechanism, such as shell-based PR waiting.

Repository-specific skills are resolved from the target project and are not
distributed in this package.

## Ponytail review

`skills/ponytail-review` is from DietrichGebert/ponytail at commit
`e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156`, under the MIT license.
Upstream source:
https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/skills/ponytail-review/SKILL.md

The packaged copy replaces example emoji with ASCII labels and uses portable
name/description frontmatter. Its license is included beside the skill.
