# Sprints / epics / boards / releases

```sh
jira sprint list --table --plain --columns id,name,start,end,state
jira sprint list --current --plain --columns key,summary,status,assignee,priority
jira sprint list --current -a$(jira me) --plain ...   # standup / handoff view
jira sprint list --prev|--next --plain
jira sprint list SPRINT_ID --plain
jira sprint add SPRINT_ID KEY1 KEY2     # write op
```

Extra sprint filters: `--current --prev --next --state future,active --table --show-all-issues`.

```sh
jira epic list [--table] --plain --columns key,summary,status,assignee
jira epic list EPIC-123 --plain --columns key,summary,status,assignee,priority
jira epic create -n"Name" -s"Summary" -b"Desc" --no-input   # write op
jira epic add EPIC-123 KEY1 KEY2                             # write op
jira epic remove KEY1 KEY2                                   # write op
```

```sh
jira project list
jira board list -pABC
jira release list -pABC     # needs Jira versions enabled
jira open [KEY]
```
