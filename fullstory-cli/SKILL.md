---
name: fullstory-cli
description: Use Fullstory from the terminal for behavioral analytics, metrics, segments, funnels, session discovery and visual review, StoryAI opportunities, or Fullstory CLI setup and authentication.
---

# fullstory-cli

`fullstory` (`~/.tnfssc-skills/fullstory-cli/bin/fullstory`) wraps a persistent `mcpc` session (`@fullstory`) to Fullstory's hosted MCP server. Requires `mcpc` + `jq` and one-time auth via `fullstory setup`. Session retries once after client, network, or auth-shaped failures.

## Command areas

- **Metrics and segments** — search before building, compute quantitative results, then validate. See `references/general-analysis.md` and `references/validation.md`.
- **Comparisons** — choose event dimensionality or user-level segments correctly. See `references/comparisons.md`.
- **Funnels** — build, compute, and retrieve completion or drop-off sessions. See `references/general-analysis.md`.
- **Sessions** — retrieve matching sessions and inspect large event transcripts outside main context. See `references/sessions.md`.
- **Visual session review** — open, screenshot, inspect accessibility trees, diff, close. See `references/session-review.md`.
- **StoryAI opportunities and pages** — thin aliases plus raw passthrough. See `references/tools.md`.
- **Setup, auth, plumbing, provenance** — see `references/setup.md`.

## Facts worth knowing

- Output is MCP text unwrapped to plain JSON when payload is JSON. Pipe to `jq`; use `-c` for compact output or `--raw` to skip pretty-printing.
- `fullstory tools [pattern]` discovers live tools. `fullstory call TOOL k:=v ...` reaches anything missing from friendly commands.
- Search saved metrics, segments, and funnels before building new objects.
- Segments identify users; metrics measure behavior; sessions explain why.
- Session transcripts are large. Redirect them to a file, inspect with `jq`, or delegate file analysis to an isolated subagent.
- Visual review is stateful: `session open` first, `session close` always. Current commands use `session_screenshot` and `session_get_a11y_tree`; deprecated `session_view` is unsupported.
- Fullstory org must have StoryAI and MCP enabled. Some opportunity tools require StoryAI Premium.
