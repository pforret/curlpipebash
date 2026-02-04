---
title: "raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"
slug: rawgithubusercontentcomnvmshnvmv0401installsh
categories:
  - script
  - raw.githubusercontent.com
date: 2026-01-30
---

The nvm (Node Version Manager) installer is a 495-line shell script invoked via `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash`. It installs nvm by either cloning the `nvm-sh/nvm` Git repository (preferred) or downloading three individual files (`nvm.sh`, `nvm-exec`, `bash_completion`) as a fallback when git isn't available — the script method runs all three downloads in parallel using background jobs. The entire script body is wrapped in `{ ... }` braces as partial-download protection, and it enforces execution under bash, rejecting zsh outright. After installation it auto-detects the user's shell profile, appends the `NVM_DIR` export and sourcing lines, and optionally installs a Node.js version if `$NODE_VERSION` is set.

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh` |
| **Invocation** | `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh \| bash` |
| **Total lines** | 495 |
| **Comments** | 52 lines |
| **Blank** | 49 lines |
| **Boilerplate** | 0 lines |
| **Installation** | 393 lines (actual work) |

## What does it change?

### Files and folders

- Creates `~/.nvm/` as the default install directory (or `$XDG_CONFIG_HOME/nvm` if `XDG_CONFIG_HOME` is set, or whatever `$NVM_DIR` points to)
- **Git method:** shallow-clones the full `nvm-sh/nvm` repo into the install directory, checks out the version tag, then runs `git reflog expire` and `git gc --aggressive --prune=now` to compact the repo
- **Script method:** downloads `nvm.sh`, `nvm-exec`, and `bash_completion` into the install directory
- Sets `nvm-exec` as executable (`chmod a+x`)
- Appends sourcing lines to the detected shell profile file (see Environment changes)

### Downloads

- **Git method:** clones from `https://github.com/nvm-sh/nvm.git` with `--depth=1`
- **Script method:** fetches three files in parallel from `https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/`:
    - `nvm.sh` — the main nvm script
    - `nvm-exec` — helper executable
    - `bash_completion` — tab completion definitions
- Supports both `curl` and `wget` as download backends; the `nvm_download()` function translates curl flags to wget equivalents
- If `$NODE_VERSION` is set, downloads and installs that Node.js version via `nvm install` after setup

### Environment changes

- Exports `NVM_DIR` pointing to the install directory
- Sources `$NVM_DIR/nvm.sh` to make the `nvm` command available
- Sources `$NVM_DIR/bash_completion` for tab completion (bash and zsh profiles only)
- Appends these three lines to the auto-detected shell profile — one of `.bashrc`, `.bash_profile`, `.zshrc`, `.zprofile`, or `.profile`, checked in that order based on `$SHELL`. Set `PROFILE=/dev/null` to skip profile modification entirely.

## Uninstall

Remove the nvm directory and clean up your shell profile:

```bash
rm -rf "${NVM_DIR:-$HOME/.nvm}"
```

Then edit your shell profile (e.g. `~/.bashrc`, `~/.zshrc`) and remove these lines:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

Any Node.js versions installed via nvm live inside `~/.nvm/versions/` and are removed with the directory above.

## Full source

The full script source is saved as [`docs/scripts/raw_githubusercontent_com_nvm_sh_nvm_v0_40_1_install_sh.txt`](../../docs/scripts/raw_githubusercontent_com_nvm_sh_nvm_v0_40_1_install_sh.txt).
