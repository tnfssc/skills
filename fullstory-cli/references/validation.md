# Validating results

Adapted from upstream `general-analysis/references/validation.md`.

Validate when result is zero, anomalous, discontinuous, or disputed. Normal-looking results need no extra calls; include returned Fullstory URL for verification.

## Zero: always cross-check

1. Refine or rebuild without narrow page/element filters.
2. Expand time window to `last_30_days` or `last_90_days`.
3. Compute broad page-view metric to confirm org has traffic.

```bash
fullstory metric update METRIC_ID 'remove page and element filters'
fullstory metric compute METRIC_ID last_90_days
fullstory metric build single_number 'count all page views'
```

If broad traffic is also zero, possible collection, org, permission, or time-window issue. Do not claim event absence.

## Anomalies

Investigate rates above 100%, implausible counts, contradictions, or sharp discontinuities before presenting conclusion.

Slice established metric by dimension:

```bash
fullstory metric update METRIC_ID 'change to top_n grouped by page' top_n
fullstory metric compute METRIC_ID
```

For sudden trend drop or spike, compare broad traffic over same period. Traffic-wide discontinuity suggests collection issue; metric-only change may be real.

## Reporting

Do not narrate every successful check. Report validation detail when it changed result, exposed data-quality issue, or requires user choice.
