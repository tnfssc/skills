# Fullstory analytics

Adapted from `skills/general-analysis` in `fullstorydev/fullstory-skills` at pinned commit in `setup.md`.

## Mental model

- **Segment** = cohort of users: who. Filter, not measurement.
- **Metric** = measurement: what and how much.
- **Session** = qualitative evidence: why. Never use session samples to answer quantitative questions.
- **Funnel** = ordered steps completed in same session by same user.

## 1. Classify intent

- Count, percentage, rate → `single_number` metric.
- Top N, breakdown, by browser/page → `top_n` metric.
- Trend, over time, getting worse → `trend` metric.
- A versus B → read `comparisons.md`.
- Show matching sessions → metric or segment, then `fullstory sessions`.
- Ordered conversion/drop-off → funnel.

Clarify ambiguous unit: users versus accounts, page path versus full URL, current user property versus event-time property.

## 2. Search before building

Users may not know saved objects already exist.

```bash
fullstory metric get 'checkout'
fullstory segment get 'enterprise'
fullstory funnel get 'signup'
```

Judge matches by definition, not name. If multiple plausible objects exist, present choices and definitions. Do not silently build duplicates. If nothing matches, say so before creating a persisted object.

## 3. Build or refine

Metrics:

```bash
fullstory metric build single_number 'count rage clicks on checkout'
fullstory metric build top_n 'rage clicks grouped by browser'
fullstory metric build trend 'daily checkout errors'
```

For `top_n`, query must state grouping dimension. Builder will not invent one.

Refine established metric instead of rebuilding:

```bash
fullstory metric update METRIC_ID 'filter to Chrome only'
fullstory metric update METRIC_ID 'show as a daily trend' trend
```

Ratio metrics may need rebuilding because upstream says `update_metric` does not support them.

Segments:

```bash
fullstory segment build 'enterprise users active in last 30 days'
fullstory segment update '{...segment definition...}' 'exclude trial users'
```

Reuse returned IDs within conversation.

Funnels:

```bash
fullstory funnel build 'signup page view then account created then onboarding completed'
fullstory funnel compute FUNNEL_ID
fullstory funnel sessions FUNNEL_ID 1 --dropoffs
```

`COMPLETED_STEP` is zero-indexed. Saved funnel time range controls computation.

## 4. Compute metrics

```bash
fullstory metric compute METRIC_ID
fullstory metric compute METRIC_ID last_30_days
```

Default to `last_30_days` when user gave no window. Ask before choosing another window. If cohort scoping needs a segment attachment not covered by friendly syntax, inspect schema then use raw call:

```bash
mcpc @fullstory tools-get update_metric
fullstory call update_metric metric_id:=METRIC_ID segment_id:=SEGMENT_ID
fullstory metric compute METRIC_ID
```

Present exact value, time window, grouping dimension, and returned Fullstory URL.

## 5. Investigate sessions

After aggregate result identifies behavior:

```bash
fullstory sessions --metric METRIC_ID
fullstory sessions --segment SEGMENT_ID
```

Start with 3–5 sessions. Read `sessions.md` before fetching transcripts. Use session evidence to explain patterns, not estimate prevalence.

## Guidelines

- Search before build.
- Keep measurement unit explicit.
- Reuse metric, segment, and funnel IDs.
- Include dimension value plus count in tables; include percentage when total exists.
- Surface Fullstory verification URL as soon as returned.
- Validate zero, anomalous, or disputed results using `validation.md`.
