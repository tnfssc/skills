---
name: figma-cli
description: Reference for the `figma` command — a standalone REST API CLI for reading Figma files, nodes, rendered screenshots, comments, versions, components, styles, projects, and team libraries, plus posting comments. Use for terminal-based Figma inspection, design metadata extraction, image export, library discovery, comment workflows, API setup/auth, or raw Figma REST API calls.
---

# figma-cli

`figma` (`~/.tnfssc-skills/figma-cli/bin/figma`) calls Figma REST API at `https://api.figma.com`. Requires `curl` + `jq` and personal access token from `FIGMA_TOKEN` or `~/.config/figma/token`. Run `figma setup` when command is missing or authentication fails; see `references/setup.md`.

## Command areas

- **Files and nodes** — document JSON, sparse node queries, URL parsing, rendered screenshots. Details: `references/files.md`.
- **Collaboration and history** — comments, safe comment posting, versions. Details: `references/files.md`.
- **Libraries and workspace** — components, styles, team projects, project files, cursors, plan gates. Details: `references/workspace.md`.
- **Everything else** — `figma api METHOD PATH ...` raw REST passthrough. Catalog: `references/api.md`.
- **Setup / auth / errors** — `references/setup.md`.

## Facts worth knowing

- Full Figma URLs work anywhere file key is accepted. URL `node-id=1-23` becomes REST node ID `1:23`.
- Output is plain JSON; `-c` compacts and `--raw` skips `jq` formatting. Screenshot outputs file path, never image bytes or base64.
- REST API has no general recent-files/search endpoint. Discover files through known team/project IDs or start from copied Figma URL.
- Project listing needs Figma approval. Variables API needs Enterprise plan; 403 can mean plan, scope, or file permission, not invalid token.
- Read commands are safe. `figma comment` writes to file. Other writes require raw `figma api`; inspect endpoint docs and confirm intent first.
- Render URLs expire. `figma screenshot` downloads immediately to local file.
