# Browser automation

For page content in Chromium-family browsers and Electron. Browser chrome, permission prompts, downloads, file pickers, and unsupported engines (Safari, Firefox, Tauri, embedded webviews without exact binding) remain native windows — use `get_window_state` + the ax/px ladder in `SKILL.md`.

## The typed route

Binds an exact native `(pid, window_id)` to a browser target and mints session-scoped tab + element capabilities. Prefer it over the legacy `page` tool, accessibility guesses, omnibox shortcuts, or raw pixels.

```text
start_session
list_windows or launch_app
get_browser_state(pid, window_id, session)       # bind
get_browser_state(target_id, tab_id, session, snapshot_format=semantic_v2)  # snapshot
browser_navigate / browser_click / browser_type / browser_pointer
browser_dialog / browser_set_input_files / browser_download
get_browser_state(target_id, tab_id, session, snapshot_format=semantic_v2)  # verify + refresh refs
end_session
```

Use one `session` value throughout. Never substitute a raw CDP target id, tab ordinal, URL match, or remembered ref for a capability from `get_browser_state`.

## 1. Bind an exact native window

```bash
cua-driver get_browser_state '{"pid":4242,"window_id":991,"session":"browser-run-1"}'
```

Mutate only when the bind reports `status:"ok"`, `binding_quality:"exact"`, and `mutation_allowed:true`. A heuristic title match is read-only. Ambiguity (same-bounds windows, stale geometry, moved tab, process restart) → re-bind; don't pick a window whose title looks close.

## 2. Prepare only when the bind requests it

`get_browser_state` is read-only — it never launches a browser, changes a profile, enables remote debugging, or accepts a consent prompt. If it returns `browser_requires_setup`, choose one explicit flow:

**Driver-owned isolated profile** (prefer when you don't need the user's cookies/login):
```bash
cua-driver browser-approve --pid 4242 --profile-mode isolated_new
cua-driver browser_prepare '{"pid":4242,"session":"browser-run-1","allow_launch":true,
  "profile":{"mode":"isolated_new"},"approval_token":"<token>"}'
```
Result returns a `prepared_pid`; list its windows and bind the new `(pid, window_id)`.

**Existing profile** (needs a separate interactive grant bound to the exact process/window/session — ordinary MCP approval is not enough):
```bash
cua-driver browser-approve --strategy existing_profile --pid 4242 --window-id 991 --session browser-run-1
cua-driver browser_prepare '{"pid":4242,"window_id":991,"session":"browser-run-1",
  "strategy":{"kind":"existing_profile"},"approval_token":"<token>"}'
```
The grant lives only in the daemon, is scoped/expiring, and is discarded on daemon restart. Never pass remote-debugging flags through `launch_app` for a personal profile, edit Chromium `Preferences`/`Local State`, reuse an approval token, copy a personal profile into a driver-owned dir, or terminate/restart the user's browser as a hidden setup step.

## 3. Snapshot the tab

```bash
cua-driver get_browser_state '{"target_id":"<target>","tab_id":"<tab>",
  "session":"browser-run-1","snapshot_format":"semantic_v2"}'
```

