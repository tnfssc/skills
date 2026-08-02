# Recording & replaying trajectories

Session-scoped capture of action sequences + pre/post state — for demos, regression diffs, and training data. Invoked only when the user explicitly asks to record; the skill does not auto-enable this.

## Start / stop

```bash
cua-driver recording start ~/cua-trajectories/run-1   # CLI subcommand
# … run the workflow …
cua-driver recording status                            # enabled/disabled, next_turn, output_dir
cua-driver recording stop                              # "Recording stopped. (video → recording.mp4)"
```

Raw-tool equivalent: `start_recording` / `get_recording_state` / `stop_recording`. Requires a running daemon (`cua-driver serve`) — recording state is in-memory and resets on daemon restart. `output_dir` expands `~` and is created with intermediates. Turn numbering starts at 1 each time recording is (re-)enabled.

While enabled, every action-tool call (`click`, `right_click`, `scroll`, `type_text`, `press_key`, `hotkey`, `set_value`) writes a numbered `turn-NNNNN/` folder. Read-only tools (`get_window_state`, `list_windows`, `screenshot`, `list_apps`, permission probes, cursor getters/setters, recording controls) are not recorded.

## Video

On by default → `<output_dir>/recording.mp4` (H.264/30fps), finalized on `stop_recording`. Opt out with `record_video:false`.
- **macOS** — native ScreenCaptureKit (zero-config, inherits daemon's Screen Recording grant; macOS 15.0+). No ffmpeg needed.
- **Windows/Linux** — ffmpeg subprocess (`gdigrab` / `x11grab`). Binary needs to be on PATH (`winget install Gyan.FFmpeg` / `apt install ffmpeg`); when missing, per-turn capture continues without video and `last_error` carries the install hint.

## Turn folder contents

- `before_state.json` / `after_state.json` — a11y state (same `tree_markdown`/`element_count` shape as `get_window_state`) immediately before/after.
- `before.png` / `after.png` — target-window images (scoped to the target even when covered).
- `evidence.json` — capture status for each phase (missing capture is explicitly classified, not absent).
- `app_state.json` / `screenshot.png` — compatibility aliases for `after_state`/`after`.
- `action.json` — tool name, full input args, result summary, pid, click point, ISO timestamp.
- `click.png` — for click-family actions: `before.png` with a red marker at the click point. Both addressing modes covered (`x,y` direct; `element_index` resolved to center via live AX/UIA cache then converted to window-local pixels). Absent for non-click tools.

## Replay

```bash
cua-driver replay_trajectory '{"dir":"~/cua-trajectories/demo1","delay_ms":500,"stop_on_error":true}'
```

Walks `turn-NNNNN/` folders in lexical order, reads each `action.json`, re-invokes the recorded tool/args. `delay_ms` (default 500) paces turns; `stop_on_error` (default true) halts on first failure.

**Caveat — element_index doesn't survive across sessions.** Indices are assigned fresh per `get_window_state` snapshot, keyed on `(pid, window_id)`, so a recorded `element_index:14` from yesterday won't resolve today (different pid/window_id). Pixel clicks (`x,y`) and keyboard tools (`press_key`/`hotkey`/`type_text` without `element_index`) replay cleanly; element-indexed actions require a live snapshot that replay doesn't re-emit (read-only tools aren't recorded). For reliable replay, compose the trajectory from pixel + keyboard primitives, or use it as a regression artifact (diff failure/success patterns across builds) rather than a re-driving script.

If recording is still enabled while replay runs, the replay is itself recorded into the current output dir — the intended regression-diff workflow.