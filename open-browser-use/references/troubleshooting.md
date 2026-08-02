# Troubleshooting

## First checks

```sh
open-browser-use ping --session-id "$ID"
open-browser-use info --session-id "$ID"
open-browser-use user-tabs --session-id "$ID"
```

If these fail: confirm Chrome is installed and running, the extension is installed/enabled, and the native host manifest is registered (`install-manifest` or `setup`). Ask the user to approve any Chrome prompt — don't bypass it.

## Stale socket / no active host

The CLI discovers the active socket from a registry; if missing it scans `--socket-dir` for `*.sock` files and repairs the registry, dropping stale entries.

```sh
open-browser-use ping --socket /tmp/open-browser-use/example.sock
open-browser-use ping --socket-dir /tmp/open-browser-use
open-browser-use ping --timeout 20s
```

If no host is running, opening Chrome with the extension enabled starts it.

## Extension / native host id mismatch

```sh
open-browser-use manifest            # print current manifest
open-browser-use install-manifest    # repair
open-browser-use setup               # Web Store id
open-browser-use setup beta          # keyed GitHub release ZIP
```

Custom extension builds: pass `--extension-id <id>` to `install-manifest`/`setup`.

## File upload

Prefer the file-chooser flow over OS-level picker automation. If Chrome blocks local file access, ask the user to enable "Allow access to file URLs" on the extension's `chrome://extensions` details page.

## Permissions and escalation

History, debugger, downloads, tab-group, and broad host access are high-privilege. Pause and ask the user when: Chrome isn't installed, opening it would interrupt their session, the extension needs confirmation, the page needs login/CAPTCHA/hardware-key/payment confirmation, or the action affects external systems.
