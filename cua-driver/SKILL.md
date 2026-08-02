---
name: cua-driver
description: Drive a native GUI app on the host (macOS/Windows/Linux) with the cua-driver CLI or MCP server — snapshot an app's accessibility tree, click/type/scroll by element_index or pixel coordinates, and verify by re-snapshotting, without stealing foreground focus. Use when the user asks to operate, drive, automate, or perform a GUI task in a real native application.
---

# cua-driver

Cross-platform native-app automation. Default transport is the shell: `cua-driver <tool-name> '<JSON-args>'`. MCP tools (`mcp__cua-driver__*`) exist but are only needed when the caller specifically asks for MCP. Requires the persistent daemon, which owns platform identity, policy, and the per-window element cache.

## Install / verify

```bash
/bin/bash -c "$(curl -fsSL https://cua.ai/driver/install.sh)"   # macOS/Linux
cua-driver doctor                                                # reports host + entry point
cua-driver serve                                                 # start the daemon (required for every tool call)
```

Companion docs in this folder cover platform specifics (`LINUX.md`), the typed browser route (`BROWSER.md`), and trajectory recording (`RECORDING.md`). Run `cua-driver doctor` to learn which platform file applies.

## Core concepts

- **Session** — a stable id you choose (`"research-1"`), declared with `start_session` and passed as `session` on every call. Owns your agent cursor (overlay, not the real pointer) and the immutable capture policy for that run. End with `end_session`.
- **`(pid, window_id)`** — the addressing pair for every window-scoped tool. `launch_app` returns `pid` plus a `windows` array; pick a `window_id` from it (or call `list_windows({pid})` for a long-lived process). The driver validates the window belongs to that pid and is on the current Space/desktop.
- **Snapshot invariant** — snapshot before AND after every action. The pre-snapshot resolves the `element_index` you're about to use (indices are stale across turns and don't cross windows/apps). The post-snapshot verifies the action landed; an unchanged tree means the action probably no-op'd — say so, don't assume success.
- **`capture_scope`** — per-session, immutable, set by `start_session`:
  - `auto` (default): begins in `window` scope; full-desktop actions are locked until the window ladder is exhausted, each step verified, and you explicitly call `escalate_session`. One-way.
  - `window`: window-only perception and actions; desktop tools rejected.
  - `desktop`: full-desktop perception and foreground/system actions; window tools rejected.

## Perception is both — modality is chosen at action time

`get_window_state({pid, window_id})` returns **both** the accessibility tree and a screenshot by default — no capture mode to pick. Ground on the tree, cross-check against the pixels. `include_screenshot:false` is a perf knob (skip the grab when just re-indexing), not a modality choice. `capture_mode` is deprecated/ignored.

You choose how to address the target on the **action** call:

- **element ax action** — pass `element_index`/`element_token`. Dispatch via the accessibility rung (AXPress / UIA Invoke / AT-SPI doAction). Backgroundable, z-order-independent, the only driver-verifiable rung. **Default.**
- **element px action** — pass `x, y` (window-local screenshot pixels, top-left origin, y-down). Best-effort; you confirm via re-snapshot. Use for canvas/video/WebGL/custom-drawn surfaces the AX tree doesn't reach.

The keyboard family (`type_text`, `press_key`, `hotkey`) takes `element_index` (ax) OR `x,y` (px) — mutually exclusive. The px form pixel-clicks to focus the renderer, then delivers the keystroke — the one-call fix for Chromium/Electron inputs the ax path can't reach.

## The verify-then-escalate ladder

```
get_window_state(pid, window_id)            # tree + screenshot, both, always
resp = click(pid, window_id, element_index) # or type_text / set_value / press_key
get_window_state(pid, window_id)           # re-snapshot — did the tree change?

if resp.effect == "confirmed" and tree changed: done   # driver-verified (ax rung only)

# escalate only on a real signal:
#   resp.effect == "suspected_noop"
#   resp.escalation.recommended == "px"
#   get_window_state.degraded (empty tree → non-AX surface)
#   tree disagrees with the screenshot

# Rung 2 — element px action off the SAME screenshot
click(pid, x, y); get_window_state(pid, window_id) → verify

# Rung 2b — typed browser page tools if get_browser_state can bind this window
#           (see BROWSER.md)

# Rung 3 — background delivery was dropped
re-call same action with delivery_mode:"foreground"; verify

# Rung 4 — desktop fallback (auto sessions only, explicit + one-way)
escalate_session(session, reason="foreground_ineffective", detail="...")
get_desktop_state(session) → desktop_action(session, scope:"desktop", ...) → verify
```

Action responses carry a verdict: `effect` ∈ {`confirmed` (ax read-back ok), `unverifiable` (px/foreground — you confirm off the screenshot, not a failure), `suspected_noop` (likely no-op → cross to px)} and optional `escalation.recommended` (`px` or `foreground`).

**`foreground` is a reaction, never a prediction.** Fire the `background` default first; let the driver tell you it can't. On Wayland an unfocused window can't be pixel-targeted in the background, so the recommendation there is `foreground`, not `px` (see LINUX.md).

## Canonical loop

```bash
cua-driver serve
cua-driver start_session '{"session":"research-1","capture_scope":"auto"}'
cua-driver launch_app '{"bundle_id":"..."}'          # → {pid, windows:[{window_id,...}]}
cua-driver get_window_state '{"pid":844,"window_id":10725}'
# ...act...
cua-driver get_window_state '{"pid":844,"window_id":10725}'   # verify
cua-driver end_session '{"session":"research-1"}'
cua-driver stop
```

