# Live Fullstory MCP tool catalog

This catalog uses the [Fullstory MCP Tools Reference](https://developer.fullstory.com/mcp/tools-reference/), checked on 2026-08-15.

Use `fullstory tools` for server-authoritative discovery and `fullstory call TOOL ...` for raw access.

## Agentic session review

| Tool | CLI |
|---|---|
| `session_open` | `fullstory session open SESSION_ID` |
| `session_screenshot` | `fullstory session screenshot CLIENT_ID PAGE_ID TIMESTAMP` |
| `session_get_a11y_tree` | `fullstory session tree CLIENT_ID PAGE_ID TIMESTAMP` |
| `session_diff` | `fullstory session diff CLIENT_ID PAGE_ID FROM_TS TO_TS` |
| `session_close` | `fullstory session close CLIENT_ID` |

`session_view` is live but deprecated and nonfunctional. Use `session_screenshot` and `session_get_a11y_tree` instead.

## Analytics

| Tool | CLI family |
|---|---|
| `build_segment`, `update_segment`, `get_segment` | `fullstory segment ...` |
| `build_metric`, `update_metric`, `compute_metric`, `get_metric` | `fullstory metric ...` |
| `build_funnel`, `get_funnel`, `compute_funnel`, `get_funnel_sessions` | `fullstory funnel ...` |

## Sessions and pages

| Tool | CLI |
|---|---|
| `get_sessions` | `fullstory sessions --metric ID` or `--segment ID` |
| `get_session_events` | `fullstory session events SESSION_ID` |
| `get_pages` | `fullstory pages [REGEX]` |

## StoryAI opportunities

Use the raw passthrough for opportunity tools because their live schemas can evolve:

| Tool | CLI |
|---|---|
| `discover_groups` | `fullstory call discover_groups k:=v ...` |
| `get_opportunity_stats` | `fullstory call get_opportunity_stats k:=v ...` |
| `get_opportunities` | `fullstory call get_opportunities k:=v ...` |
| `get_opportunity` | `fullstory call get_opportunity k:=v ...` |
| `get_sessions_for_opportunity` | `fullstory call get_sessions_for_opportunity k:=v ...` |

`get_opportunities`, `get_opportunity`, and `get_sessions_for_opportunity` require StoryAI Premium according to current docs.

## Additional live tools

| Tool | CLI |
|---|---|
| `build_journey` | `fullstory call build_journey k:=v ...` |
| `compute_journey` | `fullstory call compute_journey k:=v ...` |
| `get_journey` | `fullstory call get_journey k:=v ...` |
| `discover_org_context` | `fullstory call discover_org_context k:=v ...` |
| `get_managed_funnels` | `fullstory call get_managed_funnels` |
| `get_view_counts` | `fullstory call get_view_counts k:=v ...` |
| `update_funnel` | `fullstory call update_funnel k:=v ...` |
| `update_journey` | `fullstory call update_journey k:=v ...` |
