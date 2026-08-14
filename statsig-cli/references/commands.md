# siggy — complete command reference

Verified against `@statsig/siggy@0.0.4`. Substitute `siggy` → `npx --yes @statsig/siggy@latest`.

`siggy <group> <subcommand> --help` works at every level and is authoritative if this file drifts.

## Global

```
siggy                     # prints help
siggy -V, --version       # prints 0.0.0.0 (see SKILL.md — known bug)
siggy -h, --help
siggy help <command>
```

## config

```
siggy config                              # report which keys are set (presence only, no values)
siggy config -c, --consolekey <key>       # set Console API key
siggy config -k, --clientkey <key>        # set Client API key
```

Both flags can be given in one call. Values are written to `~/.netrc` under `machine statsig.com`
as `consolekey` / `clientkey`. See `setup.md`.

## The shared CRUD verbs

`gates`, `dyncon`, `segments`, and `experiments` each expose the same five verbs. Substitute the
group name and its argument label:

| Verb | Syntax | HTTP | Key |
|---|---|---|---|
| create | `siggy <group> create <name>` | `POST /console/v1/<path>` body `{"name": …}` | Console |
| get | `siggy <group> get <id>` | `GET /console/v1/<path>/<id>` | Console |
| list | `siggy <group> list [-p <page-number>]` | `GET /console/v1/<path>?page=N&limit=100` | Console |
| update | `siggy <group> update <id> <json>` | `PATCH /console/v1/<path>/<id>` | Console |
| delete | `siggy <group> delete [-f\|--force] <id>` | `DELETE /console/v1/<path>/<id>` | Console |

`<path>`: `gates` / `dynamic_configs` / `segments` / `experiments`.

`list` output is reduced client-side to `[{id, name, lastModifiedTime, lastModifierName}, …]` —
identical for all four groups. `limit` is fixed at 100 and is not exposed as a flag; pagination is
`-p` only. A page past the end returns `[]`, which is the only end-of-list signal. Invalid pages are
rejected by the API (`-p abc` → `[ 'page: Must be a valid number', 'page: Page number must be
greater than 0' ]`).

`delete` without `-f` prompts `Are you sure you want to delete <type> (id: <id>)? (y/n):` and
accepts only the literal `y`; anything else prints `Aborted` and makes no request.

**The prompt goes to stdout, not stderr** — `out=$(siggy gates delete X)` captures the prompt text
along with (or instead of) the result. Worse, with stdin closed or redirected from `/dev/null` the
prompt is printed with no trailing newline, `Aborted` is never reached, no request is made, and the
process exits `0`. In a CI log that is indistinguishable from a successful delete. **Always pass
`-f` non-interactively.**

## gates

```
siggy gates create <gate-name>
siggy gates get <gate-id>
siggy gates list [-p <page-number>]
siggy gates update <gate-id> <gate-properties-json>
siggy gates delete [-f] <gate-id>
siggy gates check [-u <user-object-json>] <gate-name>
```

`check` is the only gate command that uses the **Client** key. It POSTs to
`https://statsigapi.net/v1/check_gate` with `{user, gateName: <arg>}`. With no `-u` the user object
is `{}` — which evaluates against no attributes, so any rule keyed on `userID`, email, country, or a
custom field will not pass. Always pass `-u` for a meaningful check.

```bash
siggy gates check -u '{"userID":"12345","email":"a@writer.com","custom":{"orgId":"9"}}' my_gate
```

## dyncon (dynamic configs)

```
siggy dyncon create <dynamic-config-name>
siggy dyncon get <dynamic-config-id>
siggy dyncon list [-p <page-number>]
siggy dyncon update <dynamic-config-id> <dynamic-config-properties-json>
siggy dyncon delete [-f] <dynamic-config-id>
siggy dyncon get-value [-u <user-object-json>] <dynamic-config-name>
```

`get-value` uses the **Client** key, POSTing to `https://statsigapi.net/v1/get_config` with
`{user, configName: <arg>}`. Same empty-user caveat as `gates check`.

## segments

```
siggy segments create <segments-name>
siggy segments get <segments-id>
siggy segments list [-p <page-number>]
siggy segments update <segments-id> <segments-properties-json>
siggy segments delete [-f] <segments-id>
```

