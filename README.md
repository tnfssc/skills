<p align="center">
  <img src="public/logo.svg" alt="tnfssc/skills" width="88" height="88">
</p>

<h1 align="center"><a href=".">tnfssc/skills</a></h1>

<p align="center">Personal collection of agent skills.</p>

## Install

Agent skill loaders auto-discover **one level deep**: `<skills-dir>/<name>/SKILL.md`. Skills are linked into both `~/.agents/skills/` for Agent Skills-compatible tools and `~/.claude/skills/` for Claude Code.

**Clone + symlink each skill in** (safe when the skills dir is already populated — adds these skills without touching others).

Fish:

```fish
git clone https://github.com/tnfssc/skills.git ~/.tnfssc-skills
mkdir -p ~/.agents/skills ~/.claude/skills
for d in ~/.tnfssc-skills/*/
    if test -f "$d/SKILL.md"
        ln -sfn "$d" ~/.agents/skills/
        ln -sfn "$d" ~/.claude/skills/
    end
end
```

Bash/POSIX:

```sh
git clone https://github.com/tnfssc/skills.git ~/.tnfssc-skills
mkdir -p ~/.agents/skills ~/.claude/skills
for d in ~/.tnfssc-skills/*/; do [ -f "$d/SKILL.md" ] || continue; ln -sfn "$d" ~/.agents/skills/; ln -sfn "$d" ~/.claude/skills/; done
```

Project-local — use the same loop with `.tnfssc-skills`, `.agents/skills`, and `.claude/skills` inside the project.

## Update

```sh
sh -c 'git -C "$HOME/.tnfssc-skills" pull --ff-only && mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills" && for d in "$HOME"/.tnfssc-skills/*/; do [ -f "$d/SKILL.md" ] || continue; ln -sfn "$d" "$HOME/.agents/skills/"; ln -sfn "$d" "$HOME/.claude/skills/"; done'
```

## Skills

| Skill | Description | Source |
|-------|-------------|--------|
| [cua-driver](cua-driver/) | Drive native GUI apps (snapshot AX tree, click/type/scroll, verify) via the cua-driver CLI/MCP | [trycua/cua](https://github.com/trycua/cua) |
| [figma-cli](figma-cli/) | Read Figma files, nodes, screenshots, comments, and team libraries via the bundled `figma` CLI | [Figma REST API](https://www.figma.com/developers/api) |
| [fullstory-cli](fullstory-cli/) | Analyze behavior, funnels, opportunities, and sessions via the bundled mcpc-backed `fullstory` CLI | [Fullstory MCP](https://developer.fullstory.com/mcp/) |
| [gcx](gcx/) | Manage Grafana Cloud resources through the unified `gcx` CLI | [grafana/gcx](https://github.com/grafana/gcx) |
| [hallmark](hallmark/) | Design and audit interfaces with an anti-AI-slop visual discipline | [nutlope/hallmark](https://github.com/nutlope/hallmark) |
| [host-sharath](host-sharath/) | Upload files to host.sharath.page for expiring, authenticated share links | [host.sharath.page](https://host.sharath.page) |
| [jira-cli](jira-cli/) | Work with Jira issues, sprints, boards, projects, and JQL using the `jira` CLI | Local zip |
| [langfuse-cli](langfuse-cli/) | Instrument, debug, and evaluate LLM apps with Langfuse — traces, prompts, datasets, and scores via the `langfuse` CLI | [langfuse/skills](https://github.com/langfuse/skills) |
| [linear-cli](linear-cli/) | Work with Linear issues, projects, cycles, and docs via the bundled mcpc-backed `linear` CLI | [Linear MCP](https://linear.app/docs/mcp) |
| [mcpc](mcpc/) | Shell CLI for MCP servers — connect, list/call tools, read resources, async tasks | [apify/mcpc](https://github.com/apify/mcpc) |
| [open-browser-use](open-browser-use/) | Guidance for installing, verifying, troubleshooting, and operating Open Browser Use | Local zip |
| [statsig-cli](statsig-cli/) | Manage Statsig feature gates, dynamic configs, segments, and experiments with the `siggy` CLI | [Statsig CLI](https://docs.statsig.com/statsigcli/introduction) |
| [work-summary](work-summary/) | Build concise Slack-ready work summaries for custom timeframes, defaulting to the last 1 day | Local zip |
