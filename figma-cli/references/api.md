# Raw passthrough and endpoint map

`figma api` sends any request to `https://api.figma.com` with the stored token
attached. Query pairs are `key=value` and curl URL-encodes them; `--raw`, `-c`, and
`--timeout` work here as everywhere. Schemas live in Figma's API docs
(<https://www.figma.com/developers/api>) — check one before a write.

```bash
figma api GET /v1/me
figma api GET /v1/files/FILE_KEY depth=2 geometry=paths
figma api GET /v1/images/FILE_KEY ids=1:23 format=png scale=2
figma api POST /v1/files/FILE_KEY/comments --body '{"message":"Review note"}'
printf '%s' '{"message":"Review note"}' | figma api POST /v1/files/FILE_KEY/comments -
```

## What the subcommands cover

- `GET /v1/me` — `figma me`
- `GET /v1/files/:key`, `/meta`, `/nodes` and `GET /v1/images/:key` — `figma file`, `figma nodes`, `figma screenshot`
- `GET /v1/files/:key/comments`, `/versions` — `figma comments`, `figma versions`; `POST .../comments` — `figma comment`
- `GET /v1/files/:key/components`, `/styles` — `figma components`, `figma styles`
- `GET /v1/teams/:team_id/projects`, `/components`, `/styles` — `figma team ...`
- `GET /v1/projects/:project_id/files` — `figma project files`
- `GET /v1/files/:key/variables/local` — `figma variables`

Everything else — dev resources, webhooks, activity logs, variable writes — has no
subcommand and goes through `figma api`.

## Writes

`POST`, `PUT`, `PATCH`, and `DELETE` take a JSON body from `--body`, `--body-file FILE`,
or stdin (`--body-file -` or a bare `-`), and the body is validated as JSON before it
is sent. These calls mutate or delete real design data — confirm the endpoint, the
target IDs, and the user's intent first.
