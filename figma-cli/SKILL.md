---
name: figma-cli
description: Reference for the `figma` command — a standalone REST API CLI for reading Figma files, nodes, rendered screenshots, comments, versions, components, styles, projects, and team libraries, plus posting comments. Use for terminal-based Figma inspection, design metadata extraction, image export, library discovery, comment workflows, API setup/auth, or raw Figma REST API calls.
---

# figma-cli

`figma` (`~/.tnfssc-skills/figma-cli/bin/figma`) is a curl wrapper around Figma's REST API at `https://api.figma.com`. Requires `curl` + `jq` and a personal access token, from `FIGMA_TOKEN` or `~/.config/figma/token` — see `references/setup.md` if the command is missing or auth fails.

## Command areas

- **Files and nodes** — document JSON, sparse node queries, rendered screenshots. Details: `references/files.md`.
- **Collaboration and history** — comments, comment posting, versions. Details: `references/files.md`.
- **Libraries and workspace** — components, styles, team projects, project files. Details: `references/workspace.md`.
- **Everything else** — `figma api METHOD PATH ...` is a raw REST passthrough. Endpoint map: `references/api.md`.
- **Setup / auth / errors** — `references/setup.md`.

## Facts worth knowing

- A full Figma URL works anywhere a file key is accepted, and a URL's `node-id=1-23` is normalized to the REST form `1:23` — never hand-convert it.
- Output is plain JSON on stdout — pipe to `jq`. `-c` for compact, `--raw` to skip pretty-printing. `figma screenshot` prints the path of the file it wrote, never image bytes.
- There is no recent-files or search endpoint in the REST API. Every read starts from a file key, project ID, or team ID you already have — usually pasted from a Figma URL.
- 403 means plan, scope, or file permission at least as often as it means a bad token: team library and project endpoints need a paid plan and team membership, and the Variables API is Enterprise-only. The CLI only tells you to re-run `figma setup` when the failure really looks like auth.
- Reads are safe. `figma comment` writes to the file — confirm the target first. Every other write goes through raw `figma api`; check the endpoint's schema before firing one.
- Render URLs expire quickly, which is why `figma screenshot` downloads immediately and refuses to overwrite an existing file.
