---
title: "openclaw.ai"
categories:
  - script
  - openclaw.ai
date: 2026-02-04
---

OpenClaw is a CLI tool for terminal automation. This installer handles macOS and Linux (including WSL), installing Node.js 22+ if needed, and optionally Homebrew on macOS. It can install via npm (default) or from a git checkout. The script modifies shell configuration files, installs global npm packages, and may create wrapper scripts in `~/.local/bin`.

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `https://openclaw.ai/install.sh` |
| **Invocation** | `curl -fsSL https://openclaw.ai/install.sh \| bash` |
| **Total lines** | 1416 |
| **Comments** | 25 lines |
| **Blank** | 85 lines |
| **Boilerplate** | 350 lines (output formatting, colors, taglines, usage text) |
| **Installation** | 956 lines (actual work) |

## What does it change?

### Files and folders

- Creates `~/.openclaw/` directory for configuration and workspace
- Creates `~/.openclaw/openclaw.json` configuration file
- Creates `~/.npm-global/` directory on Linux if npm global prefix is not writable
- Creates `~/.local/bin/openclaw` wrapper script (when using git install method)
- Creates `~/openclaw/` directory (when using git install method)
- May backup existing `openclaw` binary to `<path>.bak-<timestamp>`

### Packages installed

- **Homebrew** (macOS only): Installed if not present, via `curl | bash` from GitHub
- **Node.js 22+**: Via Homebrew on macOS, or NodeSource repositories on Linux (apt/dnf/yum)
- **Git**: Via Homebrew on macOS or package manager on Linux
- **pnpm**: Via Corepack or npm (only for git install method)
- **openclaw**: The main package, installed globally via npm

### Downloads

- Homebrew install script from `raw.githubusercontent.com`
- NodeSource setup scripts from `deb.nodesource.com` or `rpm.nodesource.com` (Linux)
- OpenClaw repository from `github.com/openclaw/openclaw.git` (git method only)

### Environment changes

- Modifies `~/.bashrc` and `~/.zshrc` to add:
    - `$HOME/.npm-global/bin` to PATH (Linux, if npm permissions fixed)
    - `$HOME/.local/bin` to PATH (git install method)
- Sets npm global prefix to `~/.npm-global` on Linux if needed
- Evaluates Homebrew shellenv to add brew to PATH (macOS)

### Services

- May start/restart OpenClaw gateway daemon via `openclaw daemon restart`
- Runs `openclaw doctor` for migrations on upgrades
- Runs `openclaw onboard` for initial setup

### Permissions

- Uses admin permissions (sudo) on Linux for:
    - Installing Node.js via package manager
    - Installing Git via package manager
- Creates executable wrapper script at `~/.local/bin/openclaw`
- May remove/rename existing `openclaw` binaries in `/opt/homebrew/bin` or `/usr/local/bin`

## Notes

- The script downloads and executes the Homebrew installer script (another curl|bash)
- On Linux, it downloads and executes NodeSource setup scripts with admin permissions
- Existing `openclaw` binaries may be moved or deleted without explicit confirmation
- Shell configuration files are modified automatically

## Uninstall procedure

1. Remove the npm global package: `npm uninstall -g openclaw`
2. Remove configuration: `rm -rf ~/.openclaw`
3. Remove git checkout (if used): `rm -rf ~/openclaw`
4. Remove wrapper script: `rm -f ~/.local/bin/openclaw`
5. Remove npm global directory (if created): `rm -rf ~/.npm-global`
6. Edit `~/.bashrc` and `~/.zshrc` to remove PATH additions for `.npm-global/bin` and `.local/bin`

## Full source

The full script source is saved as [`scripts/openclaw_ai_install_sh.txt`](../../scripts/openclaw_ai_install_sh.txt).
