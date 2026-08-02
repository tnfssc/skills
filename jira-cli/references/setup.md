# Setup / auth / troubleshooting

Only relevant for install, init, auth, config, or "command not found" — normal ticket work doesn't need this.

```sh
command -v jira && jira version && jira me && jira serverinfo
```

Never print tokens, passwords, `.netrc`, or full config contents.

Config default: `~/.config/.jira/.config.yml`. Override with `-c path` or `JIRA_CONFIG_FILE=path`.

## Install

```sh
brew install ankitpokhrel/jira-cli/jira-cli
docker run -it --rm ghcr.io/ankitpokhrel/jira-cli:latest
jira version   # not --version
```

## Auth

Cloud:

```sh
export JIRA_API_TOKEN='...'   # Atlassian API token
jira init                      # choose Cloud, enter server/user/project
```

Server/Data Center uses the same `jira init` flow — basic auth by default; PAT/bearer needs `JIRA_AUTH_TYPE=bearer`; mTLS is configured interactively (`jira init` → Local → mTLS, with CA/client cert/key).

## Multiple projects/configs

```sh
JIRA_CONFIG_FILE=./local.yaml jira issue list
jira issue list -c ./local.yaml
jira issue list -p ABC
```

## Troubleshooting

- `command not found` — check install/PATH; a new shell may be needed.
- 401/auth failure — confirm `JIRA_API_TOKEN` is set in-shell; Cloud needs an API token not a password; Server PAT often needs `JIRA_AUTH_TYPE=bearer`; re-run `jira init` if server/user/project changed.
- Wrong project — `jira project list`, then `-p KEY` or a separate config.
- Shell completion — `jira completion zsh|bash`.