`launch_app` is idempotent — two runs launching the same app get the same instance. For concurrent runs give each its own `session` (own cursor) AND `creates_new_application_instance:true` (own window).

## Tool dispatch table

Every row assumes a `(pid, window_id)` from the last `get_window_state`. `window_id` is required alongside `element_index`; optional on pixel forms.

| Intent | Tool | Notes |
|---|---|---|
| List windows | `list_windows({pid})` | returns `window_id`, `title`, `bounds`, `is_on_screen`, `on_current_space` |
| Snapshot | `get_window_state({pid, window_id})` | returns `tree_markdown` (elements tagged `[N]`) + `screenshot_*`; populates the element_index cache. `screenshot_out_file:"/tmp/shot.jpg"` writes to disk (stdout stays readable) |
| Left click | `click({pid, window_id, element_index})` \| `click({pid, x, y})` | default `action:"press"`; `modifier:["cmd"\|"ctrl"]`; `count:2` for double |
| Double-click | `double_click({pid, window_id, element_index})` | default action if advertised (Open on Finder items), else stamped pixel double-click |
| Right click | `right_click({pid, window_id, element_index})` \| `click({..., action:"show_menu"})` | browser page content → typed route (BROWSER.md) |
| Type text | `type_text({pid, text, window_id, element_index})` (ax) \| `type_text({pid, text, window_id, x, y})` (px) | ax focuses then writes; px pixel-clicks to focus renderer then types |
| Set non-text control value | `set_value({pid, window_id, element_index, value})` | AX-only — dropdown/checkbox/slider/stepper; also the keyboard-commit workaround on minimized windows |
| Scroll | `scroll({pid, direction, amount, by, window_id, element_index})` | synthesizes PageUp/PageDown/arrows per pid |
| Press key | `press_key({pid, key, window_id, element_index, modifiers})` (ax) \| `press_key({pid, key, x, y})` (px) | ax sets focus then posts key; px pixel-clicks to focus, then sends |
| Send key (no focus change) | `press_key({pid, key, modifiers})` | key goes to pid's current focus |
| Modifier combo | `hotkey({pid, keys})` \| `hotkey({pid, x, y, keys})` | e.g. `["cmd","c"]`; posted per-pid. px pixel-clicks a field first (e.g. `["cmd","v"]` to paste into it) |

Desktop-scope equivalents omit `pid`/`window_id` and pass `scope:"desktop"` (screen-absolute coords from the latest `get_desktop_state`): `click`, `scroll`, `drag`, `move_cursor`, `type_text`, `press_key`, `hotkey`.

## Window state → what works

| state | `get_window_state` | element-index click | `press_key` commit | pixel click |
|---|---|---|---|---|
| frontmost | ✅ | ✅ | ✅ | ✅ |
| backgrounded/visible | ✅ | ✅ | ✅ | ✅ |
| minimized | ✅ | ✅ (fires in place) | ❌ silent no-op — use `set_value` or click a commit button | ❌ no on-screen bounds |
| hidden | ✅ | ✅ | depends | ❌ |
| other desktop/Space | ⚠️ tree may be stripped — `off_space:true` | ✅ | ✅ | ❌ |

## Pixel-coordinate clicks

`click({pid, x, y})` — coords are window-local screenshot pixels (same space as the PNG). PNGs are capped at 1568 px long-side by default (matches vision downsampling limits), so the image you see and the click coordinate system are the same resolution — no scaling math. For precision, write the screenshot to disk, draw a crosshair, verify before clicking. `right_click({pid, x, y})` and `modifier` clicks also take pixel form.

## Web-rendered apps (browsers, Electron, Tauri)

For page content in Chromium-family browsers and Electron, prefer the typed browser route (`get_browser_state`, `browser_click`, `browser_type`, `browser_navigate`) — see `BROWSER.md`. For browser chrome, permission prompts, downloads, file pickers, Safari, Firefox, Tauri, and embedded webviews without exact binding, use the native `get_window_state` + ax/px ladder.

## Common errors

| Error | Meaning | Fix |
|---|---|---|
| `No cached AX state for pid X window_id W` | Skipped `get_window_state` this turn, or mismatched `window_id` | Call `get_window_state` with the same `window_id` you intend to click |
| `Invalid element_index N for pid X window_id W` | Stale/out-of-range index | Re-snapshot, pick a fresh index |
| `window_id W belongs to pid P, not …` | window_id owned by a different process | `list_windows({pid:X})` to enumerate |
| `AX action … failed` / `UIA invoke failed` | Element doesn't support the default action | Try `show_menu`/`confirm`/`cancel`/`pick`, or pixel-click the element's center |

## Notes

- `tree_markdown` can be huge (Finder ~1600 elements). When it exceeds token limits the harness saves it to a file; use `jq -r '.tree_markdown'` + `grep` to pull the section you need.
- The agent cursor overlay is enabled by default for declared sessions (anonymous actions are cursor-less). Toggle with `set_agent_cursor_enabled`; tune motion with `set_agent_cursor_motion`. Visual-only — never moves the real pointer.
- Recording (trajectories + optional MP4) is opt-in via `start_recording`/`cua-driver recording start` — see `RECORDING.md`.