# Setup, auth, and CI

## Requirements

Node.js ≥ 14 (`fetch` is used, so ≥ 18 in practice) and npm. No other dependencies —
the package's only runtime dep is `commander`.

## Running it

Prefer `npx`; there is no reason to keep a global install current:

```bash
npx --yes @statsig/siggy@latest gates list
npx --yes @statsig/siggy@0.0.4  gates list     # pinned, for CI
```

`--yes` skips the "Ok to proceed?" prompt on first download. npx caches the package, so repeated
calls in one session are fast.

If a global install already exists (`npm i -g @statsig/siggy`), the binary is `siggy` and behaves
identically. `npm view @statsig/siggy version` is the only reliable way to see the published
version — `siggy --version` always prints `0.0.0.0`.

## Getting keys

Statsig Console → **Settings → Project Settings → Keys & Environments**.

- **Console API key** — server-side admin key. Grants read/write over the whole project (create,
  update, **delete** gates and experiments). Treat it like a production credential.
- **Client API key** — the same public client SDK key your app ships. Only used for evaluation
  (`check` / `get-value`).

Keys are per-project. To work against a different Statsig project you must re-run `siggy config`
with that project's keys — there is no project flag and no profile support.

Console keys are prefixed `console-`, client keys `client-`. **`siggy` does not check the prefix**,
so a mismatched flag is accepted silently and only surfaces later as "key not set".

### Recovering from `config -k <console-key>`

The most likely first-run mistake, because the CLI's own error text tells you to run `config -k` for
the console key — which is the *client* flag. Symptom: `config -k` prints `Client API key set`, then
every command still reports `Console key not set`.

There is no unset command, so fix it in two steps — set the right slot, then delete the wrong entry
by hand (`siggy` only ever reads the file):

```bash
npx --yes @statsig/siggy@latest config -c <console-key>
printf 'machine statsig.com\n    consolekey %s\n' '<console-key>' > ~/.netrc   # drops the bad clientkey
chmod 600 ~/.netrc
npx --yes @statsig/siggy@latest config      # → "Console API key is present."
```

Don't leave a console key parked in `clientkey`: `gates check` and `get-value` would send an admin
credential to the public Client API endpoint. If a console key has been exposed anywhere, rotate it
in the Console — it can delete gates and ship experiments.

## How keys are stored — read this before running `config`

`siggy config` writes to `~/.netrc`, `machine statsig.com`, attributes `consolekey` / `clientkey`,
**in plaintext**. There is no env-var, no keychain, and no alternative config path.

The write path parses `~/.netrc`, mutates the in-memory map, and then **regenerates the entire file
from scratch**. Consequences if you already have a `~/.netrc`:

- **Comments are destroyed.** The parser strips everything after `#` and the writer never puts it back.
- **Entry order is normalized** — machines are re-emitted sorted alphabetically, indented 4 spaces.
- **`macdef` blocks and bare `default` entries are mangled**, because the parser only understands
  whitespace-separated `key value` pairs grouped under `machine`.
- **A `~/.netrc` whose first token is not `machine` will crash `siggy config`** with a TypeError —
  the parser has no current-machine to assign into.

So:

```bash
cp ~/.netrc ~/.netrc.bak            # if it exists
npx --yes @statsig/siggy@latest config -c <console-key>
chmod 600 ~/.netrc                  # the writer does not set restrictive perms on a new file
diff ~/.netrc.bak ~/.netrc          # confirm nothing else was lost
```

If you'd rather not let it touch the file, write the entry yourself — the CLI only reads it:

```
machine statsig.com
    clientkey client-XXXX
    consolekey console-XXXX
```

Verify with `npx --yes @statsig/siggy@latest config`, which prints presence only:
`Console API key is present.` / `Client API key is present.` / `No keys set.`

## CI

There is no env-var path, so a CI job must materialize a netrc before calling `siggy`:

```yaml
- name: Configure Statsig
  env:
    STATSIG_CONSOLE_KEY: ${{ secrets.STATSIG_CONSOLE_KEY }}
  run: |
    umask 077
    printf 'machine statsig.com\n    consolekey %s\n' "$STATSIG_CONSOLE_KEY" > "$HOME/.netrc"

- name: Flip the gate
  run: |
    npx --yes @statsig/siggy@0.0.4 gates update my_gate '{"isEnabled":true}' > out.json 2> err.txt
    [ -s err.txt ] && { cat err.txt >&2; exit 1; }   # siggy exits 0 on failure — check stderr
    cat out.json
```

Two CI rules that follow from the CLI's behavior:

1. **Never rely on the exit code.** It is `0` whether the call succeeded, was rejected by the API,
   or never went out because no key was set. Assert on stderr or on the content of stdout.
2. **Always pass `-f` to `delete`.** Without a TTY the confirmation prompt gets an empty answer and
   the command aborts silently — a "successful" no-op run.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `Console key not set. Please run \`statsig config -k …\`` | No console key. The message is wrong twice: the binary is `siggy`, and console is `-c`. Run `siggy config -c <console-key>`. |
| `Client key not set…` | `check` / `get-value` need the **client** key: `siggy config -k <client-key>`. |
| `Invalid JSON` | A `<...-json>` argument or `-u` value failed `JSON.parse`. Wrap it in single quotes so the shell doesn't eat the double quotes. |
| `Unauthorized` / `403` | Key is for a different project, or is a server secret rather than a console key. |
| Command not found after global install | Node's global bin dir isn't on `PATH` — use `npx` instead. |
| `siggy --version` says `0.0.0.0` | Expected; see above. |
