# Issue view

```sh
jira issue view KEY
jira issue view KEY --plain       # readable terminal output
jira issue view KEY --raw        # full JSON — fields, comments, links, custom fields
jira issue view KEY --comments N  # include N recent comments
jira open KEY                     # open in browser
```

`jira issue show` is an alias for `view`.

Multiple keys: loop and view each, or dump `--raw` per key to `/tmp/KEY.json` for structured comparison.

`--raw` output is JSON with a top-level `fields` object (`summary`, `status.name`, `assignee.displayName`, `priority.name`, etc.) — parse with `jq` or Python.

## Example summary shape

A useful shape for "summarize this ticket" type requests:

```md
**ABC-123 — <summary>**
- Status / owner: <status>, <assignee or unassigned>
- Priority / type: <priority>, <issue type>
- What it is: <1-3 sentence plain-English summary>
- Latest signal: <latest relevant comment/update>
- Next step: <if clear from the ticket>
```
