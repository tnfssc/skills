# Setup, auth, and errors

## How it works

`figma` is a bash wrapper around `curl`. Each subcommand builds a request against
`https://api.figma.com`, sends the personal access token in the `X-Figma-Token`
header, and prints the response body so stdout is the endpoint's plain JSON.

- Script: `~/.tnfssc-skills/figma-cli/bin/figma`, symlinked from `~/.local/bin/figma`.
- Dependencies: `curl`, `jq`, macOS system bash (3.2-compatible).

## First-time setup

Create a personal access token in Figma → Settings → Security, with the scopes the
commands you plan to run need (`file_content:read` covers most reads; comments,
library assets, and variables each have their own scope). Then:

```bash
figma setup figd_XXXX                    # verify + store
printf '%s\n' "$FIGMA_PAT" | figma setup # or read it from stdin, keeping it out of shell history
figma me                                 # verify: prints your Figma user
```

`figma setup` checks the token with `GET /v1/me` before storing it at
`~/.config/figma/token` with mode `600`. `FIGMA_TOKEN` overrides the stored token.
Never put a real token in a script, a doc, or a repository file.

## Exit codes

- `0` — success
- `1` — CLI usage or local validation error
- `2` — HTTP/API error, including plan, scope, and permission gates
- `3` — network or download failure
- `4` — missing or invalid authentication

Figma answers 403 both for a bad token and for an endpoint you simply cannot reach.
The CLI treats a 403 on `/v1/me` (and any 403 whose message mentions the token) as
an auth failure worth re-running `figma setup` for; every other 403 stays an API
error with a plan/scope/permission hint.

## Troubleshooting

```bash
figma me                                          # is the token live?
figma --raw api GET /v1/me                        # unformatted response
FIGMA_TIMEOUT=300 figma file FILE_KEY             # large documents are slow — try --depth 1 first
```

Tokens expire; re-run `figma setup` after a rotation. Set `FIGMA_TOKEN_FILE` only
when the token has to live somewhere other than `~/.config/figma/token`, and
`FIGMA_BASE_URL` only to point at a mock server.
