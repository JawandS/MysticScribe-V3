# MysticScribe v0 Technical To-Do

This backlog is ordered to produce a testable vertical slice early. Complete each section before expanding its scope.

## 1. Project Foundation

- [ ] Create the Python package and `pyproject.toml`.
- [ ] Pin the supported Python version and core dependencies.
- [ ] Add typed configuration for model routing, database path, seed, retry limit, and run length.
- [ ] Add commands for formatting, linting, type checking, and tests.
- [ ] Add a minimal CLI entry point with explicit `init`, `run`, and `inspect` commands.

Done when the empty application installs, starts, and passes all local checks.

## 2. Domain Contracts

- [ ] Define typed identifiers for runs, turns, characters, locations, events, and idempotency keys.
- [ ] Define `ActionProposal`, `Resolution`, `CheckResult`, and `Observation` models.
- [ ] Define the allowlisted state-command variants.
- [ ] Define actor-scoped and adjudicator-scoped state views.
- [ ] Define clock, turn-order, state-version, and usage-ledger models.
- [ ] Add validation tests for valid and rejected payloads.

Done when every boundary can exchange validated data without using unstructured dictionaries.

## 3. SQLite State Store

- [ ] Add schema creation and versioned migrations.
- [ ] Store simulation runs, clock, turn order, and state version.
- [ ] Store characters, attributes, conditions, goals, locations, facts, and inventories.
- [ ] Store character-specific knowledge and memories.
- [ ] Store turns, append-only events, RNG results, and model usage.
- [ ] Implement one atomic resolution transaction.
- [ ] Enforce optimistic version checks and unique idempotency keys.
- [ ] Add JSON fixture import and snapshot export.
- [ ] Test rollback, duplicate commits, and restart persistence.

Done when canonical state survives restart and a resolution cannot be partially or repeatedly applied.

## 4. State MCP Server

- [ ] Expose the active character's knowledge-scoped view.
- [ ] Expose the broader adjudication view for the current turn.
- [ ] Expose resolution commit through validated commands.
- [ ] Expose read-only run, state, and event inspection.
- [ ] Expose development-only seed and reset operations for an explicitly named run.
- [ ] Enforce active-actor, caller-role, state-version, and idempotency checks.
- [ ] Test that one character cannot retrieve another character's private facts.

Done when all canonical world and character access flows through the MCP boundary.

## 5. Deterministic Check Tool

- [ ] Implement seeded d20 generation as an ordinary Pydantic AI function tool.
- [ ] Allow only easy, moderate, and hard difficulties: DC 10, 15, and 20.
- [ ] Resolve modifiers from the active character's validated context.
- [ ] Calculate totals and success in code.
- [ ] Record inputs and results for the eventual atomic turn commit.
- [ ] Test bounds, modifiers, seeded output, and success calculation.

Done when the model can select a permitted check but cannot invent its roll, modifier, total, or result.

## 6. Character Actor

- [ ] Create one reusable Pydantic AI Character Actor definition.
- [ ] Construct each invocation from the active character's scoped MCP view.
- [ ] Require exactly one structured `ActionProposal`.
- [ ] Keep invocations stateless and exclude hidden facts.
- [ ] Add bounded retries for invalid structured output.
- [ ] Test proposals using a fake model before connecting a live provider.

Done when different character contexts produce independently validated proposals without durable chat history.

## 7. Action Adjudicator

- [ ] Create one shared Pydantic AI Action Adjudicator definition.
- [ ] Provide the proposal and relevant adjudication view.
- [ ] Permit calls to the deterministic check tool.
- [ ] Require one structured `Resolution` containing only allowlisted commands.
- [ ] Validate that reported check results match recorded tool results.
- [ ] Reject invented attributes, targets, items, facts, or state transitions.
- [ ] Test no-check, success, failure, and invalid-command paths with a fake model.

Done when an action becomes a validated resolution without granting the model mutation authority.

## 8. Simulation Scheduler

- [ ] Implement fixed repeating character order.
- [ ] Skip characters marked ineligible while preserving order.
- [ ] Track tick, round, and turn position in canonical state.
- [ ] Orchestrate actor view, proposal, adjudication view, resolution, and atomic commit.
- [ ] Make in-world failure consume a turn.
- [ ] Ensure technical failure does not advance state or time.
- [ ] Add bounded retries and visible terminal errors.
- [ ] Resume from the correct character after application restart.
- [ ] Support manual stop, turn limit, round limit, and terminal scenario state.

Done when a run completes deterministically ordered turns and resumes safely after interruption.

## 9. Initial Simulation Fixture

- [ ] Create one contained placeholder location.
- [ ] Create three characters with distinct goals, attributes, inventories, and private facts.
- [ ] Add a situation likely to require a check.
- [ ] Add a fact known to the world but hidden from at least one character.
- [ ] Configure a three-round default run.
- [ ] Verify the fixture imports repeatedly without duplicating state.

Done when the fixture exercises turns, knowledge isolation, RNG, and state mutation.

## 10. Observer CLI

- [ ] Show run, round, tick, active character, proposal, and committed outcome.
- [ ] Show RNG calls and resulting checks.
- [ ] Show state-version changes and applied commands.
- [ ] Provide concise and diagnostic verbosity modes.
- [ ] Add commands to inspect current state, character knowledge, events, and usage.
- [ ] Clearly distinguish committed world truth from model execution history.

Done when a developer can understand a run without opening SQLite or reading raw traces.

## 11. Routing, Usage, and Observability

- [ ] Configure LiteLLM Proxy through environment-based settings.
- [ ] Keep provider and model names outside simulation logic.
- [ ] Attribute model calls, tokens, latency, and cost to run, turn, and agent role.
- [ ] Instrument model, MCP, tool, scheduler, and commit operations with OpenTelemetry.
- [ ] Preserve validation errors and retries without treating them as canonical events.
- [ ] Redact credentials and sensitive request metadata from logs.

Done when each turn's operational behavior and cost can be inspected end to end.

## 12. v0 Acceptance Suite

- [ ] Run the three-character fixture for three complete rounds.
- [ ] Assert that every eligible character acts exactly once per round.
- [ ] Assert that private knowledge never appears in another actor's context.
- [ ] Assert that at least one correctly calculated RNG check is committed.
- [ ] Assert that event and state changes commit atomically.
- [ ] Assert that duplicate commits have no additional effect.
- [ ] Assert that restart resumes at the correct turn.
- [ ] Assert that model and schema failures do not advance the clock.
- [ ] Assert that usage and tool activity are attributable to their run, turn, and role.
- [ ] Run one opt-in smoke test through the configured live model route.

Done when all architecture acceptance criteria pass automatically.

## Deferred Beyond v0

- Dynamic initiative, reactions, interrupts, and simultaneous actions.
- Variable fictional time and long-running actions.
- Full D&D combat, spell, progression, and rules support.
- Separate Narrator and Character Steward agents.
- Multiple locations and broad world simulation.
- Rich UI, VTT integration, voice, and multiplayer controls.
- Additional model providers beyond validating the existing routing boundary.

