# Live Fullstory MCP tool catalog

Source: [Fullstory MCP Tools Reference](https://developer.fullstory.com/mcp/tools-reference/), checked 2026-08-15.

Use `fullstory tools` for server-authoritative discovery and `fullstory call TOOL ...` for raw access.

## Agentic session review

| Tool | CLI |
|---|---|
| `session_open` | `fullstory session open DEVICE_ID SESSION_ID` |
| `session_screenshot` | `fullstory session screenshot CLIENT_ID PAGE_ID TIMESTAMP` |
| `session_get_a11y_tree` | `fullstory session tree CLIENT_ID PAGE_ID TIMESTAMP` |
| `session_diff` | `fullstory session diff CLIENT_ID PAGE_ID FROM_TS TO_TS` |
| `session_close` | `fullstory session close CLIENT_ID` |

`session_view` is deprecated and nonfunctional. Do not call it.

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
| `get_session_events` | `fullstory session events DEVICE_ID SESSION_ID` |
| `get_pages` | `fullstory pages [REGEX]` |

## StoryAI opportunities

Thin aliases accept raw `mcpc` argument syntax because live schemas can evolve:

| Tool | CLI |
|---|---|
| `discover_groups` | `fullstory opportunity discover [k:=v ...]` |
| `get_opportunity_stats` | `fullstory opportunity stats k:=v ...` |
| `classify_opportunity` | `fullstory opportunity classify k:=v ...` |
| `get_opportunities` | `fullstory opportunity list [k:=v ...]` |
| `get_opportunity` | `fullstory opportunity get k:=v ...` |
| `get_sessions_for_opportunity` | `fullstory opportunity sessions k:=v ...` |

`get_opportunities`, `get_opportunity`, and `get_sessions_for_opportunity` require StoryAI Premium according to current docs.
