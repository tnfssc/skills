# JSON bodies for `update`, `ship`, and `-u`

`siggy` validates nothing beyond `JSON.parse`. Whatever you pass is forwarded to the Console API,
so the schema is the Console API's: <https://docs.statsig.com/console-api/introduction>.

## The safe workflow: round-trip, don't hand-write

`update` is a `PATCH`. Top-level keys you omit are untouched, but any key you *do* send **replaces
that key wholesale** — sending `rules` replaces the entire rules array, silently dropping rules you
didn't include. So for anything beyond a one-field flip, read the current state, edit it, and send
it back:

```bash
siggy gates get my_gate > /tmp/gate.json
jq '.rules += [{"name":"Beta orgs","passPercentage":100,
                "conditions":[{"type":"custom_field","operator":"any","field":"orgId",
                               "targetValue":["9","14"]}]}]' /tmp/gate.json > /tmp/next.json
siggy gates update my_gate "$(jq -c '{rules}' /tmp/next.json)"
siggy gates get my_gate | jq '.rules | map(.name)'   # verify — the exit code will not tell you
```

Quote the JSON argument with **single quotes** (or `"$(...)"`), or the shell will strip the double
quotes and you'll get `Invalid JSON`.

## Common one-liners

```bash
# kill switch
siggy gates update my_gate '{"isEnabled":false}'

# percentage rollout — replaces ALL rules; only safe when the gate has exactly this one rule
siggy gates update my_gate '{"rules":[{"name":"Rollout","passPercentage":25,"conditions":[{"type":"public"}]}]}'

# metadata
siggy gates update my_gate '{"description":"Enables X for beta orgs","tags":["beta"]}'
```

## Gate shape (confirmed fields)

```jsonc
{
  "name": "string",              // 3–100 chars: alphanumeric, dash, underscore, dot, space
  "description": "string",       // ≤ 1000 chars
  "idType": "userID",
  "isEnabled": true,
  "tags": ["string"],
  "targetApps": [],
  "teamID": null,
  "owner": { "ownerID": "…", "ownerType": "…", "ownerName": "…", "ownerEmail": "…" },
  "rules": [
    {
      "name": "string",
      "passPercentage": 0,       // 0–100
      "environments": null,      // null = all environments, else ["development", …]
      "returnValue": {},         // dynamic configs / experiments only
      "conditions": [
        {
          "type": "public",      // also: user_id, email, custom_field, passes_gate, fails_segment, …
          "operator": null,      // valid operators depend on `type`
          "targetValue": null,   // string | number | array | null
          "field": null,         // the custom-field key, when type is custom_field
          "customID": null
        }
      ]
    }
  ]
}
```

Rules are evaluated **in order**; the first matching rule decides. Confirm the exact condition
`type`/`operator` pairs you need against a `get` of a gate that already uses them — that is the
most reliable schema reference available.

## Experiment shape (confirmed fields)

```jsonc
{
  "name": "string",
  "hypothesis": "string",        // required by the API
  "idType": "userID",
  "allocation": 100,             // 0–100, share of the layer allocated to this experiment
  "duration": 14,                // days, min 1
  "status": "setup",             // setup | active | decision_made | abandoned | archived
                                 //   | experiment_stopped | assignment_stopped
  "targetingGateID": null,
  "groups": [
    { "name": "Control", "size": 50, "isControl": true,  "description": "", "parameterValues": {} },
    { "name": "Test",    "size": 50, "isControl": false, "description": "", "parameterValues": {} }
  ],
  "primaryMetrics":   [{ "name": "…", "type": "…", "direction": "increase" }],
  "secondaryMetrics": [{ "name": "…", "type": "…" }]
}
```

That is a *subset*. A real experiment object carries ~60 top-level keys (statistical config —
`bayesianPriors`, `bonferroniCorrection`, `cureCovariates`, …). Always `get` before you `update`.

Prefer the lifecycle verbs over patching `status` by hand: `siggy experiments start|reset <id>`
(`abandon` is broken — see below).

## `experiments ship <id> <json>`

Maps to `PUT /console/v1/experiments/<id>/make_decision`. The body schema isn't in the docs, but
probing the API establishes the required fields: **`id` and `decisionReason`**. The positional
`<id>` only builds the URL, so the id must appear in the body as well:

```bash
siggy experiments ship my_exp '{"id":"my_exp","decisionReason":"Test won on activation"}'
```

Missing either gives `[ 'id: Required', 'decisionReason: Required' ]`.

The field that names the **winning variant is unconfirmed**. `groupName` is accepted without
complaint, but that was only exercised against a nonexistent experiment, where the not-found check
fires before any group is resolved. Groups carry both an `id` and a `name`, and names are free-form
— often the variant slug, sometimes an opaque ID, not reliably `Control`/`Test`:

```bash
siggy experiments get my_exp | jq '{status, groups: [.groups[]|{id,name,isControl,size}]}'
```

Shipping is irreversible. Read the real groups, confirm the field against the Console API reference
or the Console UI's network calls, and check the payload with the experiment owner — do not guess.

## `experiments abandon` — no body, no way to pass one

The API requires `decisionReason`; the CLI sends `{}` with no flag to override it, so the command
always fails. Use `curl` directly — see `commands.md`.

## `-u` user objects (`gates check`, `dyncon get-value`, `experiments get-value`)

Sent verbatim as the `user` field to the Client API. It is the standard Statsig user object:

```json
{
  "userID": "12345",
  "email": "someone@example.com",
  "country": "US",
  "appVersion": "1.2.3",
  "userAgent": "…",
  "custom": { "orgId": "9", "plan": "enterprise" },
  "customIDs": { "orgID": "9" },
  "statsigEnvironment": { "tier": "development" }
}
```

Omitting `-u` sends `{}`, so every attribute-based rule fails and you'll see the default — which
looks like "the gate is off" rather than "I gave it nothing to match on". Always pass a user.

`statsigEnvironment.tier` selects the environment a rule's `environments` list is matched against;
without it you are evaluating production.

## Anything the CLI doesn't cover

Metrics, layers, holdouts, audit logs, users, target apps, and tags have no `siggy` command. Call
the Console API directly with the same key:

```bash
curl -sS https://statsigapi.net/console/v1/metrics \
  -H "STATSIG-API-KEY: $(awk '/machine statsig.com/{f=1} f&&/consolekey/{print $2; exit}' ~/.netrc)" \
  -H 'Content-Type: application/json' | jq
```

Console API base is `https://statsigapi.net/console/v1`; the Client API base (evaluation only) is
`https://statsigapi.net/v1`. Both authenticate with the `STATSIG-API-KEY` header.
