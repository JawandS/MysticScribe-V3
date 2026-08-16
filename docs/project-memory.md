# MysticScribe Project Memory

Last updated: 2026-08-15

## Status

The repository is new. The contained v0 proof of concept now has an implementation-ready architecture baseline in `docs/v0-architecture.md` and an ordered development backlog in `docs/v0-tech-todo.md`; implementation has not begun.

## Progress

Completed:

- Defined the contained v0 scope, simulation topology, and fixed round-robin loop.
- Selected Pydantic AI with LiteLLM Proxy, one SQLite-backed state MCP server, and application-owned scheduling.
- Defined the minimal Character Actor and Action Adjudicator collaboration.
- Defined scoped knowledge, stateless agent calls, atomic state commits, ordinal time, and the generic d20 mechanic.
- Recorded the implementation baseline and acceptance criteria in `docs/v0-architecture.md`.
- Created the ordered technical backlog in `docs/v0-tech-todo.md`.

Next milestone:

- Implement **Project Foundation**, the first backlog section.

## Vision

Build a modern, provider-portable autonomous multi-agent world simulation that can be observed as it evolves, initially using the OpenAI API and Python where appropriate.

## Project Intent

- This is a fun personal world-building project, not a product-first commercial exercise.
- A primary goal is to sharpen technical skills through practical work with RAG, MCP, Agent Skills, multi-agent systems, and context-window management.
- The simulation should deliberately expose useful agentic primitives for experimentation and learning.
- Examples include RNG through tool calls and character sheets or state through MCP resources and tools.

## Confirmed Constraints

- The system must use meaningful specialist-agent collaboration.
- The world should be able to progress autonomously while a human observes it.
- The human is initially the experimenter and audience, not a required DM in the simulation loop.
- Initial model usage will use OpenAI, without making OpenAI a permanent dependency.
- MCP and portable Agent Skills should be first-class architectural considerations.
- Deterministic game operations must remain ordinary code rather than LLM judgments.
- Canonical campaign state must remain independent of model conversations and agent-framework checkpoints.

## Confirmed Collaboration Style

- Chat covers one main idea at a time and remains ultra-concise.
- Discovery and decisions happen through a single continuing chat thread.
- Ask at most one focused question at a time and allow it to be resolved before advancing.
- Make reasonable assumptions for simple, low-risk choices; ask only when a decision materially affects architecture, behavior, or cost.
- Adopt a clear recommendation without asking for confirmation; stop only when required information or a consequential preference is genuinely unknown.
- Documents preserve context and decisions; they are not workbooks for the user to complete.

## Current Simulation Hypothesis

The system is an autonomous world simulation whose progress can be watched and inspected:

1. Character agents pursue goals using their knowledge, memories, and current state.
2. World or referee agents interpret actions and invoke deterministic tools for rules and randomness.
3. Approved events update canonical world and character state.
4. Narrative or chronicler agents make the evolving simulation understandable to an observer.

The earlier DM-copilot direction is no longer the leading scope.

## Confirmed Simulation Topology

- Deterministic infrastructure advances time and schedules opportunities to act.
- Character agents choose actions based on their goals, knowledge, memories, and current state.
- World or referee agents adjudicate actions and consequences using deterministic tools.
- The observer can watch both the evolving fiction and the underlying agent and tool activity.

## Confirmed v0 Scope

- The first proof of concept simulates one contained location.
- Broader world simulation is deferred until the contained loop is understandable and observable.
- Narrative setting, lore, and character details will use reasonable placeholders.
- Detailed world-building is deferred until the technical simulation is established.

## Confirmed v0 Storage

- SQLite is the canonical store for world and character state.
- JSON is used for seed data, snapshots, and debugging fixtures.
- All mutations pass through structured, validated commands rather than direct agent access to SQLite.

## Confirmed v0 Execution Boundary

- RNG is an ordinary Pydantic AI function tool.
- World and character state are exposed through one MCP server backed by SQLite.
- The simulation clock and scheduler remain application code.

## Confirmed v0 Simulation Loop

- The simulation proceeds like turns around a D&D table: one character acts at a time.
- Characters act in a fixed repeating order; initiative and interrupts are deferred beyond v0.
- Each character proposes one high-level action per turn; the adjudicator resolves the complete action.
- For each turn, the scheduler activates a character, the character agent proposes an action, the adjudicator resolves it using deterministic tools when needed, the state MCP server validates and commits resulting changes, the event is logged, and the clock advances.

## Confirmed v0 Agent Set

- Character Actors propose actions for the character currently taking a turn.
- One shared Action Adjudicator resolves proposed actions.
- v0 has no separate Narrator or Character Steward agent.
- The observer sees the adjudicator's structured outcome, rendered directly by application code.
- Validated state changes are executed through the state MCP server rather than delegated to another agent.

