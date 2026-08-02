# cua-driver — Linux

The Linux backend drives X11 apps in the background (no raise/activate/real-pointer-warp) — same no-foreground contract as macOS/Windows. AT-SPI is talked to natively over D-Bus (`atspi`/`zbus); no `pyatspi` or GObject typelibs needed at runtime.

## Input delivery (no-foreground)

- **Pixel click** — `XSendEvent(ButtonPress/Release)` to the resolved target window. No raise, no activate, no real-pointer warp. (Not `XTestFakeButtonEvent` — that would route through the focused window.)
- **Element click** (`element_index`) — AT-SPI `do_action` on the accessible. Toolkit-native, focus-free.
- **type_text** — AT-SPI `EditableText` first (focus-free; lands in an unfocused window's editable for Qt6/GTK4). For a non-editable focused widget (spreadsheet cell, terminal, canvas) it synth-types via XTest; terminals take a focus-free pty-injection path.
- **Agent cursor** — synthetic overlay, never moves the real pointer. Glides on clicks and `move_cursor`.

## delivery_mode

Every input tool takes optional `delivery_mode`:
- `background` (default) — inject without activating/raising.
- `foreground` — activate target (EWMH `_NET_ACTIVE_WINDOW`), inject, restore prior active window. The escalation when a background inject didn't land (e.g. a GTK dialog button).
- `bring_to_front` — persistent `_NET_ACTIVE_WINDOW` activation (the `wmctrl -a` equivalent), kept active. Call before foreground input to avoid a per-call flash.

`type_text` reports `verified`: AT-SPI `EditableText.insertText` (path `ax`) → `verified:true` (driver-verifiable); keystroke/XSendEvent/XTest/foreground → `verified:false` (confirm via screenshot).

## ax/px choice on Linux

`get_window_state` returns both tree + screenshot. `degraded:true` (empty AT-SPI walk) → do an element px action off the screenshot (X11) or escalate to `delivery_mode:"foreground"` (Wayland: raw background pixels can't target an unfocused window).

## AT-SPI needs the session bus

AT-SPI lives on the desktop session's D-Bus (`DBUS_SESSION_BUS_ADDRESS`). The daemon auto-discovers it at startup (`/run/user/<uid>/bus`, or reads it from a running `gnome-session`/`xfce4-session` environ), so normal desktop logins just work. Two things must still be true:

1. An accessibility bus must be running (`/usr/libexec/at-spi-bus-launcher`) and `toolkit-accessibility` on. `cua-driver doctor` probes `org.a11y.Bus` for real.
2. The daemon must run as the desktop user (root-against-user-session is the Linux analogue of Windows Session 0 isolation).

Empty AT-SPI walk is surfaced as `degraded:true` + `degraded_reason` (vs. a window that genuinely has no controls).

## X11 modality matrix

| Modality | delivery_mode | Path | Driver-verifiable? |
|---|---|---|---|
| Element click | background | `x11_atspi` (AT-SPI do_action) | ✅ |
| Element px (x,y) | background | `x11_atspi` for AX apps; else MPX `x11_pixel` | ✅ when AT-SPI-at-point lands; else best-effort |
| Pixel click, escalated | foreground | `x11_pixel_fg` (EWMH activate → inject → restore) | ❌ confirm via screenshot |
| type_text editable | background | `ax` (AT-SPI insertText) | ✅ `verified:true` |
| type_text non-editable focus | bg/fg | `key_events` / `key_events_fg` | ❌ confirm via screenshot |

A background element px action lands on X11 — for AX apps via AT-SPI `do_action`-at-point, exactly like macOS/Windows. The MPX virtual-pointer path needs real Xorg + `/dev/uinput`; under Xvnc/minimal containers without uinput, escalate to `foreground`.

## Wayland

Set `CUA_DRIVER_RS_ENABLE_WAYLAND=1`. Backend selected by compositor:
- **Sway/wlroots** — foreign-toplevel, wlr-screencopy, virtual pointer/keyboard. Full discovery + foreground input + semantic background actions; raw background pointer/keyboard remains focus-bound.
- **GNOME/Mutter** — WinRects Shell helper for geometry/activation + portal/libei for foreground raw input. Requires the `winrects@cua` extension (`Enabled:Yes`, `State:ACTIVE`) and portal grant.
- **KDE/KWin** — AT-SPI + portal where available; target-specific activation experimental, unsafe raw input refuses.

Standard Wayland has no client protocol for raw input to an arbitrary occluded surface. Background AX actions deliver via AT-SPI; a PX left click delivers when hit-testing resolves to an actionable AT-SPI control. Other focus-bound background shapes return `background_unavailable` (they don't silently drop). Use `delivery_mode:"foreground"` for raw Wayland input.

## Triage

1. `cua-driver doctor` — reports display server, whether `org.a11y.Bus` answers, discovered `DBUS_SESSION_BUS_ADDRESS`, ffmpeg availability.
2. `XDG_SESSION_TYPE` — `x11` fully supported; `wayland` needs `CUA_DRIVER_RS_ENABLE_WAYLAND=1`.
3. Empty AT-SPI tree (`degraded:true`) — most likely: daemon not on session bus (headless/container/`runuser`/root); a11y bridge off (`gsettings set org.gnome.desktop.interface toolkit-accessibility true`); GTK4/Qt6/Chromium populate lazily (re-snapshot after interaction).

## Forbidden vectors

Don't shell out to things that foreground a target: `wmctrl -a`/`-R`, `xdotool windowactivate`, `xdotool key --window ... alt+Tab`. Use cua-driver tools with explicit `window_id`.