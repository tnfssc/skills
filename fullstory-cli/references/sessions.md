# Session investigation

This guide was adapted from upstream `general-analysis/references/sessions.md` and `agents/session-context.md`.

Sessions answer why, not how many. Use them when the user asks for examples, an aggregate result raises a causal question, or a hypothesis needs behavioral evidence.

## Keep transcripts out of main context

Session event transcripts are large. Never stream several directly into the main conversation. Redirect each transcript to a file:

```bash
fullstory session events DEVICE_ID SESSION_ID --raw > /tmp/fullstory-session.json
jq '.events[] | {event_time,event_type,event_properties}' /tmp/fullstory-session.json
```

If the environment supports subagents, give an isolated subagent the file path and a focused question. Do not paste the whole transcript into the prompt.

Ask focused questions such as:

- Did the checkout submit? If not, what was the last interaction?
- Which element received rage clicks, and did the page change afterward?
- Was there a JavaScript or network error? What were the exact message and page?

## Workflow

1. Retrieve 3–5 sessions:

   ```bash
   fullstory sessions --metric METRIC_ID
   # or
   fullstory sessions --segment SEGMENT_ID
   ```

2. Save each transcript to a separate file with `fullstory session events`.
3. Inspect each file with targeted `jq`, or delegate it to an isolated context.
4. Compare the answers for a repeated page, element, error, or sequence.
5. Report the pattern and session URLs as evidence.

Stop when the pattern is clear. Pull more sessions only when the sample remains inconclusive. Never generalize the sample frequency to the entire population without a metric.
