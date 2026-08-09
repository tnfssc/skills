# Workspace and libraries

## Projects

```bash
figma team projects TEAM_ID
figma project files PROJECT_ID
figma project files PROJECT_ID --branches
```

Figma REST API cannot discover team IDs programmatically. Copy team ID from Figma team URL. Projects endpoints require separate Figma approval and may return 403 even with valid PAT.

## Components and styles

```bash
figma components FILE_KEY
figma styles FILE_KEY
figma team components TEAM_ID --page-size 100 --after CURSOR
figma team styles TEAM_ID --page-size 100 --before CURSOR
```

File commands list published assets in one library file. Team commands paginate with `meta.cursor.before` / `meta.cursor.after`; feed cursor back through matching flag. Team library reads require appropriate plan, team permission, and token scope.

## Variables

```bash
figma variables FILE_KEY
```

Thin wrapper around `GET /v1/files/:file_key/variables/local`. Variables REST API requires Enterprise membership; writes additionally require Full seat and edit access. Use raw API only after explicit write request.