`active` is tri-state: `true` (proven selected), `false` (proven unselected), `null` (can't distinguish). Don't guess from list order when all are `null`. Add `include_screenshot:true` when the visual state matters.

The screenshot reports `viewport_css_px` space with `pixel_to_css_scale_x/y`. Convert image pixels to action coords: `css_x = png_x * pixel_to_css_scale_x`. Don't assume device scale 1.

`semantic_v2` composes a11y tree + pierced DOM + layout + viewport. Read `outline` for content; use `refs` only for actions declared in each entry's `actions`; `content_refs` only to scope later reads (a content ref is NOT an action capability). Check `snapshot.complete`/`omitted`/`continuation` — the first response may not be exhaustive. Continue with the opaque `continuation`, or bound a read with `query` or a `scope_ref`. Refs are scoped to session/target/tab/document/frame/latest snapshot; navigation and newer snapshots invalidate old refs.

## 4. Mutate

**Navigate** — `browser_navigate({target_id, tab_id, url, session})`. Only `http:`/`https:`/`about:`. Invalidates tab refs; snapshot again before the next ref action.

**Click** — `browser_click({target_id, tab_id, ref, input_route, session})`.
- `trusted` (default) — CDP Input domain; driver refreshes element box + hit-tests, refuses stale/covered/ambiguous. Standalone Chromium on macOS/Linux can't stay background on trusted pointer → returns `browser_input_trust_unavailable` instead of claiming background. Windows Chrome/Edge have validated trusted background delivery.
- `dom_event` — explicit synthetic JS click (full-background where supported). Never silently change trust class after a refusal. Coordinate clicks (viewport CSS `x,y`) accept trusted route only; prefer refs.

**Type** — `browser_type({target_id, tab_id, ref, text, mode, session})`. `mode:"insert_text"` (default) bulk-inserts; `keystrokes` for per-character key events. `cua-driver describe browser_type` for the live schema.

**Pointer** — `browser_pointer` for `hover`/`right_click`/`double_click`/`scroll`/`drag`. Same `trusted` vs `dom_event` distinction. Hover/right/double/drag need a ref declaring `pointer`; scroll accepts `scroll` or `pointer`. Drag needs `destination_ref` in the same proven frame.

**Dialogs** — `browser_dialog` handles page-owned `alert`/`confirm`/`prompt`/`beforeunload` only. Inspect the tab, then accept/dismiss the opaque `dialog_id`. Browser permission UI and native dialogs are outside this tool. Linux Chromium can't resolve its native modal in background — retry with `delivery_mode:"foreground"` when acceptable.

**File inputs** — `browser_set_input_files` with 1–32 absolute regular-file paths (no symlinks/dirs); bypasses the native picker. Paths redacted from trajectory args.

**Downloads** — `browser_download` activates one ref under destructive approval, saves under a canonical absolute `destination_root`, returns only an opaque download id + byte count (never URL/filename/destination).

## Browser chrome + native fallbacks

The browser tools operate on page content, not the surrounding native UI. Use the native loop for: tabs, address bar, menus, bookmarks, extension UI; permission/auth sheets; native save dialogs and file pickers; WebView2/WKWebView/WebKitGTK/Tauri/Electron without exact correlation; Safari and Firefox. Don't use `Ctrl+L`/`Cmd+L`, tab-switch shortcuts, shell launchers, or activation scripts as a browser API — use `browser_navigate` or the native AX/PX ladder.

When crossing from page tools to a native chrome control (toolbar extension, password manager, global shortcut): snapshot the native `(pid, window_id)`, confirm the intended tab is visibly selected (select via native ladder if not), re-ground the page, then invoke the native control. Prefer an injected field control over a toolbar popup when the screenshot proves it's present; verify autofill only via a non-secret postcondition (`value.length > 0`), never return/log a password. A vault PIN/biometric/master-password unlock is a human handoff.

## Recovery rules

- `browser_requires_setup` → explicit approval + `browser_prepare`; never make setup a hidden read side effect.
- `browser_consent_required` → exact interactive approval flow; don't automate a generic approval dialog.
- `browser_binding_ambiguous` / heuristic → resolve native-window ambiguity + re-bind; don't mutate.
- `browser_ref_stale` → snapshot again, use a new ref.
- `browser_action_unavailable` → pick a ref declaring the action; a readable `content_ref` is not clickable/editable.
- `browser_input_trust_unavailable` → request `dom_event` if its semantics are acceptable, else use the native ladder; don't foreground while calling background.
- closed tab / moved tab / restart / reconnect → discard capabilities, bind again.

Verify the page with a fresh `get_browser_state`. If the result affects native UI, also verify the exact native window with `get_window_state`.

## Support matrix

| Surface | Typed state/mutation | Boundary |
|---|---|---|
| Chrome/Edge on Windows | Exact binding, refs, nav, typing, trusted or DOM click | interactive user session, not Session 0 |
| Chrome/Edge on macOS | Exact binding, refs, nav, typing, explicit DOM click | trusted standalone click refuses to preserve background |
| Chrome/Chromium on Linux X11 | Exact binding, refs, nav, typing, explicit DOM click | trusted standalone click refuses to preserve background |
| Chromium on validated Wayland | Exact binding only when compositor identity provable | ambiguous compositor identity refuses mutation |
| Electron | Exact single-page routes where endpoint/host relationship proven | don't infer support for arbitrary embedded webviews |
| Safari/Firefox | Native window state only | typed page mutation not supported |
| WebView2/Tauri/embedded | Native AX/PX fallback unless an exact route is reported | host/renderer correlation may refuse |

Product classification alone is not a capability claim — trust the structured result from the current host/process/window/session/tab.