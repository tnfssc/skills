# Issue search / JQL / reports

```sh
jira issue list --plain
jira issue list --raw
jira issue list --csv
jira issue list --plain --no-headers --columns key,summary,status,assignee
```

Columns available: `type,key,summary,status,assignee,reporter,priority,resolution,created,updated,labels`.

## Common searches

```sh
# Assigned to me, not Done
jira issue list -a$(jira me) -s~Done --plain --columns key,summary,status,priority

# Reported by me this week
jira issue list -r$(jira me) --created week --plain --columns key,summary,status,created

# Unassigned this week
jira issue list -ax --created week --plain --columns key,summary,status,priority

# Assigned, not Done, stale (no update in 24 weeks)
jira issue list -a~x -s~Done --created-before -24w --plain --columns key,summary,status,assignee,updated

# Watched, in project ABC
jira issue list -w -pABC --plain --columns key,summary,status

# Recently accessed
jira issue list --history --plain --columns key,summary,status
```

## Filters

```text
-p KEY                       project
-t, --type Bug                issue type
-s, --status "In Progress"    status; repeatable; ~ negates (-s~Done)
-y, --priority High            priority
-a, --assignee NAME            $(jira me)=self, x=unassigned, ~x=assigned
-r, --reporter NAME
-l, --label backend            repeatable
-C, --component Backend
-P, --parent EPIC-123
--created / --updated          today|week|month|year|date|relative (-7d)
--created-after/-before, --updated-after/-before
--order-by, --reverse, --paginate 0:50
```

## JQL

```sh
jira issue list -q 'project = ABC AND statusCategory != Done ORDER BY priority DESC' --plain
jira issue list -q 'assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC' --plain
```

Quote JQL as a single shell argument.

## CSV export

```sh
jira issue list -q 'project = ABC AND updated >= -30d' --csv > export.csv
```
