# Validating results

This guide was adapted from upstream `general-analysis/references/validation.md`.

Validate a result when it is zero, anomalous, discontinuous, or disputed. Normal-looking results need no extra calls; include the returned Fullstory URL for verification.

## Zero: always cross-check

1. Refine or rebuild without narrow page or element filters.
2. Expand the time window to `last_30_days` or `last_90_days`.
3. Compute a broad page-view metric to confirm that the organization has traffic.

> `metric update` and `segment update` persist a new object and return a **new** id. Compute the returned id, not the one you passed.

```bash
fullstory metric update METRIC_ID 'remove page and element filters'      # returns a NEW metric_id
fullstory metric compute NEW_METRIC_ID last_90_days
fullstory metric build single_number 'count all page views'
```

If broad traffic is also zero, there may be a collection, organization, permission, or time-window issue. Do not claim that the event is absent.

## Anomalies

Investigate rates above 100%, implausible counts, contradictions, or sharp discontinuities before presenting a conclusion.

Slice an established metric by dimension:

```bash
fullstory metric update METRIC_ID 'change to top_n grouped by page' top_n      # returns a NEW metric_id
fullstory metric compute NEW_METRIC_ID
```

For a sudden trend drop or spike, compare broad traffic over the same period. A traffic-wide discontinuity suggests a collection issue; a metric-only change may be real.

## Reporting

Do not narrate every successful check. Report validation details when they changed the result, exposed a data-quality issue, or require a user choice.
