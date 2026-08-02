---
name: jira-cli
description: Reference for ankitpokhrel/jira-cli (the `jira` command) — viewing, searching, creating, editing, and managing Jira issues, sprints, epics, and boards from the terminal. Use for any Jira/ticket work — view or summarize a ticket, search or report on issues, create/edit/transition/comment/assign/link/clone/delete, worklogs, sprints, epics, releases, boards, or Jira setup/auth.
---

# jira-cli

`jira` (github.com/ankitpokhrel/jira-cli) is a terminal client for Jira Cloud, Server, and Data Center. Requires a configured account (`jira init`, or `JIRA_CONFIG_FILE`) — see `references/setup.md` if the command is missing or auth fails.

## Command areas

- **View a ticket** — `jira issue view KEY [--plain|--raw] [--comments N]`, `jira open KEY`. Details: `references/issue-view.md`.
- **Search / list / report** — `jira issue list` with filters or `-q '<JQL>'`, `--plain`/`--raw`/`--csv` output. Details: `references/issue-search.md`.
- **Write** — create/edit/assign/transition/comment/worklog/link/clone/delete. Details: `references/issue-write.md`.
- **Agile** — sprints, epics, boards, projects, releases. Details: `references/agile.md`.
- **Setup** — install, auth, config, troubleshooting. Details: `references/setup.md`.

## Facts worth knowing

- `--plain`, `--raw` (JSON), and `--csv` avoid the interactive TUI — use one of these for scripting or agent output.
- `$(jira me)` resolves to the current user; useful in `-a`/`-r` filters.
- `jira issue delete` (especially `--cascade`) and bulk edit/transition/comment are destructive and hard to undo.
- Config commonly lives at `~/.config/.jira/.config.yml`; never print tokens or full config contents.
