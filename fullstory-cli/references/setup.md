# Setup, auth, plumbing, and provenance

## How it works

`fullstory` is a Bash 3.2-compatible wrapper around `mcpc`, `jq`, and a persistent session named `@fullstory` connected to:

```text
https://api.fullstory.com/mcp/fullstory
```

Each friendly command builds a JSON argument object and calls `mcpc --json @fullstory tools-call`. `fullstory call` provides raw passthrough. MCP text envelopes are unwrapped so stdout contains the tool payload.

A Fullstory organization must have both StoryAI and Model Context Protocol enabled under its account settings. A connected organization with StoryAI disabled may expose zero tools.

## OAuth setup

```bash
fullstory setup
fullstory tools
```

`fullstory setup` runs browser OAuth, connects `@fullstory`, then pings server.

## API-key setup

`mcpc connect` supports custom HTTP headers. Fullstory API keys therefore work without a proxy. MCP uses a Bearer header, unlike the Fullstory REST API's Basic header.

Either export the key:

```bash
export FULLSTORY_API_KEY='...'
fullstory setup
```

Or store the key in `~/.config/fullstory/env`:

```dotenv
FULLSTORY_API_KEY=...
```

Then run the setup command:

```bash
chmod 600 ~/.config/fullstory/env
fullstory setup
```

The wrapper refuses the key file unless its mode is exactly `600`. Never commit the key or pass it as a normal CLI argument.

## Session behavior

- `FULLSTORY_SESSION` defaults to `@fullstory`.
- `FULLSTORY_SERVER` defaults to the hosted endpoint above.
- `FULLSTORY_TIMEOUT` defaults to 120 seconds.
- `FULLSTORY_ENV_FILE` can select another key file.
- Calls retry once after mcpc exits with 1, 3, or 4. Server or tool errors (exit 2) are not retried.

Use these commands for troubleshooting:

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

The adaptations replace direct MCP calls with `fullstory` CLI commands, preserve the large-transcript isolation guidance, route segment scoping through `compute_metric` instead of the upstream `update_metric` guidance, and update session review to the current hosted tools (`session_screenshot`, `session_get_a11y_tree`) from [Fullstory's live tool reference](https://developer.fullstory.com/mcp/tools-reference/).

To refresh:

1. Fetch current upstream commit and live tool reference.
2. Diff upstream `skills/general-analysis`, `skills/comparisons`, `skills/session-review`, and `agents/session-context.md` against these references.
3. Preserve CLI command forms and local setup section.
4. Replace removed or renamed tools from live reference; never retain stale aliases.
5. Record new commit here and update `references/tools.md`.
