# Files, nodes, images, comments, versions

## Files and nodes

```bash
figma file 'https://www.figma.com/design/FILE_KEY/Example' --depth 2   # top levels only
figma file FILE_KEY --meta                                             # name/owner/version, no document
figma file FILE_KEY --version VERSION_ID                               # an older version
figma file FILE_KEY --branches                                         # + branch metadata
figma nodes 'https://www.figma.com/design/FILE_KEY/Example?node-id=1-23'
figma nodes FILE_KEY 1:23 4-56 --depth 2
```

`figma file` is `GET /v1/files/:key` (`--meta` is the much cheaper `/meta`
variant); `figma nodes` is `GET /v1/files/:key/nodes`. A whole design file is
easily megabytes of JSON, so reach for `figma nodes` or `--depth` before
fetching the document. `--geometry` adds vector path data.

A full Figma URL supplies both the file key and, when it carries `node-id`, the
node — so `figma nodes URL` needs no other argument. Node IDs are accepted in
either URL form (`1-23`) or REST form (`1:23`).

## Screenshots

```bash
figma screenshot 'https://www.figma.com/design/FILE_KEY/Example?node-id=1-23' -o frame.png
figma screenshot FILE_KEY 1:23 --format svg --scale 2 -o frame.svg
```

Formats: `png`, `jpg`, `svg`, `pdf`; `--scale` runs from `0.01` to `4`. The
command asks Figma to render, downloads the (short-lived) render URL immediately,
and prints the path it wrote. It refuses to overwrite an existing file. A node
that cannot be rendered comes back as a null entry in the image map, which
surfaces as `render returned no image URL`.

## Comments

```bash
figma comments FILE_KEY
figma comment 'https://www.figma.com/design/FILE_KEY/Example?node-id=1-23' 'Looks ready for review.'
```

`figma comment` is a write — confirm the file and the wording before running it.
Given a node (from `--node` or the URL) the comment is pinned to that node,
otherwise it lands on the file. Deleting a comment has no subcommand; do it
through the raw API once you have verified the comment ID:

```bash
figma api DELETE /v1/files/FILE_KEY/comments/COMMENT_ID
```

## Versions

```bash
figma versions FILE_KEY
figma versions FILE_KEY --page 'https://api.figma.com/v1/files/FILE_KEY/versions?before=CURSOR'
```

The response carries `pagination.next_page` and `pagination.prev_page`; pass one
of those URLs back through `--page` unchanged.
