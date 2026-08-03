---
name: linear-cli
description: Reference for the `linear` command — a standalone CLI (mcpc-backed, Linear MCP server) for viewing, searching, creating, and updating Linear issues, projects, teams, cycles, docs, and status updates from the terminal. Use for any Linear work — view or summarize an issue, search or report on issues, create/edit/comment/assign/transition, projects, milestones, cycles, labels, documents, initiatives, or Linear setup/auth.
---

# linear-cli

`linear` (`~/.tnfssc-skills/linear-cli/bin/linear`) wraps a persistent mcpc session (`@linear`) to Linear's hosted MCP server (`mcp.linear.app/mcp`). Requires `mcpc` + `jq` and a one-time OAuth (`linear setup`) — see `references/setup.md` if the command is missing or auth fails. The session self-heals on dead/expired connections.

## Command areas

- **View an issue** — `linear issue view ID [--relations]`, `linear issue open ID`. Details: `references/issues.md`.
- **Search / list / report** — `linear issue list` with filters (`-a me`, `-t TEAM`, `-s STATE`, `-q QUERY`, `--fields`). Details: `references/issues.md`.
- **Write** — `linear issue create/update/comment`; surgical description edits via `patch` ops. Details: `references/issues.md`.
- **Workspace** — teams, projects, milestones, cycles, users, labels, statuses, docs, initiatives, status updates. Details: `references/workspace.md`.
- **Everything else** — ~57 MCP tools total; `linear tools [pattern]` to discover, `linear call TOOL k:=v ...` to invoke raw. Catalog: `references/tools.md`.
- **Setup / auth / plumbing** — `references/setup.md`.

## Facts worth knowing

- Output is plain JSON on stdout (MCP envelope already unwrapped) — pipe to `jq`. `-c` for compact, `--raw` to skip pretty-printing. Never interactive.
- `me` resolves to the current user in any assignee/member/user filter; `null` means unassigned (`-a null`).
- Lists paginate: default limit 50 (max 250); responses carry `hasNextPage` + `cursor`, pass back via `--cursor`. `--fields id,title,status` shrinks issue/project/doc list output a lot.
- Date filters accept ISO-8601 dates or durations: `--updated-after -P1D` = last 24h.
- Priorities: 0=None 1=Urgent 2=High 3=Medium 4=Low; the CLI also accepts the words.
- Writes: `--labels` REPLACES the full label set; `--link`/`--blocks`/relations are append-only; `save_*` tools upsert (id present = update). `delete_*` tools exist only via `linear call` — they are destructive and hard to undo.
- Issue/state/team/project args accept names, keys, IDs, or identifiers (e.g. `ENG-123`) — no UUID hunting needed (exception: `list_cycles` wants a team UUID; `linear cycles` resolves names automatically).
