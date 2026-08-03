# Issues: view, search, write

## View

```bash
linear issue view ENG-123                    # full issue JSON (description, status, assignee, url, gitBranchName, …)
linear issue view ENG-123 --relations        # + blocking/related/duplicate relations
linear issue view ENG-123 --releases --needs # + releases, customer needs
linear issue open ENG-123                    # open in browser
linear issue comments ENG-123                # comment thread (paginated)
```

Useful jq: `linear issue view ID | jq -r .description`, `... | jq -r .gitBranchName`.

## Search / list / report

```bash
linear issue list -a me                                  # my issues (any state)
linear issue list -a me -s started                       # state accepts type, name, or ID:
                                                         #   types: triage backlog unstarted started completed canceled
linear issue list -t Engineering -s "In Progress" -n 100
linear issue list -q "cache stampede"                      # title/description search
linear issue list -p "Payments Revamp" --no-archived
linear issue list --label Bug --priority urgent
linear issue list -a null -t Engineering                 # unassigned
linear issue list --updated-after -P7D --fields id,title,status,assignee
linear issue list --parent ENG-42                     # sub-issues
linear issue list --cycle current -t Engineering
```

- Output: `{issues: [...], hasNextPage, cursor}` — page with `--cursor CURSOR`.
- `--fields` (comma-sep) keeps reports small; `id` is always included. Available:
  title, description, status, statusType, priority, estimate, assignee, labels,
  project, team, url, gitBranchName, createdAt, updatedAt, completedAt, dueDate,
  parentId, cycleId, triageIntel, …
- `--order createdAt|updatedAt` (default updatedAt).

## Create

```bash
linear issue create -t Platform --title "Fix cache stampede" \
  -b "Steps:\n1. ..." --priority high --labels Bug --project "Payments Revamp" -a me
linear issue create -t ENG --title "..." --body-file notes.md --parent ENG-42
git diff | linear issue create -t ENG --title "..." --body-file -   # stdin body
```

`-t/--team` and `--title` are required. Body is Markdown — use real newlines
(the server rejects escaped `\n` styling); `--body-file` is the safe route for
multi-line content. Mention users with `@displayName`.

## Update / transition / assign

```bash
linear issue update ENG-123 -s Done                    # transition
linear issue update ENG-123 -a me --priority medium    # assign + priority
linear issue update ENG-123 --no-assignee              # unassign
linear issue update ENG-123 --labels Bug,Regression    # REPLACES the whole label set
linear issue update ENG-123 --blocks ENG-99 --blocked-by ENG-42   # append-only
linear issue update ENG-123 --link 'https://github.com/…/pull/123|PR #123'
linear issue update ENG-123 --due 2026-08-15 --estimate 3 --milestone Engineering
```

Field flags (create+update share them): `--title -b/--body --body-file -t/--team
-p/--project -s/--state -a/--assignee --no-assignee --delegate --priority
--labels --parent --due --estimate --cycle --milestone --link 'url|Title'
--blocks --blocked-by --related --dup-of`.

Full-body rewrite: `-b`/`--body-file` on update replaces the entire description.
For surgical edits use `patch` ops via raw call (anchors must match exactly once;
ops: replace, insert_before, insert_after, prepend, append, replace_range):

```bash
linear call save_issue id:="ENG-123" \
  patch:='[{"op":"append","text":"\n\n## Findings\n..."}]'
linear call save_issue id:="ENG-123" \
  patch:='[{"op":"replace","old_string":"status: open","new_string":"status: fixed"}]'
```

## Comments

```bash
linear issue comment ENG-123 -b "Fixed in PR #123"
linear issue comment ENG-123 --body-file notes.md
some-cmd | linear issue comment ENG-123 --body-file -        # stdin
linear issue comment ENG-123 -b "agreed" --reply-to COMMENT_ID
```

Comment edit/delete, and comments on projects/docs/initiatives, go through raw
calls: `linear call save_comment id:=… body:=…`, `linear call delete_comment id:=…`
(destructive), `linear call save_comment projectId:=… body:=…`.
