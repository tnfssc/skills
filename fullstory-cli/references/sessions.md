# Session investigation

Adapted from upstream `general-analysis/references/sessions.md` and `agents/session-context.md`.

Sessions answer why, not how many. Use them when user asks for examples, aggregate result raises causal question, or hypothesis needs behavioral evidence.

## Keep transcripts out of main context

Session event transcripts are large. Never stream several directly into main conversation. Redirect each transcript to file:

```bash
fullstory session events DEVICE_ID SESSION_ID --raw > /tmp/fullstory-session.json
jq '.events[] | {event_time,event_type,event_properties}' /tmp/fullstory-session.json
```

If environment supports subagents, give isolated subagent file path plus focused question. Do not paste whole transcript into prompt.

Good questions:

- Did checkout submit? If not, what was last interaction?
- Which element received rage clicks, and did page change afterward?
- Was there JavaScript or network error? Exact message and page?

## Workflow

1. Retrieve 3–5 sessions:

   ```bash
   fullstory sessions --metric METRIC_ID
   # or
   fullstory sessions --segment SEGMENT_ID
   ```

2. Save each transcript to separate file with `fullstory session events`.
3. Inspect with targeted `jq`, or delegate each file to isolated context.
4. Compare answers for repeated page, element, error, or sequence.
5. Report pattern plus session URLs as evidence.

Stop when pattern is clear. Pull more sessions only when sample remains inconclusive. Never generalize sample frequency to entire population without metric.
