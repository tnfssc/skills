# Comparisons

This guide was adapted from upstream `skills/comparisons` at the pinned commit in `setup.md`.

The right mechanism depends on what the comparison axis is.

## Event or session properties: dimensionality

If the property describes the context of the event at the moment it fired, use a single `top_n` metric grouped by that property.

Examples include device type, browser, OS, page URL, and element.

```bash
fullstory metric build top_n 'rage clicks grouped by device type'
```

Refine an existing metric instead of rebuilding it:

```bash
fullstory metric update METRIC_ID 'filter to Chrome only'      # returns a NEW metric_id
```

Do not use user segments for event properties. A user who used mobile once and later rage-clicked on desktop may qualify for both user cohorts, misattributing desktop events to mobile.

## User properties: separate segments

Properties that describe the user should use segments. Fullstory resolves user properties to their last known values for segment matching.

Examples include `signed_up`, `first_seen` / `last_seen`, `total_sessions`, and `user_var_*` custom properties set via `setUserProperties`.

```bash
fullstory segment build 'users whose current plan is enterprise'
fullstory segment build 'users whose current plan is free'
fullstory metric build single_number 'count application errors'
```

Compute the same metric once per segment, recording each result.

```bash
mcpc @fullstory tools-get compute_metric        # confirm the live parameter set
fullstory call compute_metric metric_id:=METRIC_ID segment_id:=SEGMENT_ID
```

Using a dimension for a user property answers an event-time question instead: a user who changes plans mid-period has events split across old and new values. Use this only when point-in-time attribution is intended.

## Decision table

| Axis | Type | Mechanism |
|---|---|---|
| Device, browser, OS | Event | `top_n` dimensionality |
| Page URL, element | Event | `top_n` dimensionality |
| `signed_up`, `first_seen` / `last_seen` | User | Separate segments |
| `total_sessions` | User | Separate segments |
| `user_var_*` set via `setUserProperties` | User | Separate segments |

If the property level remains unknown, prefer dimensionality because it uses fewer calls and provides precise event attribution. State the assumption.
