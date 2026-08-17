# MysticScribe

MysticScribe is an observable autonomous multi-agent world simulation. The v0 implementation
is being built in the dependency order recorded in `docs/v0-tech-todo.md`.

## Development

Install the locked development environment and run every local check:

```console
uv sync
uv run poe check
```

The CLI is available through `uv run mysticscribe --help`. Configuration uses environment
variables prefixed with `MYSTICSCRIBE_`; nested model and run-length values use a double
underscore, such as `MYSTICSCRIBE_MODEL__ACTOR_MODEL`.
