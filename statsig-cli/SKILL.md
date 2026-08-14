---
name: statsig-cli
description: Reference for the Statsig CLI ("Siggy", npm `@statsig/siggy`) — create, list, get, update, delete and evaluate Statsig feature gates, dynamic configs, segments, and experiments from the terminal or CI. Use for any Statsig work from a shell — read a gate's rules, enable/disable a gate, change a rollout percentage, check a gate or config value for a user, start/reset/ship/abandon an experiment, or script the Statsig Console API.
---

# statsig-cli (`siggy`)

Thin CLI over the Statsig **Console API** (`https://statsigapi.net/console/v1`) and **Client API**
(`https://statsigapi.net/v1`). It does no validation of its own — it forwards JSON you hand it and
prints what comes back. Everything below is verified against `@statsig/siggy@0.0.4` source, live
`--help` output, and live calls against a real project.

## Invocation — use `npx`, don't install globally

```bash
npx --yes @statsig/siggy@latest <command>     # canonical form
npx --yes @statsig/siggy@0.0.4 <command>      # pin in CI / for reproducibility
```

All examples below write `siggy` for brevity — substitute `npx --yes @statsig/siggy@latest`.
(A global `npm i -g @statsig/siggy` also works and the binary is `siggy`, but prefer `npx`.)

## Auth — two different keys, and which commands need which

```bash
siggy config -c <console-api-key>   # Console key: everything except the two below
siggy config -k <client-api-key>    # Client key: `gates check`, `dyncon get-value`, `experiments get-value`
siggy config                        # no flags → prints only which keys are present (never the values)
```

Keys come from Statsig Console → Settings → Project Settings → Keys & Environments.
They are stored **in plaintext** in `~/.netrc` under `machine statsig.com`. There is no env-var
support. **Read `references/setup.md` before running `siggy config` if `~/.netrc` already exists** —
the write path rewrites the whole file and can mangle or crash on other entries.

## Command map

| Entity | Command group | Console API path |
|---|---|---|
| Feature gates | `siggy gates` | `gates` |
| Dynamic configs | `siggy dyncon` | `dynamic_configs` |
| Segments | `siggy segments` | `segments` |
| Experiments | `siggy experiments` | `experiments` |

Every group has `create <name>`, `get <id>`, `list [-p <page>]`, `update <id> <json>`,
`delete [-f] <id>`. Beyond that:

- `siggy gates check [-u <user-json>] <gate-name>` — evaluate a gate (Client key)
- `siggy dyncon get-value [-u <user-json>] <config-name>` — evaluate a config (Client key)
- `siggy experiments start|reset|abandon <id>`
- `siggy experiments ship <id> <json>` — launch a variant (`make_decision`)
- `siggy experiments get-value [-u <user-json>] <experiment-name>` (Client key)

Full flags, exact syntax, and worked examples: `references/commands.md`.
JSON bodies for `update` / `ship` / `-u`: `references/json-bodies.md`.

## Facts worth knowing

- **Exit code is always 0 — even on failure.** Verified against the live API: missing key, `404 Gate
  not found`, `400 Bad Request`, and malformed-JSON args all print to stderr and exit `0`.
  **Never gate a script on `$?`** — check stderr, or parse stdout for the expected JSON.
- Results go to **stdout** as 2-space-indented JSON (or plain text for a bare `{message}`). Errors go
  to **stderr and are _not_ JSON** — API validation failures print as a JS array literal with single
  quotes, e.g. `[ 'decisionReason: Required' ]`. Do not try to `jq` stderr; match on it as text.
- **`list` truncates.** All four groups return only `id`, `name`, `lastModifiedTime`,
  `lastModifierName` per item. To see rules, values, or enabled state you must `get <id>`. Page size
  is hardcoded to 100; paginate with `-p 2`, `-p 3`, … until you get `[]` — a page past the end
  returns an empty array, which is the only end-of-list signal (there is no total count). `-p 0` and
  non-numeric pages are rejected by the API.
- **`create` sets nothing but the name.** It POSTs `{"name": "<arg>"}`. Configure the entity in a
  second `update` call.
- **`update` is a PATCH with your raw JSON** — top-level keys you omit are left alone, but keys you
  do send are replaced wholesale (sending `rules` replaces the entire rules array).
- **Console commands take the entity `id`; the three Client commands take the entity `name`.**
  `check`/`get-value` pass their argument through as `gateName`/`configName`. Get ids from `list`.
- **`delete` prompts interactively** and only the exact answer `y` proceeds. **The prompt is written
  to stdout**, so it contaminates any captured output. With no TTY and no `-f` it makes no request,
  prints only the prompt (no trailing newline, and not even `Aborted`), and exits `0` — a silent
  no-op that looks like a successful delete. Always pass `-f` in scripts.
- **`experiments abandon` can never succeed.** The API requires a `decisionReason` in the body; the
  CLI sends `{}` and exposes no way to supply one, so it always returns
  `Bad Request Exception [ 'decisionReason: Required' ]`. Use `curl` — see `references/commands.md`.
  (`start` and `reset` need no body and work fine.)
- **`experiments ship` needs the id *inside* the JSON body too**, duplicating the positional arg:
  `{"id": "<same-id>", "decisionReason": "..."}` is the minimum the API accepts.
- `siggy --version` reports `0.0.0.0` — it reads `npm_package_version`, which is unset outside npm
  scripts. Use `npm view @statsig/siggy version` for the real version (0.0.4 as of 2026-08-14).
- **Both "key not set" errors name the wrong flag, and the wrong binary.** They say `statsig` (it's
  `siggy`), and they invert `-c`/`-k`: the console-key error tells you to run `config -k`, and the
  client-key error tells you to run `config -c`. Ignore them — console is `-c`, client is `-k`.

## Scope limits

The CLI covers gates, dynamic configs, segments, and experiments only. Metrics, layers, holdouts,
audit logs, users, targeting apps, and everything else in the Console API have **no** `siggy`
command — call the Console API directly with `curl` and the console key (`STATSIG-API-KEY` header).
See `references/json-bodies.md` for the request pattern.
