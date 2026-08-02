# SDK and protocol

## Connection model

```text
CLI / MCP server / SDK -> active Open Browser Use socket -> native messaging host -> Chrome extension -> tabs/debugger/history/downloads
```

The extension starts the native host via Chrome Native Messaging; the host writes the active socket registry so clients can discover it. Pass `--socket`/`socketPath` explicitly only when the runtime supplies one.

## Install SDKs

```sh
npm install open-browser-use-sdk
pip install open-browser-use-sdk   # import as open_browser_use
go get github.com/ifuryst/open-browser-use/packages/open-browser-use-go   # import as obu
```

## JavaScript

```ts
import { connectOpenBrowserUse } from "open-browser-use-sdk";

const browser = await connectOpenBrowserUse({ socketPath, sessionId: "obu-docs-scan-20260510" });
try {
  await browser.client.nameSession("Task - OBU");
  const tab = await browser.newTab();
  await tab.goto("https://example.com", { waitUntil: "domcontentloaded" });
  console.log((await tab.playwright.domSnapshot()).slice(0, 4000));
} finally {
  await browser.client.finalizeTabs([]);
  browser.close();
}
```

Low-level: `new OpenBrowserUseClient({ socketPath, sessionId })`, `await client.connect()`, `await client.executeCdp(tabId, method, params)`. Notifications: `client.onNotification(event => ...)` (e.g. `onDownloadChange`).

## Python

```py
from open_browser_use import connect_open_browser_use

browser = connect_open_browser_use(socket_path=..., session_id="obu-issue-scan-20260510")
try:
    browser.client.name_session("Issue scan - OBU")
    tab = browser.new_tab()
    tab.goto("https://example.com", wait_until="domcontentloaded")
    text = tab.playwright.locator("body").inner_text(timeout_ms=10000)
finally:
    browser.client.finalize_tabs([])
    browser.close()
```

Low-level: `OpenBrowserUseClient(socket_path=..., session_id=...)`, `client.execute_cdp(tab["id"], method, params)`.

## Go

```go
browser, err := obu.ConnectActive(obu.Options{SessionID: "obu-issue-scan-20260510", Timeout: 20 * time.Second})
defer browser.Close()
defer browser.Client.FinalizeTabs(nil)
browser.Client.NameSession("Issue scan - OBU")
tab, _ := browser.NewTab()
tab.Goto("https://example.com", obu.GotoOptions{WaitUntil: obu.LoadStateDOMContentLoaded, Timeout: 15 * time.Second})
```

Low-level: `obu.NewClient(obu.Options{SocketPath, SessionID})`, `client.ExecuteCDP(tabID, method, params)`.

## Core JSON-RPC methods

`ping`, `getInfo`, `createTab`, `getTabs`, `getUserTabs`, `getUserHistory`, `claimUserTab`, `finalizeTabs`, `nameSession`, `attach`, `detach`, `executeCdp`, `moveMouse`, `waitForFileChooser`, `setFileChooserFiles`, `waitForDownload`, `downloadPath`, `readClipboardText`, `writeClipboardText`, `readClipboard`, `writeClipboard`, `turnEnded`.

```sh
open-browser-use call --session-id "$ID" --method getInfo --params '{}'
```

Escape hatch from any SDK: `client.request(method, params)` / `client.Request(...)`.

## Action plan format

One action per line, `#` comments, shared session/turn, default tab set by `open-tab`/`claim-tab`. Actions: `ping info tabs user-tabs history name-session open-tab claim-tab navigate wait-load page-info cdp move-mouse wait-file-chooser set-file-chooser-files finalize-tabs turn-ended call`.

## MCP

```toml
[mcp_servers.open_browser_use]
command = "obu"
args = ["mcp", "--session-id", "obu-<task-or-conversation-id>"]
```

Speaks newline-delimited JSON-RPC (`initialize`, `ping`, `tools/list`, `tools/call`) and mirrors the CLI action surface plus `run_action_plan`. Pass `--socket`/`--socket-dir` only if the runtime needs an explicit socket.

## User tab claiming

`user-tabs`/`getUserTabs` → pick by title/url/recency/group → `claim-tab --tab-id <id>` / `claimUserTab`. Never invent a tab id.

## Cleanup

`finalize-tabs --keep '[]'` (or SDK equivalent) once, as the last browser action of the turn. `status: "deliverable"` for a user-facing result (moves to `✅ Open Browser Use`); `status: "handoff"` for unfinished work needing user input (stays in the task group).

## File chooser

`wait-file-chooser --tab-id <id>` (or SDK `waitForFileChooser`) → trigger the picker in the page → `set-file-chooser-files --file-chooser-id <id> --file /abs/path` (repeat `--file` or comma-separate for multiple).