## Confirmed v0 Runtime Defaults

- Character knowledge is scoped: actors cannot see hidden world facts or another character's private knowledge.
- Agent calls are stateless; durable character memories remain in canonical state.
- One reusable Character Actor definition serves character-specific context, and one shared Action Adjudicator serves all turns.
- v0 uses an ordinal clock: one tick per committed turn and one round after every eligible character has acted.
- In-world failure consumes a turn; technical failure does not advance state or time.
- Resolutions commit state changes and an append-only event atomically, with optimistic versioning and idempotency.
- Mechanical checks use a bounded generic d20 rule with easy, moderate, and hard difficulties.
- The initial fixture uses one location, three placeholder characters, and a three-round default run.

## Candidate Agent Roles

- **Character Actor:** pursues a character's goals using its knowledge, memories, relationships, and current situation.
- **Action Adjudicator:** interprets a proposed action using relevant rules and world context, invokes deterministic resolution tools, and returns a structured success or failure outcome.
- **Narrator:** explains the fixed outcome using world-building context without changing its mechanics.
- **Character Steward:** translates approved in-game events into character updates such as XP, level progression, hunger, health, exhaustion, and inventory changes.

Dice generation, success calculations, level rules, and character-state mutations remain deterministic code exposed to agents as tools. Agents select and explain operations; they do not invent mechanical results.

The observer should see one evolving world while still being able to inspect agent activity and tool use for learning.

## Architecture Principles

- Store campaign truth in project-owned typed models and a database or event log.
- Let agents propose validated commands; deterministic services execute them.
- Keep model routing, agent runtime, tools, skills, persistence, and telemetry behind project-owned boundaries.
- Treat model usage and monetary cost as project-owned simulation data, attributable to an agent, model, provider, and simulation run.
- Use MCP for external or reusable tool boundaries, not every internal function.
- Store portable skills as vendor-neutral `SKILL.md` packages.
- Use the selected LiteLLM Proxy as the v0 routing and budget boundary while keeping provider-specific configuration outside simulation logic.
- Use OpenTelemetry as the preferred observability boundary.

## Confirmed Context Boundaries

- **Canonical world state:** authoritative facts about the world and characters, stored independently of model conversations.
- **Agent context and memory:** a deliberately selected, agent-specific view of world state, observations, and remembered events.
- **Execution history:** prompts, responses, handoffs, tool calls, traces, token usage, and cost retained for debugging and learning, never treated as world truth.

Agents interact with canonical state through structured, validated tools rather than editing storage directly.

## Framework Research

### Confirmed Selection Requirements

- The agent framework must work with a model router so providers can be changed without redesigning the simulation.
- Token usage, monetary cost, and enforceable budgets are first-class concerns.
- Agent handoffs, model calls, MCP traffic, and ordinary tool calls must remain observable and understandable for learning.
- Convenience abstractions must not prevent direct use of lower-level tool and MCP primitives.

The leading candidates are:

- OpenAI Agents SDK: smallest set of direct agent primitives, with agents-as-tools, handoffs, MCP integration, sessions, and tracing.
- Pydantic AI: strongest Python-first, typed, provider-portable candidate, with several multi-agent patterns, MCP support, graph workflows, and context-management capabilities.
- LangGraph: strongest explicit durable graph, checkpointing, replay, and state-inspection candidate.

The selected v0 combination is **Pydantic AI with a LiteLLM Proxy**:

- Pydantic AI provides typed, provider-agnostic agents, direct LiteLLM support, inspectable toolsets, and both high- and low-level MCP access.
- LiteLLM provides centralized provider routing, retries and fallbacks, spend tracking, and budgets.
- A project-owned cost ledger should retain attribution per agent and simulation run rather than relying solely on aggregate framework usage.

This selection preserves provider portability while keeping agent, tool, MCP, usage, and cost behavior inspectable.

## Interface Hypothesis

- Engineering validation: CLI with structured event logs and reproducible fixtures.
- First usable surface: an observer view showing world events, character state, agent decisions, and tool calls as the simulation progresses.
- A VTT is explicitly outside the proposed MVP.

## Product and Content Constraints

- Generic recap generation is insufficient differentiation.
- Initial rules content should use properly attributed SRD material and user-authorized content.
- Do not scrape unsupported D&D Beyond endpoints.
- Voice capture introduces recording consent, privacy, retention, and deletion requirements.
- Commercial intent will materially affect licensing, authentication, privacy, and interface decisions.

## Open Questions

### Active

None currently.

### Parked

- Post-session versus live-session scope.
- Detailed agent contracts and schemas.
- Input sources and existing campaign tools.
- SRD-only versus proprietary-content requirements.
- Spoiler and character-knowledge permissions.
- Personal-only versus eventual open-source or commercial distribution.
