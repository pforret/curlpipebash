---
title: "Script: openclaw.ai"
categories:
  - Analysis
date: 2026-01-30
---

The OpenClaw installer at `openclaw.ai/install.sh` is a 1407-line bash script that sets up the OpenClaw CLI tool on macOS and Linux (including WSL). It is invoked via `curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash`. The script installs prerequisites (Homebrew on macOS, Node.js 22+, Git), then installs OpenClaw either globally via npm or from a git checkout, configures PATH, and optionally runs onboarding and migration steps.

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `https://openclaw.ai/install.sh` |
| **Invocation** | `curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh \| bash` |
| **Total lines** | 1407 |
| **Comments** | 30 lines |
| **Blank** | 138 lines |
| **Boilerplate** | 242 lines (output formatting, colors, usage text) |
| **Installation** | 996 lines (actual work) |

## What does it change?

### Files and folders

- Creates `~/.npm-global/` directory on Linux if npm prefix is not user-writable
- Creates `~/.local/bin/` directory and writes an `openclaw` wrapper script there (git install method)
- Creates `~/.openclaw/` config directory (via the `openclaw onboard` / `openclaw doctor` subcommands)
- Clones the OpenClaw repo to `~/openclaw` (or a specified directory) when using the git install method
- Writes to `~/.bashrc` and `~/.zshrc` to add PATH entries for `~/.npm-global/bin` and/or `~/.local/bin`

### Packages installed

- **Homebrew** (macOS): installs Homebrew itself if missing, by downloading and running `https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh`
- **Node.js 22** (macOS): `brew install node@22`
- **Node.js 22** (Linux): downloads and runs the NodeSource setup script (`https://deb.nodesource.com/setup_22.x` or `https://rpm.nodesource.com/setup_22.x`), then installs via `apt-get`, `dnf`, or `yum`
- **Git**: `brew install git` (macOS) or `apt-get install -y git` / `dnf install -y git` / `yum install -y git` (Linux)
- **pnpm** (git method only): installed via Corepack or `npm install -g pnpm@10`
- **OpenClaw** itself: `npm install -g openclaw@latest` (npm method) or `pnpm install` + `pnpm build` in the git checkout (git method)

### Downloads

- Homebrew install script from `https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh` (macOS, if Homebrew is missing)
- NodeSource setup scripts from `https://deb.nodesource.com/setup_22.x` or `https://rpm.nodesource.com/setup_22.x` (Linux, if Node.js is missing)
- OpenClaw git repo from `https://github.com/openclaw/openclaw.git` (git install method)
- OpenClaw npm package from the npm registry (npm install method)

### Environment changes

- Adds `~/.npm-global/bin` to PATH in `~/.bashrc` and `~/.zshrc` (Linux, when fixing npm permissions)
- Adds `~/.local/bin` to PATH in `~/.bashrc` and `~/.zshrc` (git install method)
- Exports modified PATH within the current session for Homebrew shellenv, npm global bin, and user-local bin
- Sets `npm config set prefix "$HOME/.npm-global"` on Linux when the default prefix is not user-writable
- Runs `openclaw onboard` and `openclaw doctor` which may create or modify OpenClaw configuration files

### Permissions

- Uses `sudo` on Linux for system-level package installs (NodeSource setup, apt-get/dnf/yum)
- Runs `chmod +x` on the `~/.local/bin/openclaw` wrapper script (git install method)
- Creates symlinks in the npm global bin directory to the OpenClaw entry point

## Full source

The full script source is saved as [`scripts/openclaw_ai_install_sh.txt`](../../scripts/openclaw_ai_install_sh.txt).
