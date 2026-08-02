# Write ops

Destructive/broad changes (`delete`, `--cascade`, bulk edit/transition/comment, moving many issues) are worth a confirmation step before running.

Multiline description/comment: use a temp file or stdin instead of inline shell quoting.

```sh
cat >/tmp/jira-body.md <<'EOF'
Steps:
1. Open checkout
2. Enter SAVE10
3. Click Apply

Expected: discount appears.
Actual: spinner never stops.
EOF

jira issue create -p PAY -tBug -s"Checkout page hangs on coupon apply" \
  -yHigh -lcheckout -lregression --template /tmp/jira-body.md --no-input
```

```sh
jira issue create -pABC -tBug -s"Summary" -yHigh -lbug -b"Description" --no-input
jira issue create -tStory -s"Story title" -PEPIC-42 --no-input
jira issue create --custom story-points=3 -tStory -s"..." --no-input
cat body.md | jira issue create -pABC -tTask -s"Summary" --template - --no-input
```

Create flags: `-p/-t/-P/-s/-b/-y/-r/-a/-l/-C/--fix-version/--affects-version/-e/--custom/-T(--template file or -)/--web/--no-input/--raw`.

```sh
jira issue edit KEY -s"New summary" --no-input
jira issue edit KEY --label -old --label new --no-input   # +/- semantics for repeatable fields
cat body.md | jira issue edit KEY --template - --no-input
```

Aliases: `update`, `modify`. `--skip-notify` suppresses watcher notifications.

```sh
jira issue assign KEY "User Name" | $(jira me) | default | x

jira issue move KEY "In Progress"           # aliases: transition, mv
jira issue move KEY Done -RFixed -a$(jira me)

jira issue comment add KEY "text" [--internal] [--template file|-]

jira issue worklog add KEY "2d 1h" [--comment ...] [--started "..." --timezone ...]

jira issue link KEY OTHER-KEY Blocks
jira issue link remote KEY https://example.com "Design doc"
jira issue unlink KEY OTHER-KEY

jira issue clone KEY [-s"..."] [-H"old text:new text"]

jira issue delete KEY [--cascade]
```
