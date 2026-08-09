# Setup, auth, and errors

## First-time setup

Create PAT in Figma account settings with scopes needed by intended commands. Then:

```bash
figma setup figd_XXXX
printf '%s\n' "$FIGMA_PAT" | figma setup
figma me
```

`figma setup` verifies token through `GET /v1/me`, then stores it at `~/.config/figma/token` with mode `600`. `FIGMA_TOKEN` overrides stored token. Token is sent as `X-Figma-Token`; never put real tokens in scripts, shell history, docs, or repository files.

Dependencies: `curl`, `jq`, macOS system bash 3.2-compatible.

## Exit codes

- `0`: success
- `1`: CLI usage or local validation error
- `2`: HTTP/API error, including plan/scope/permission gates
- `3`: network or download failure
- `4`: missing or invalid authentication

Figma uses 403 for both invalid tokens and access gates. CLI treats `/v1/me` 403 and explicit token/auth errors as authentication failures; other 403 responses stay API errors with plan/scope/permission hint.

## Troubleshooting

```bash
figma me
figma --raw api GET /v1/me
FIGMA_TIMEOUT=300 figma file https://www.figma.com/design/FILE_KEY/Example
```

PATs expire. Re-run `figma setup` after rotation. Set `FIGMA_TOKEN_FILE` only when alternate token storage path is required.
