# Setup, auth, and plumbing

## How it works

`linear` is a bash wrapper around an `mcpc` session named `@linear` connected to
Linear's hosted MCP server `https://mcp.linear.app/mcp` (OAuth 2.1, `default`
profile). Each subcommand builds a JSON argument object with `jq`, pipes it to
`mcpc --json @linear tools-call <tool>`, and unwraps `.content[].text` so stdout
is the tool's plain JSON payload.

- Script: `~/.tnfssc-skills/linear-cli/bin/linear`, symlinked from `~/.local/bin/linear`.
- Dependencies: `mcpc`, `jq`, macOS system bash (3.2-compatible).

## First-time setup

```bash
linear setup     # mcpc login (browser OAuth) + connect @linear + ping
linear me        # verify: prints your Linear user
```

The OAuth consent opens in the default browser. One workspace per auth session —
re-run `linear setup` after switching workspaces.

## Self-healing

Every call retries once after `mcpc restart @linear || mcpc connect ...` when the
failure is client/network/auth-shaped (mcpc exit 1/3/4). Server-side tool errors
(exit 2) are NOT retried, so a rejected write is never re-sent. Tool-level errors
print the server's JSON error to stderr and exit 2.

## Troubleshooting

```bash
linear status                 # session details (state, transport, tool count)
mcpc @linear logs -n 50       # bridge log
mcpc @linear ping             # round-trip check
linear setup                  # full re-auth when the token is revoked/expired
```

- `unauthorized` state → `linear setup`.
- Env overrides: `LINEAR_SESSION` (default `@linear`), `LINEAR_SERVER`
  (default `mcp.linear.app/mcp`; `mcp.linear.app/mcp/readonly` exists for a
  read-only session), `LINEAR_TIMEOUT` (seconds, default 120).
- A parallel read-only setup: `LINEAR_SERVER=mcp.linear.app/mcp/readonly LINEAR_SESSION=@linear-ro linear setup`.
