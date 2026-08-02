# [tnfssc/skills](.)

Personal collection of agent skills.

## Install

Agent skill loaders (opencode, Claude Code, …) auto-discover **one level deep**: `<skills-dir>/<name>/SKILL.md`. So each skill folder must sit directly under `~/.agents/skills/` (or `.agents/skills/`), not nested under a namespace.

**Clone + symlink each skill in** (safe when the skills dir is already populated — adds these skills without touching others).

Fish:

```fish
git clone https://github.com/tnfssc/skills.git ~/.tnfssc-skills
mkdir -p ~/.agents/skills
for d in ~/.tnfssc-skills/*/
    test -f "$d/SKILL.md"; and ln -sfn "$d" ~/.agents/skills/
end
```

Bash/POSIX:

```sh
git clone https://github.com/tnfssc/skills.git ~/.tnfssc-skills
mkdir -p ~/.agents/skills
for d in ~/.tnfssc-skills/*/; do [ -f "$d/SKILL.md" ] && ln -sfn "$d" ~/.agents/skills/; done
```

Project-local — same loop using `.tnfssc-skills` and `.agents/skills` in the current project. Update later with `git pull -C ~/.tnfssc-skills` (symlinks stay live). Remove with `rm -rf ~/.tnfssc-skills` plus `rm ~/.agents/skills/cua-driver ~/.agents/skills/host-sharath …`.

If the skills dir is empty/dedicated, you can skip symlinking and clone directly: `git clone https://github.com/tnfssc/skills.git ~/.agents/skills`.

## Skills

| Skill | Description | Source |
|-------|-------------|--------|
| [cua-driver](cua-driver/) | Drive native GUI apps (snapshot AX tree, click/type/scroll, verify) via the cua-driver CLI/MCP | [trycua/cua](https://github.com/trycua/cua) |
| [host-sharath](host-sharath/) | Upload files to host.sharath.page for expiring, authenticated share links | [host.sharath.page](https://host.sharath.page) |
| [jira-cli](jira-cli/) | Work with Jira issues, sprints, boards, projects, and JQL using the `jira` CLI | Local zip |
| [mcpc](mcpc/) | Shell CLI for MCP servers — connect, list/call tools, read resources, async tasks | [apify/mcpc](https://github.com/apify/mcpc) |
| [open-browser-use](open-browser-use/) | Guidance for installing, verifying, troubleshooting, and operating Open Browser Use | Local zip |
| [work-summary](work-summary/) | Build concise Slack-ready work summaries for custom timeframes, defaulting to the last 1 day | Local zip |
