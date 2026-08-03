# Workspace: teams, projects, users, cycles, docs, updates

## Teams, users, statuses, labels

```bash
linear teams                              # {teams: [...]} — paginated
linear team Engineering                   # one team by UUID, key, or name
linear users -q jane                   # filter by name/email
linear user me   |  linear me             # current user (id, teams, email)
linear statuses Engineering               # workflow states for a team (name, type, id)
linear labels -t Engineering              # issue labels; --name to filter
linear cycles Engineering --type current  # current|previous|next|all (team name auto-resolved to UUID)
```

## Projects, milestones, initiatives

```bash
linear projects --member me                       # my projects
linear projects -t Engineering -s started -q payments
linear project "Payments Revamp" --milestones --members --resources
linear milestones "Payments Revamp"
linear call list_initiatives limit:=20
linear call get_initiative query:="Q3 platform" includeProjects:=true
```

## Documents

```bash
linear docs -q "design"                   # list/search docs
linear docs -p PROJECT_UUID               # docs filters take UUIDs (projectId/teamId)
linear doc DOC_ID_OR_SLUG                 # full doc content (Markdown)
linear call save_document title:="..." content:="..." project:="Payments Revamp"   # write via raw call
```

## Status updates (project/initiative health)

```bash
linear updates -p "Payments Revamp"                     # project status updates (default --type project)
linear updates --type initiative --user me
linear call save_status_update type:="project" project:="Payments Revamp" \
  body:="On track. Shipped X." health:="onTrack"    # write via raw call (check schema first)
```

## Releases, diffs/reviews, attachments, agent skills

No dedicated subcommands — use `linear tools <pattern>` + `linear call`:

- Releases: `list_release_pipelines`, `list_releases`, `get_release`, `save_release`,
  `list_release_notes`, `save_release_note`; attach issues via `save_issue addReleases:=[...]`.
- Code review (Linear diffs): `list_diffs`, `get_diff`, `get_diff_threads`,
  `save_diff_comment`, `resolve_diff_thread`, `submit_diff_review`, `merge_diff`
  (the last two are destructive/outward-facing — confirm before using).
- Attachments: `get_attachment`, `create_attachment` (base64),
  `prepare_attachment_upload` + `create_attachment_from_upload`, `delete_attachment`.
- `search_documentation` (= `linear search-docs`) searches Linear's product docs,
  not your workspace.

Before any raw call, check the schema: `mcpc @linear tools-get <tool>`.
