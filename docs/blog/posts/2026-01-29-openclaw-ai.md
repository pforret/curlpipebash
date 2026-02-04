---
title: "OpenClaw"
slug: openclaw
image: "/images/openclaw-ai.jpg"
categories:
  - script
  - openclaw.ai
date: 2026-01-29
---

Ever wished you had a lobster-themed CLI assistant that could automate your terminal chores? OpenClaw is exactly that — a chat-powered automation tool that installs itself with a single `curl | bash` command. This 1400+ line script handles everything from checking your Node.js version to installing Homebrew on macOS, setting up npm permissions on Linux, and even cracking jokes about your deployment anxiety.

![openclaw-ai](../../images/openclaw-ai.jpg)

<!-- more -->

## Script info

|                  |                                                                    |
|------------------|--------------------------------------------------------------------|
| **URL**          | `https://openclaw.ai/install.sh`                                   |
| **Invocation**   | `curl -fsSL https://openclaw.ai/install.sh | bash`                 |
| **Total lines**  | 1416                                                               |
| **Comments**     | 15 lines                                                           |
| **Blank**        | 50 lines                                                           |
| **Boilerplate**  | ~350 lines (color codes, taglines, usage text, completion messages) |
| **Installation** | ~1000 lines (actual work)                                          |

## What does it change?

This is a comprehensive installer that can make quite a few changes to your system. Let's walk through what it does — and don't worry, most of it is pretty standard stuff for CLI tools.

### Files and folders

- **`~/.openclaw/`** — This becomes OpenClaw's home base, storing configuration in `openclaw.json`
- **`~/.local/bin/openclaw`** — If you choose the git installation method, a wrapper script lands here
- **`~/.npm-global/`** — On Linux systems, npm's global packages get redirected here to avoid permission headaches

### Packages installed

The script is quite thorough about dependencies. Here's what might get installed:

- **Homebrew** (macOS only) — If you don't have it, the script fetches the official Homebrew installer. This is a well-known and trusted package manager for Mac.
- **Node.js v22+** — The script requires a modern Node.js. On macOS it uses Homebrew (`node@22`), on Linux it pulls from NodeSource repositories.
- **Git** — Needed for both installation methods, installed via your system's package manager.
- **pnpm** — If you go the git route, pnpm handles the monorepo's dependencies.
- **openclaw npm package** — The main event! Installed globally via npm.

### Downloads

Depending on your setup, the script may fetch:

- The Homebrew installer from `raw.githubusercontent.com`
- NodeSource setup scripts for Debian/RHEL-based Linux
- The OpenClaw git repository (if you choose `--git` method)

### Environment changes

Here's where things get a bit more personal — the script may modify your shell configuration:

- **PATH updates** in `~/.bashrc` and `~/.zshrc` to include:
  - `~/.npm-global/bin` (Linux npm installs)
  - `~/.local/bin` (git wrapper script)
- **npm prefix** gets changed to `~/.npm-global` on Linux to avoid needing admin rights for global installs

### Services

- **Gateway daemon** — If OpenClaw's daemon service is already running, the installer will restart it after upgrading. This is optional and only affects existing users.

### Permissions

- **Admin rights on Linux** — The script uses sudo for system package installations (Node.js, Git via apt/dnf/yum)
- **File permissions** — The wrapper script at `~/.local/bin/openclaw` gets execute permissions

## Heads up!

Before you yolo this into your terminal, a few things worth noting:

1. **Homebrew installation** — If you don't have Homebrew on macOS, this script will install it. That's a significant addition to your system.

2. **NodeSource repositories** — On Linux, it adds NodeSource as a package source. This is a trusted source, but it does modify your system's package manager configuration.

3. **Shell config modifications** — Your `.bashrc` and/or `.zshrc` files may be edited to add PATH entries. The script does check before adding, so no duplicates.

4. **npm global prefix change** — On Linux, your npm configuration changes to use a user-local directory. This is actually a good practice, but it might surprise you if you expect global packages elsewhere.

## Changed your mind?

No judgment! Here's how to undo things:

**Remove OpenClaw itself:**
```bash
# If installed via npm:
npm uninstall -g openclaw

# If installed via git:
rm -rf ~/openclaw ~/.local/bin/openclaw
```

**Clean up the config:**
```bash
rm -rf ~/.openclaw
```

**Undo shell modifications:**
Edit your `~/.bashrc` and/or `~/.zshrc` and remove these lines if present:
```bash
export PATH="$HOME/.npm-global/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
```

**Remove npm-global directory (Linux):**
```bash
rm -rf ~/.npm-global
npm config delete prefix
```

**Note:** If the script installed Homebrew, Node.js, or Git, those are generally useful to keep around. But if you really want them gone:

- Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"`
- Node.js via Homebrew: `brew uninstall node@22`
- Node.js via NodeSource: Use your package manager (`apt remove nodejs` or `dnf remove nodejs`)

## Full source

The full script source is saved as [`scripts/openclaw_ai_install_sh.txt`](../../scripts/openclaw_ai_install_sh.txt).
