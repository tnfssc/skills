# Comparisons

Adapted from upstream `skills/comparisons` at pinned commit in `setup.md`.

Comparison mechanism depends on axis.

## Event or session properties: dimensionality

If property describes context when event fired, use one `top_n` metric grouped by that property.

Examples: device type, browser, OS, page URL, element.

```bash
fullstory metric build top_n 'rage clicks grouped by device type'
```

Refine existing metric instead of rebuilding:

```bash
fullstory metric update METRIC_ID 'filter to Chrome only'
```

Do not use user segments for event properties. A user who used mobile once and later rage-clicked on desktop may qualify for both user cohorts, misattributing desktop events to mobile.

## User properties: separate segments

Properties describing user should use segments. Fullstory resolves user properties to last known value for segment matching.

Examples: signed-up status, first/last seen, total sessions, plan/account properties set as custom user properties.

```bash
fullstory segment build 'users whose current plan is enterprise'
fullstory segment build 'users whose current plan is free'
fullstory metric build single_number 'count application errors'
```

Attach each segment to metric, compute, record result, repeat. Inspect live `update_metric` schema before raw segment attachment:

```bash
mcpc @fullstory tools-get update_metric
fullstory call update_metric metric_id:=METRIC_ID segment_id:=SEGMENT_ID
fullstory metric compute METRIC_ID
```

Using a dimension for user property answers event-time question instead: user who changes plan mid-period has events split across old and new values. Use this only when point-in-time attribution is intended.

## Decision table

| Axis | Type | Mechanism |
|---|---|---|
| Device, browser, OS | Event | `top_n` dimensionality |
| Page URL, element | Event | `top_n` dimensionality |
| Signed-up, first/last seen | User | Separate segments |
| Total sessions | User | Separate segments |
| Custom user properties | User | Separate segments |

If property level remains unknown, prefer dimensionality: fewer calls and precise event attribution. State assumption.
