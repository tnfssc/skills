# Workspace and libraries

## Projects

```bash
figma team projects TEAM_ID
figma project files PROJECT_ID
figma project files PROJECT_ID --branches
```

There is no endpoint that lists the teams you belong to — take the team ID from a
Figma team URL (`figma.com/files/team/TEAM_ID/...`), then walk down to projects and
files. These endpoints need a paid plan and membership of the team, so a valid
token can still come back 403.

## Components and styles

```bash
figma components FILE_KEY
figma styles FILE_KEY
figma team components TEAM_ID --page-size 100 --after CURSOR
figma team styles TEAM_ID --page-size 100 --before CURSOR
```

The file commands list what one library file publishes; the team commands list a
whole team library and paginate — take `meta.cursor.after` / `meta.cursor.before`
from the response and feed it back through the matching flag.

## Variables

```bash
figma variables FILE_KEY
```

A thin wrapper around `GET /v1/files/:key/variables/local`. The Variables REST API
is Enterprise-only; reads need an Enterprise org member token, and writes (raw API
only) additionally need a Full seat and edit access to the file.
