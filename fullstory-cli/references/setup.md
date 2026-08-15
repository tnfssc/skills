# Setup, auth, plumbing, and provenance

## How it works

`fullstory` is a Bash 3.2-compatible wrapper around `mcpc`, `jq`, and a persistent session named `@fullstory` connected to:

```text
https://api.fullstory.com/mcp/fullstory
```

Each friendly command builds a JSON argument object and calls `mcpc --json @fullstory tools-call`. `fullstory call` is raw passthrough. MCP text envelopes are unwrapped so stdout contains tool payload.

Fullstory org must have both StoryAI and Model Context Protocol enabled under account settings. A connected org with StoryAI disabled may expose zero tools.

## OAuth setup

```bash
fullstory setup
fullstory tools
```

`fullstory setup` runs browser OAuth, connects `@fullstory`, then pings server.

## API-key setup

`mcpc connect` supports custom HTTP headers. Fullstory API keys therefore work without proxy. MCP uses a Bearer header, unlike Fullstory REST API's Basic header.

Either export key:

```bash
export FULLSTORY_API_KEY='...'
fullstory setup
```

Or store it in `~/.config/fullstory/env`:

```dotenv
FULLSTORY_API_KEY=...
```

Then:

```bash
chmod 600 ~/.config/fullstory/env
fullstory setup
```

Wrapper refuses key file unless mode is exactly `600`. Never commit key or pass it as a normal CLI argument.

## Session behavior

- `FULLSTORY_SESSION` defaults to `@fullstory`.
- `FULLSTORY_SERVER` defaults to hosted endpoint above.
- `FULLSTORY_TIMEOUT` defaults to 120 seconds.
- `FULLSTORY_ENV_FILE` can select another key file.
- Calls retry once after mcpc exit 1, 3, or 4. Server/tool errors (exit 2) are not retried.

Troubleshooting:

```bash
fullstory status
mcpc @fullstory logs -n 50
mcpc @fullstory ping
fullstory setup
```

## Vendored guidance

Analytics, comparison, validation, session, and review guidance was adapted from [`fullstorydev/fullstory-skills`](https://github.com/fullstorydev/fullstory-skills) at commit:

```text
b20614e2d08d7a7c70775bb62b5af640f60b024b
```

Adaptations replace direct MCP calls with `fullstory` CLI commands, preserve large-transcript isolation guidance, and update session review to current hosted tools (`session_screenshot`, `session_get_a11y_tree`) from [Fullstory's live tool reference](https://developer.fullstory.com/mcp/tools-reference/).

To refresh:

1. Fetch current upstream commit and live tool reference.
2. Diff upstream `skills/general-analysis`, `skills/comparisons`, `skills/session-review`, and `agents/session-context.md` against these references.
3. Preserve CLI command forms and local setup section.
4. Replace removed or renamed tools from live reference; never retain stale aliases.
5. Record new commit here and update `references/tools.md`.
