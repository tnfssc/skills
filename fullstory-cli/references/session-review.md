# Session review

This guide was adapted from upstream `skills/session-review` and corrected to the live tool contract checked on 2026-08-15.

Use this workflow for user-reported bugs, unexpected behavior, user-flow analysis, or UI-state validation.

## Current command sequence

```text
fullstory session open
  → (fullstory session screenshot | fullstory session tree | fullstory session diff)*
  → fullstory session close
```

The current hosted tools are `session_screenshot` and `session_get_a11y_tree`. The deprecated `session_view` tool is nonfunctional and must not be used.

## Workflow

1. Extract the `device_id` and `session_id` from the replay URL, then open the session:

   ```bash
   fullstory session open DEVICE_ID SESSION_ID
   ```

   Save the returned `client_id`, and note the `page_id` and timestamps of interesting events from the summaries. Scan the event summaries for navigations, clicks, errors, network failures, rage clicks, and custom events.

2. Render a screenshot at a key moment:

   ```bash
   fullstory session screenshot CLIENT_ID PAGE_ID TIMESTAMP
   ```

3. Inspect the semantic structure and accessible state:

   ```bash
   fullstory session tree CLIENT_ID PAGE_ID TIMESTAMP
   ```

4. Compare the state changes:

   ```bash
   fullstory session diff CLIENT_ID PAGE_ID FROM_TIMESTAMP TO_TIMESTAMP
   ```

5. Close the session even after investigation errors:

   ```bash
   fullstory session close CLIENT_ID
   ```

Sequential increasing timestamps are faster than random access.

## Report

- State what the user saw at each key moment.
- Include exact observed errors or missing changes.
- Give an evidence-backed cause when the transcript or rendered state proves one.
- Report the cause as unknown when the recording cannot establish it.
- Include the session URL and relevant timestamps.

Do not infer beyond the events, screenshot, accessibility tree, or diff.
