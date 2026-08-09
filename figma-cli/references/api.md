# REST endpoint catalog and raw passthrough

Base URL: `https://api.figma.com`. Discover current schemas in official Figma REST API documentation.

```bash
figma api GET /v1/me
figma api GET /v1/files/FILE_KEY depth=2 geometry=paths
figma api GET /v1/images/FILE_KEY ids=1:23 format=png scale=2
figma api POST /v1/files/FILE_KEY/comments --body '{"message":"Review note"}'
printf '%s' '{"message":"Review note"}' | figma api POST /v1/files/FILE_KEY/comments -
```

## Wrapped reads

- `GET /v1/me` — current user
- `GET /v1/files/:key`, `/meta`, `/nodes`, `/images/:key` — file context and renders
- `GET /v1/files/:key/comments`, `/versions` — collaboration and history
- `GET /v1/files/:key/components`, `/styles` — published file library assets
- `GET /v1/teams/:team_id/projects`, `/components`, `/styles` — workspace and libraries
- `GET /v1/projects/:project_id/files` — project files
- `GET /v1/files/:key/variables/local` — Enterprise-gated variables

## Raw writes

Raw passthrough supports `POST`, `PUT`, `PATCH`, and `DELETE` with JSON body from `--body`, `--body-file FILE`, `--body-file -`, or `-`. These can mutate or delete data. Inspect endpoint schema, exact target, and user intent before running.

Query pairs use `key=value` and are URL-encoded by curl. `--raw`, `-c`, and `--timeout` work globally.
