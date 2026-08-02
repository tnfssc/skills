---
name: work-summary
description: Builds a concise Slack-ready work summary from Slack context and verified GitHub activity. Use for daily/weekly updates, "what did I work on", standup notes, or a condensed report over any timeframe. Defaults to the last 1 day when no timeframe is given.
---

# Work summary

Combines Slack activity (via a handoff prompt, since the agent has no direct Slack access) with GitHub activity (verified via `gh`) into a short, Slack-formatted update. Goal: product outcomes, not an activity ledger.

## Timeframe

Default: last 1 day (24h through now). Accepts custom windows — `last 12 hours`, `yesterday`, `this week`, `since Monday`, explicit dates/ranges. Interpret relative times in `Asia/Dubai` unless told otherwise; ask for clarification if the window is ambiguous.

## Slack context

The agent can't read Slack directly. When no Slack summary is supplied and a GitHub-only update wasn't requested, hand off this prompt (with the window filled in) for the user to run through their Slack bot and paste back:

```text
Give me a complete summary of work I materially contributed on Slack during [WINDOW] in [TIMEZONE].

Search all channels, group DMs, DMs, threads, and replies I can access. Include problems investigated/resolved, implementation decisions, PRs/tickets/incidents discussed, blockers raised or unblocked, meaningful review feedback, coordination that changed ownership/priority/scope, and work shared or handed off.

Exclude greetings, routine status replies, duplicate thread messages, and conversations with no material contribution.

For each outcome give: summary, status, channel/DM, message link, related ticket/PR ids, and people involved when relevant. Be exhaustive — I'll combine this with GitHub activity.
```

## GitHub collection

Identify the user with `gh api user` rather than assuming identity. Gather, for the window: authored PRs (created/merged/closed/updated) and reviews submitted (verify actual submission time, not just PR `updated_at`), plus other events (pushes, comments, older PRs merged) via the events API — supplement with Search/PR-review APIs since events pagination is capped. Verify current PR status/title/ticket id/merge state directly from GitHub; treat Slack-sourced status as a lead, not ground truth.

## What to report

Collect exhaustively, publish selectively: combine related commits/PRs/discussions into one outcome per line, favor shipped work, production fixes, direction-changing decisions, and high-signal reviews; skip routine pushes, duplicate comments, and untouched assignments. Distinguish completed from in-progress/proposed/reviewed work, and authored from reviewed work. Never invent ticket ids or infer resolution from discussion alone.

## Output

Plain, paste-ready Slack text — bold headings, plain bullets, no emojis, no em/en dashes, no preamble unless audit detail is requested. Group into 2-4 short headings only when useful; use one heading if the work is cohesive. Aim for roughly 6-10 lines total. Start each line with a plain state verb (Merged, Shipped, Pushed, Investigated, Reviewed, Coordinated, Shared, Scheduled...) and append known ticket/PR ids.

Example:

```text
*Checkout and billing*

- Merged retry logic and timeout fixes for the payment webhook. `PROJ-1201`
- Continued rate-limit handling for the invoice export job. `PROJ-1214`
- Shared a proposal for splitting the billing worker into two queues.

*Onboarding flow*

- Merged step-order fix and validation cleanup. `PROJ-1188`, `PROJ-1190`
- Reviewed the new email-verification PR, flagged a race condition.
```
