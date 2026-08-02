# Installation

Read when asked to install, verify, repair, or explain setup.

## Components

- Chrome extension — browser-side controller (installing/enabling needs the user's Chrome approval).
- Native host + CLI — local `open-browser-use` binary, aliased `obu`.
- SDKs — JS/Python/Go clients that connect to the active native-host socket.

## Install CLI

```sh
npm install -g open-browser-use
brew install iFurySt/open-browser-use/open-browser-use
open-browser-use version   # or: obu version
```

Running with no subcommand prints version, extension detection status, and the next setup/upgrade step.

## Register browser + extension

```sh
open-browser-use setup                              # registers native host, opens Chrome Web Store page
open-browser-use setup --browser chrome-beta
open-browser-use install-manifest --browser <bitbrowser-instance-id>
open-browser-use setup beta                          # release-ZIP path while the Web Store listing is unavailable
open-browser-use install-manifest                     # repair native host manifest only
open-browser-use manifest                             # print manifest without installing
```

Extension install/enable always needs the user's approval — don't bypass it.

## Platform notes

- macOS/Windows may prompt the user to approve the extension after Chrome detects it.
- Linux external extension registration can need elevated permissions.
- Native messaging host name: `com.ifuryst.open_browser_use.extension`.
- Default socket registry: `/tmp/open-browser-use/`.

## Verify

```sh
open-browser-use ping --session-id "$ID"
open-browser-use info --session-id "$ID"
open-browser-use user-tabs --session-id "$ID"
```

If `ping` fails, confirm Chrome is installed/running and the extension is enabled, then see `troubleshooting.md`.
