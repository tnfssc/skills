# Fullstory analytics

This guide was adapted from `skills/general-analysis` in `fullstorydev/fullstory-skills` at the pinned commit in `setup.md`.

## Mental model

- A **segment** is a cohort of users: the who. It is a filter, not a measurement.
- A **metric** is the measurement: what happened and how much.
- A **session** is qualitative evidence: the why. Never use session samples to answer quantitative questions.
- A **funnel** is an ordered sequence of steps completed in the same session by the same user.

## 1. Classify intent

- A count, percentage, or rate requires a `single_number` metric.
- A top-N list or breakdown by browser or page requires a `top_n` metric.
- A trend or change over time requires a `trend` metric.
- An A-versus-B question requires the guidance in `comparisons.md`.
- A request for matching sessions requires a metric or segment, followed by `fullstory sessions`.
- An ordered conversion or drop-off question requires a funnel.

Clarify an ambiguous unit, such as users versus accounts, a page path versus a full URL, or a current user property versus an event-time property.

## 2. Search before building

Users may not know which saved objects already exist.

```bash
fullstory metric get 'checkout'
fullstory segment get 'enterprise'
fullstory funnel get 'signup'
```

Judge matches by their definitions, not only their names. If multiple plausible objects exist, present the choices and definitions. Do not silently build duplicates. If nothing matches, say so before creating a persisted object.

## 3. Build or refine

Build metrics with the output type that matches the question:

```bash
fullstory metric build single_number 'count rage clicks on checkout'
fullstory metric build top_n 'rage clicks grouped by browser'
fullstory metric build trend 'daily checkout errors'
```

For `top_n`, the query must state the grouping dimension. The builder will not invent one.

Refine an established metric instead of rebuilding it:

```bash
fullstory metric update METRIC_ID 'filter to Chrome only'      # returns a NEW metric_id
fullstory metric update METRIC_ID 'show as a daily trend' trend
```

> `metric update` and `segment update` persist a new object and return a **new** id. Compute the returned id, not the one you passed.

`update_metric` does not support ratio metrics — rebuild those with `metric build`.

Build segments for user cohorts:

```bash
fullstory segment build 'enterprise users active in last 30 days'
fullstory segment update '{...segment definition...}' 'exclude trial users'
```

Reuse returned IDs within the conversation.

Build funnels for ordered sequences:

```bash
fullstory funnel build 'signup page view then account created then onboarding completed'
fullstory funnel compute FUNNEL_ID
fullstory funnel sessions FUNNEL_ID 1 --dropoffs
```

`COMPLETED_STEP` is zero-indexed. The saved funnel time range controls computation.

## 4. Compute metrics

```bash
fullstory metric compute METRIC_ID
fullstory metric compute METRIC_ID last_30_days
```

Default to `last_30_days` when the user gives no window. Ask before choosing another window. For cohort scoping, confirm the live computation schema and use the raw call:

```bash
mcpc @fullstory tools-get compute_metric        # confirm the live parameter set
fullstory call compute_metric metric_id:=METRIC_ID segment_id:=SEGMENT_ID
```

Present the exact value, time window, grouping dimension, and returned Fullstory URL.

## 5. Investigate sessions

After an aggregate result identifies a behavior:

```bash
fullstory sessions --metric METRIC_ID
fullstory sessions --segment SEGMENT_ID
```

Start with 3–5 sessions. Read `sessions.md` before fetching transcripts. Use session evidence to explain patterns, not to estimate prevalence.

## Guidelines

- Search before building.
- Keep the measurement unit explicit.
- Reuse metric, segment, and funnel IDs.
- Include the dimension value and count in tables; include a percentage when a total exists.
- Surface the Fullstory verification URL as soon as it is returned.
- Validate zero, anomalous, or disputed results using `validation.md`.
