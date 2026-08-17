# Collaboration Rules

These rules apply to the entire repository.

## Current Project State

- v0 discovery and architecture decisions are complete.
- `docs/project-memory.md` is the durable project summary.
- `docs/v0-architecture.md` is the confirmed implementation baseline.
- `docs/v0-tech-todo.md` is the ordered development backlog.
- Implementation has begun; **Project Foundation** is complete and verified.
- Begin next with **Domain Contracts** in the backlog.
- Keep deferred features out of v0 unless the user explicitly changes scope.

## Conversation

- Keep chat focused on one main idea, topic, or decision at a time.
- Give the user time to understand and respond before advancing.
- Keep responses ultra-concise. Every sentence must add meaningful information.
- Use chat as the primary place for discovery and decisions.
- Ask at most one focused question at a time.
- Do not redirect the user to a workbook or ask them to edit a document to continue the conversation.
- After the user responds, resolve or clarify the current topic before introducing the next one.

## Project Memory

- Treat `docs/project-memory.md` as the durable summary of project direction.
- Record confirmed decisions separately from hypotheses and open questions.
- Update memory after material decisions or meaningful changes in direction so work can resume after a restart.
- Preserve concise rationale when it is necessary to understand a decision.
- Use documents as records, not interactive worksheets.
- Never treat an unanswered chat question as a decision.

## Execution

- Do not scaffold architecture from provisional ideas.
- Before implementation, identify the single decision currently being made.
- Prefer small, reviewable changes with explicit verification.
- Follow the v0 backlog in dependency order and mark items complete only after verification.
- Update the current project state and project memory after meaningful implementation milestones.

## Development Framework

- Work autonomously through one requested backlog stage, making reasonable low-risk assumptions.
- Use `uv` for Python versions, dependencies, locking, environments, builds, and command execution.
- Keep runtime dependencies bounded to compatible versions and commit `uv.lock` as the exact resolution.
- Define portable quality tasks in `pyproject.toml`; the full local gate is `uv run poe check`.
- Track implementation and verification in `docs/v0-tech-todo.md` as work progresses.
- Update `docs/project-memory.md` after a stage passes its completion criteria.
- End a completed stage with exactly two concise overview sentences and up to three material unresolved questions for user review.
- Never pad a handoff with trivial, reversible, or safely assumed questions.
- A multi-question stage handoff is the explicit exception to the conversation rule limiting chat to one question at a time.