No evaluation command — segments are only readable/writable through the Console API.

## experiments

```
siggy experiments create <experiment-name>
siggy experiments get <experiment-id>
siggy experiments list [-p <page-number>]
siggy experiments update <experiment-id> <experiments-properties-json>
siggy experiments delete [-f] <experiment-id>
siggy experiments start <experiment-id>
siggy experiments reset <experiment-id>
siggy experiments abandon <experiment-id>
siggy experiments ship <experiment-id> <ship-properties-json>
siggy experiments get-value [-u <user-object-json>] <experiment-name>
```

Lifecycle verbs are `PUT /console/v1/experiments/<id>/{start,reset,abandon}` with an empty body,
Console key. `ship` is `PUT /console/v1/experiments/<id>/make_decision` with your JSON body.

`get-value` uses the **Client** key and hits `get_config` (experiments and dynamic configs share
that endpoint), returning the variant the user is bucketed into.

`reset` discards accumulated exposure/results data. `abandon` ends the experiment without shipping.
Both are irreversible from the CLI — confirm with the owner before running either.

### `abandon` is broken — use `curl`

`start` and `reset` need no body and work. **`abandon` cannot succeed as shipped**: the API requires
`decisionReason`, the CLI hard-codes an empty body, and there is no flag to supply one. Every call
returns:

```
Bad Request Exception
[ 'decisionReason: Required' ]
```

Go around the CLI:

```bash
curl -sS -X PUT "https://statsigapi.net/console/v1/experiments/<id>/abandon" \
  -H "STATSIG-API-KEY: $(awk '/machine statsig.com/{f=1} f&&/consolekey/{print $2; exit}' ~/.netrc)" \
  -H 'Content-Type: application/json' \
  -d '{"decisionReason":"why this experiment is being abandoned"}'
```

### `ship` requires the id twice

The positional `<experiment-id>` only builds the URL — it is **not** copied into the body. The API
validates `id` and `decisionReason` as required body fields, so the id must be repeated:

```bash
siggy experiments ship my_exp '{"id":"my_exp","decisionReason":"Test won on activation"}'
```

Omitting either yields `[ 'id: Required', 'decisionReason: Required' ]`. The field naming the
winning variant is **not confirmed** — `groupName` is accepted without complaint, but that was only
tested against a nonexistent experiment, where a not-found short-circuits before any group lookup.
Read the real group names first and confirm against the Console API reference before shipping:

```bash
siggy experiments get my_exp | jq '[.groups[] | {id, name, isControl, size}]'
```

Group `name`s are free-form and are **not** reliably `Control`/`Test` — in practice they are often
the variant slug, and sometimes an opaque ID. Each group carries both an `id` and a `name`; which
one `make_decision` expects is unverified. Shipping is irreversible — do not guess.

## Output contract

- Success with a `data` field → `JSON.stringify(data, null, 2)` on stdout.
- Success with only a `message` field → that string on stdout.
- Anything else → the whole response object, pretty-printed, on stdout.
- Failure → the API's `error`, or `message` (plus `errors` if present), or the raw body, on
  **stderr**. Process still exits `0`.

Stderr is **not** machine-readable. A field-validation failure prints the message on one line and
then the `errors` array via `console.error(array)`, which Node renders as a JS literal — single
quotes, spaces inside the brackets, not JSON:

```
Bad Request Exception
[ 'id: Required', 'decisionReason: Required' ]
```

Match that as text; `jq` will not parse it. Observed error strings: `Gate not found.`,
`Experiment not found.`, `Bad Request Exception`, `Invalid JSON` (the last is the CLI's own, emitted
before any request when a JSON argument fails `JSON.parse`).

Because of the exit-code bug, a scripted check looks like:

```bash
out=$(siggy gates get my_gate 2>/tmp/err)
if [ -s /tmp/err ]; then echo "siggy failed: $(cat /tmp/err)" >&2; exit 1; fi
echo "$out" | jq -r '.isEnabled'
```

"Non-empty stderr means failure" is a sound rule here: across every probe, successful calls wrote
nothing to stderr and failing calls wrote nothing to stdout.
