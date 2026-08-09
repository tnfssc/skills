# Setup, auth, and vendoring

## Installation

Official package: `langfuse-cli`, installed user-locally so `langfuse` lands on PATH without touching system npm directories:

```bash
npm install -g --prefix ~/.local langfuse-cli
langfuse --help
```

This repository does not wrap, fork, or reimplement the CLI.

## Credentials and project profiles

Langfuse API keys are project-scoped. Keep one mode-`600` env file per project under `~/.config/langfuse/`; use `env` for the default and `env.<short-project-slug>` for additional projects. The CLI reads `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and the host from either `LANGFUSE_HOST` or `LANGFUSE_BASE_URL`:

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-XXXX
LANGFUSE_SECRET_KEY=sk-lf-XXXX
LANGFUSE_HOST=https://langfuse.example.com
LANGFUSE_BASE_URL=https://langfuse.example.com
```

Both host names are set because the CLI takes either while the Langfuse SDKs read `LANGFUSE_BASE_URL` — so the same file works when sourced for application code.

The machine-local profile registry lives at `~/.config/langfuse/profiles.md`. Use it to map a Langfuse URL's `/project/<id>/` to the correct env file.

### Adding a project profile

1. Obtain that project's API key pair from Settings → API Keys; ask the user to provide it.
2. Verify once with `LANGFUSE_PUBLIC_KEY=… LANGFUSE_SECRET_KEY=… LANGFUSE_HOST=… langfuse api projects get-public`; confirm the returned project ID matches.
3. Write `~/.config/langfuse/env.<short-slug>` in the standard four-variable format above and set mode `600`.
4. Register the profile, project name, project ID, and env file in `~/.config/langfuse/profiles.md`.

```bash
langfuse --env ~/.config/langfuse/env api __schema
langfuse --env ~/.config/langfuse/env.<slug> api traces list --limit 5 --json
```

Keys are project-scoped and come from the project's Settings → API Keys. Never commit the env file, paste secret keys into chat, or pass keys as command-line flags. Rotate compromised keys in project settings.

## Vendored upstream skill

This skill vendors `skills/langfuse/` from [langfuse/skills](https://github.com/langfuse/skills) at commit `b9958d6c7b0df35a7f1df76a5f6c3a4505b0a3d3`, installed 2026-08-09. Upstream references are unchanged except normalized trailing whitespace; `SKILL.md` adds local frontmatter and the "Local setup" section above the upstream body; this setup file is local-only.

To refresh: diff that directory at a newer upstream commit, take the upstream content as-is, keep the local frontmatter and "Local setup" section in `SKILL.md`, and record the new commit here. `langfuse get-skill` prints upstream's current `SKILL.md` from `main`, which is a quick drift check but does not cover the references.

## Troubleshooting

```bash
command -v langfuse
npm list -g --prefix ~/.local --depth=0 langfuse-cli
langfuse --env ~/.config/langfuse/env api __schema
langfuse --env ~/.config/langfuse/env api traces --help
```

Authentication failure usually means wrong host/key pairing, expired or rotated keys, or keys from another project. Check presence and file permissions without printing values:

```bash
stat -f '%Sp %N' ~/.config/langfuse/env
sed -E 's/=.*/=<redacted>/' ~/.config/langfuse/env
```
