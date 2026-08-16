# MysticScribe v0 Architecture

Status: confirmed design baseline

## Purpose

v0 proves that multiple character agents can take autonomous turns in one persistent world while a separate adjudicator resolves their actions and an observer can inspect the full loop.

It does not attempt to provide a complete D&D rules engine, combat system, polished narrative layer, dynamic initiative, or broad world simulation.

## Runtime Components

1. The application owns the simulation loop, clock, retries, stopping conditions, and model orchestration.
2. A reusable Character Actor agent definition proposes one action for the active character.
3. A shared Action Adjudicator agent resolves that proposal and may call the ordinary RNG function tool.
4. One state MCP server owns all world and character reads and validated mutations.
5. SQLite stores canonical state, committed events, RNG results, and usage attribution.
6. The CLI renders committed outcomes and diagnostic activity directly; there is no Narrator agent.

LiteLLM remains the model-routing boundary, while all model names and provider credentials remain configuration.

## Turn Lifecycle

Characters act in a fixed repeating order.

1. The application selects the next eligible character.
2. It requests that character's scoped view from the state MCP server.
3. A fresh Character Actor invocation returns one structured `ActionProposal`.
4. The application requests the relevant adjudication view from the state MCP server.
5. A fresh Action Adjudicator invocation returns one structured `Resolution` and calls RNG only when a check is necessary.
6. The application submits the resolution to the state MCP server with the expected state version and an idempotency key.
7. The server validates and atomically commits state changes, the turn event, RNG results, and clock advancement.
8. The CLI prints the committed event and moves to the next character.

An adjudicated in-world failure consumes the turn. A transport, model, validation, or commit failure does not consume it; the application retries within a configured limit and otherwise stops the run visibly.

## Time Model

v0 uses ordinal simulation time rather than fictional seconds or minutes:

- `tick` advances after every committed character turn.
- `round` advances after every eligible character has received one turn.
- `turn_position` identifies the active place in the fixed order.

Variable action duration, simultaneous actions, initiative, reactions, and interrupts are deferred.

## Agent Context and Authority

Character Actors receive only:

- their own state and goals;
- public facts visible at their location;
- facts and memories known by that character;
- observable state of nearby characters;
- recent events that character observed.

They never receive hidden world facts or another character's private knowledge.

The Action Adjudicator receives the proposal plus the broader state needed to resolve it. It may select a check from the bounded v0 mechanic and propose typed state commands, but it cannot write canonical state directly.

Agent invocations are stateless. Durable memories belong in canonical state, not provider conversation history or framework checkpoints. The project may retain prompts and responses as execution history for inspection, but they are never world truth.

## Structured Contracts

### ActionProposal

- `actor_id`
- `intent`
- `approach`
- `target_ids`
- `desired_outcome`

The contract does not request private chain-of-thought.

### Resolution

- `actor_id`
- `summary`
- `outcome`: `success`, `failure`, or `no_check`
- optional `check`
- `commands`
- `observations`

### Check

- `difficulty`: `easy`, `moderate`, or `hard`
- `modifier`
- `roll`
- `total`

### State Commands

v0 exposes a small allowlist rather than arbitrary patches:

- set or clear a character condition;
- adjust a bounded character attribute;
- move an item between known containers or characters;
- set a world fact;
- add character knowledge or memory;
- change a character's active goal or eligibility.

Each command is validated against its schema and current state. No agent receives SQL access or a generic database-write tool.

## Resolution Mechanic

Checks use a deliberately small, system-neutral d20 mechanic:

- easy DC: 10;
- moderate DC: 15;
- hard DC: 20;
- success when `d20 + modifier >= DC`.

The adjudicator decides whether a check is needed, selects one of the three named difficulties, and supplies a modifier already present in canonical character state. The RNG tool produces the roll; deterministic application code calculates the total and success. Natural-roll critical rules are deferred.

## MCP Boundary

The single state server provides role-scoped operations for:

- reading the active character's view;
- reading the adjudication view for the current turn;
- applying one complete resolution;
- inspecting committed events and current state;
- seeding or resetting an explicitly selected development run.

Mutation access is reserved for the application orchestrator. The MCP server verifies the active actor, expected state version, command validity, and idempotency key before committing.

## Persistence

The initial SQLite model contains:

- simulation runs and their clock and state version;
- characters, attributes, conditions, goals, and turn order;
- locations and flexible world facts;
- inventories;
- character-specific knowledge and memories;
- turns and append-only committed events;
- RNG rolls;
- model and tool usage attributed to run, turn, role, provider, and model.

Current-state changes and their corresponding event are written in one transaction. JSON is used inside bounded payload columns where the domain is intentionally flexible and for seed fixtures and exported snapshots.

## Initial Fixture

The development fixture uses one contained location and three placeholder characters with distinct goals, attributes, and private facts. It includes at least one situation likely to require a check and one conflict between what the world knows and what an individual character knows.

A run defaults to three rounds and can also stop on a configured turn limit, manual interruption, terminal scenario flag, or unrecoverable error.

## Observability

For every turn, the observer can inspect:

- the active character and scoped context identifiers;
- the structured proposal and resolution;
- MCP reads and the atomic commit;
- RNG inputs and output;
- state version before and after the turn;
- model, token usage, latency, and monetary cost where the provider supplies enough data;
- validation errors and retries.

OpenTelemetry is the instrumentation boundary. SQLite retains the project-owned run ledger and canonical event record.

## v0 Acceptance Criteria

- A seeded three-character simulation completes three rounds in fixed order.
- Every eligible character receives exactly one action per round.
- Character Actors cannot access private facts belonging only to other characters.
- At least one action invokes RNG and records a mechanically correct result.
- Every committed outcome and its state changes share one atomic transaction.
- Restarting the application preserves the world and resumes at the correct turn.
- Duplicate commit attempts cannot apply a resolution twice.
- Model or schema failures are visible and do not silently advance the clock.
- The observer can attribute model usage and tool activity to a run, turn, and agent role.

