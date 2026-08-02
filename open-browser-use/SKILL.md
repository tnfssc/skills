---
name: open-browser-use
description: Reference for Open Browser Use, the open-source Chrome automation stack for AI agents (browser extension + native host + CLI/`obu` + JS/Python/Go SDKs + optional MCP server). Use for automating a real Chrome tab — navigation, CDP calls, user tab claiming, file choosers, downloads, clipboard, screenshots.
---

# Open Browser Use

Connects a Chrome extension (MV3), a local native-messaging host, a CLI (`open-browser-use` / `obu`), SDKs, and an optional stdio MCP server, so an agent can drive a real Chrome profile. Not tied to any specific agent runtime — adapt commands/config to whatever's current.

## Concepts

- **Session id** — every CLI/SDK/MCP call for a task should share one session id (e.g. `obu-<task-slug>-<timestamp>`, or the runtime's own conversation id). This scopes tabs, groups, and cleanup to the task. The CLI's fallback `obu-cli` session is for manual one-offs only — don't reuse it across agent tasks.
- **Tab claiming** — `user-tabs` / `getUserTabs` lists the user's open tabs (title, url, group, recency). `claim-tab` takes control of an existing one instead of opening a duplicate — useful for continuing a task or reusing a dev server tab the user already has open.
- **Finalize tabs** — `finalize-tabs --keep '[...]'` (or SDK `finalizeTabs`) releases/keeps tabs at the end of a turn. A tab can be marked `deliverable` (the user-facing result — moves to the `✅ Open Browser Use` group) or `handoff` (task unfinished, e.g. waiting on login/payment/CAPTCHA — stays in the task group). Default to keeping nothing.
- **Browser/profile selection** — `open-browser-use profiles --connected` lists installed browser/profile targets (`chrome`, `chrome-beta`, `bitbrowser:<id>`, etc.) with directory/display names and connection state. When more than one target exists, `--browser`/`--profile` selectors pin every subsequent command to one target for the task.

## CLI

```sh
open-browser-use ping|info --session-id "$ID"
open-browser-use tabs|user-tabs|history --session-id "$ID"
open-browser-use open-tab --session-id "$ID" --url https://example.com
open-browser-use navigate --session-id "$ID" --tab-id <id> --url https://example.com
open-browser-use claim-tab --session-id "$ID" --tab-id <id>
open-browser-use cdp --session-id "$ID" --tab-id <id> --method Runtime.evaluate --params '{"expression":"document.title"}'
open-browser-use name-session --session-id "$ID" --name "Task - OBU"
open-browser-use finalize-tabs --session-id "$ID" --keep '[]'
open-browser-use call --session-id "$ID" --method <rpc-method> --params '{...}'   # unrestricted escape hatch
```

Multi-step orchestration without SDK code — a line-oriented action plan:

```sh
open-browser-use run --session-id "$ID" -c '
name-session "Docs scan - OBU"
open-tab https://docs.browser-use.com
wait-load domcontentloaded
page-info
finalize-tabs []
'
```

`open-tab`/`claim-tab` set the default tab for later tab-scoped actions in the same plan (`wait-load`, `page-info`, `navigate`, `cdp`, `move-mouse`, `wait-file-chooser`).

Screenshots — claim/open the tab, wait for load, then capture via the bundled helper instead of decoding CDP base64 manually:

```sh
open-browser-use run --session-id "$ID" -c '
claim-tab <tab-id>
wait-load domcontentloaded
'
python scripts/capture-screenshot.py --session-id "$ID" --tab-id <tab-id> --output /tmp/page.png [--full-page]
```

## MCP

```toml
[mcp_servers.open_browser_use]
command = "obu"
args = ["mcp", "--session-id", "obu-<task-id>"]
```

Exposes `ping`, `info`, `tabs`, `user_tabs`, `history`, `open_tab`, `claim_tab`, `navigate`, `wait_load`, `page_info`, `cdp`, `move_mouse`, `wait_file_chooser`, `set_file_chooser_files`, `name_session`, `finalize_tabs`, `turn_ended`, `call`, and `run_action_plan` (same action-plan format as `obu run`). Pin `--browser`/`--profile` at server start — they apply to every call, not per-tool.

## SDKs, protocol, install, and troubleshooting

- `references/sdk-and-protocol.md` — connection model, JS/Python/Go SDK patterns, JSON-RPC method list.
- `references/installation.md` — CLI + extension setup per platform.
- `references/troubleshooting.md` — connection, socket, extension/native-host, and permission issues.

## Safety notes

This is the user's real Chrome profile: don't inspect unrelated cookies/passwords/session data, and ask before installing/enabling the extension, submitting forms, purchasing, deleting, or other externally visible actions. Don't guess tab ids — list first. Pause and ask on login/payment/CAPTCHA workflows.
