# Session review

Adapted from upstream `skills/session-review`, corrected to live tool contract checked 2026-08-15.

Use for user-reported bugs, unexpected behavior, user-flow analysis, or UI-state validation.

## Current command sequence

```text
fullstory session open
  → (fullstory session screenshot | fullstory session tree | fullstory session diff)*
  → fullstory session close
```

Current hosted tools are `session_screenshot` and `session_get_a11y_tree`. Deprecated `session_view` is nonfunctional and must not be used.

## Workflow

1. Extract `device_id` and `session_id` from replay URL, then open:

   ```bash
   fullstory session open DEVICE_ID SESSION_ID
   ```

   Save returned `client_id`. Scan event summaries for navigations, clicks, errors, network failures, rage clicks, and custom events.

2. Render screenshot at key moment:

   ```bash
   fullstory session screenshot CLIENT_ID PAGE_ID TIMESTAMP
   ```

3. Inspect semantic structure and accessible state:

   ```bash
   fullstory session tree CLIENT_ID PAGE_ID TIMESTAMP
   ```

4. Compare state changes:

   ```bash
   fullstory session diff CLIENT_ID PAGE_ID FROM_TIMESTAMP TO_TIMESTAMP
   ```

5. Close even after investigation errors:

   ```bash
   fullstory session close CLIENT_ID
   ```

Sequential increasing timestamps are faster than random access.

## Report

- What user saw at each key moment.
- Exact observed errors or missing changes.
- Evidence-backed cause when transcript or rendered state proves one.
- Unknown when recording cannot establish cause.
- Session URL and relevant timestamps.

Do not infer beyond events, screenshot, accessibility tree, or diff.
