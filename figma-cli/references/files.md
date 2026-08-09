# Files, nodes, images, comments, versions

## Files and nodes

```bash
figma file https://www.figma.com/design/FILE_KEY/Example --depth 2
figma file FILE_KEY --meta
figma file FILE_KEY --geometry
figma nodes 'https://www.figma.com/design/FILE_KEY/Example?node-id=1-23'
figma nodes FILE_KEY 1:23 4-56 --depth 2
```

`figma file` calls `GET /v1/files/:key`; `--meta` uses lightweight `/meta` endpoint. `figma nodes` calls `GET /v1/files/:key/nodes`. Full URLs supply file key and optional node ID. Bare hyphen node IDs normalize to colon form.

## Screenshots

```bash
figma screenshot 'https://www.figma.com/design/FILE_KEY/Example?node-id=1-23' -o frame.png
figma screenshot FILE_KEY 1:23 --format svg --scale 2 -o frame.svg
```

Supported formats: `png`, `jpg`, `svg`, `pdf`; scale range: `0.01` to `4`. Command requests render URL, downloads it immediately, then prints output path. Image-map entry can be null when node cannot render.
Existing output files are never overwritten.

## Comments

```bash
figma comments FILE_KEY
figma comment 'https://www.figma.com/design/FILE_KEY/Example?node-id=1-23' 'Looks ready for review.'
```

`figma comment` is write operation. Confirm target and intent before running. Delete comment only through raw API after verifying exact comment ID:

```bash
figma api DELETE /v1/files/FILE_KEY/comments/COMMENT_ID
```

## Versions

```bash
figma versions FILE_KEY
figma versions FILE_KEY --page 'https://api.figma.com/v1/files/FILE_KEY/versions?before=CURSOR'
```

Response exposes `pagination.next_page` and `pagination.prev_page`; pass returned URL through `--page` unchanged.
