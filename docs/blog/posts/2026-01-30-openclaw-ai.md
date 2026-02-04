---
title: "openclaw.ai/install.sh"
slug: openclaw
categories:
  - openclaw.ai
  - script
date: 2026-01-31
---

The OpenClaw installer at `openclaw.ai/install.sh` sets up the OpenClaw CLI tool on macOS and Linux (including WSL). Invoked via `curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash`, it installs prerequisites (Homebrew, Node.js 22, Git), then installs OpenClaw either globally via npm or from a git checkout. The script is notably large — roughly a quarter of its 1416 lines are tagline jokes and color formatting.

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `https://openclaw.ai/install.sh` |
| **Invocation** | `curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh \| bash` |
| **Total lines** | 1416 |
| **Comments** | 30 lines |
| **Blank** | 138 lines |
| **Boilerplate** | 353 lines (output formatting, colors, taglines, usage text) |
| **Installation** | 894 lines (actual work) |

## What does it change?

### Files and folders

- Creates `$HOME/.local/bin/openclaw` wrapper script (git install method)
- Creates `$HOME/.npm-global/` directory for npm prefix on Linux
- Creates/uses `$HOME/.openclaw/` for configuration and workspace data
- Appends PATH export lines to `$HOME/.bashrc` and `$HOME/.zshrc`

### Packages installed

- **Homebrew** (macOS only, if not already present)
- **Node.js 22** via `brew install node@22` (macOS) or NodeSource setup script (Linux: apt-get, dnf, or yum)
- **Git** via brew (macOS) or apt-get/dnf/yum (Linux)
- **pnpm** via Corepack or npm (git install method only)
- **OpenClaw** itself via `npm install -g openclaw` (npm method) or `git clone` + `pnpm build` (git method)

### Downloads

- Homebrew installer from `https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh`
- NodeSource setup from `https://deb.nodesource.com/setup_22.x` or `https://rpm.nodesource.com/setup_22.x`
- OpenClaw repo from `https://github.com/openclaw/openclaw.git` (git method)

### Environment changes

- Modifies `PATH` at runtime to include npm global bin dir, `$HOME/.npm-global/bin`, and `$HOME/.local/bin`
- Sets `npm config prefix` to `$HOME/.npm-global` on Linux when the default prefix isn't writable
- Persists PATH changes by appending export lines to `.bashrc` and `.zshrc`

### Services

- Detects and restarts the OpenClaw gateway daemon if already loaded (`openclaw daemon restart`)

### Permissions

- Uses `sudo` for Linux system package installs (apt-get, dnf, yum)
- Runs `chmod +x` on the `$HOME/.local/bin/openclaw` wrapper script

## Full source

The full script source is saved as [`scripts/openclaw_ai_install_sh.txt`](../../scripts/openclaw_ai_install_sh.txt).
