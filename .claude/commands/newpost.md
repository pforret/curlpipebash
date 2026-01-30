---
description: Download and analyze a curl|bash script, create a blog post
argument-hint: <script-url>
allowed-tools: Bash(curl:*), Bash(mkdir:*), Bash(wc:*), Bash(date:*), Read, Write, Grep, Glob
---

Analyze a "curl | bash" installation script and create a blog post about it.

The script URL is: $ARGUMENTS

Follow these steps precisely:

## Step 1: Parse the URL

Extract the domain name and path from the URL.
- Example: `https://openclaw.ai/install.sh` → domain = `openclaw.ai`, path = `install.sh`
- Example: `https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh` → domain = `raw.githubusercontent.com`, path = `nvm-sh/nvm/v0.39.0/install.sh`

## Step 2: Download the script

1. Create the `scripts/` directory at the project root if it doesn't exist: `mkdir -p scripts`
2. Build a sanitized filename from the full URL (after removing the scheme): replace all `/`, `.`, and `-` with `_`. Append `.txt`. Example: `https://openclaw.ai/install.sh` → `scripts/openclaw_ai_install_sh.txt`
3. Download: `curl -sL <URL> -o scripts/<filename>.txt`
4. Verify the file was downloaded and is non-empty.

## Step 3: Read and analyze the script

Read the downloaded script file. Classify every line into one of these categories:

- **Shebang**: the `#!/...` line (typically line 1)
- **Blank lines**: empty or whitespace-only lines
- **Comment lines**: lines where the first non-whitespace character is `#` (excluding shebang)
- **Boilerplate lines**: lines that handle output formatting, color codes, or cosmetic concerns. These include:
  - Variable assignments for ANSI color codes (e.g., `RED=`, `GREEN=`, `BOLD=`, `RESET=`, `NC=`, or lines containing `\033[`, `\e[`, `\x1b[`)
  - `echo`/`printf` statements that only print decorative output (banners, separators, status messages)
  - Usage/help text functions (functions named `usage`, `help`, `print_help`, `show_help` and their contents)
  - Error handling helper functions that only format/print messages
- **Installation lines**: everything else — the lines that actually perform work:
  - Package manager commands (`apt`, `brew`, `npm`, `pip`, `yum`, `dnf`, `pacman`, `apk`, `snap`)
  - File operations (`mkdir`, `cp`, `mv`, `ln`, `chmod`, `chown`, `touch`, `cat >`, `tee`)
  - Downloads (`curl`, `wget`, `git clone`)
  - Service management (`systemctl`, `service`, `launchctl`)
  - Environment changes (`export`, `PATH=`, sourcing files)
  - Conditional logic, loops, and function definitions that drive the installation

Produce a count for each category.

## Step 4: Identify system changes

Determine what the script would change on a machine. Look for:

- **Files/folders created**: `mkdir`, `touch`, `cat >`, `tee`, file redirections (`>`, `>>`)
- **Packages installed**: commands using `apt-get install`, `brew install`, `npm install`, `pip install`, `yum install`, etc.
- **Downloads**: additional `curl`, `wget`, or `git clone` commands fetching other resources
- **PATH/environment changes**: modifications to `PATH`, `export` statements, writes to `.bashrc`, `.zshrc`, `.profile`, `.bash_profile`
- **Services**: `systemctl enable/start`, `service start`, cron jobs
- **Permissions**: `chmod`, `chown`, `sudo` usage
- **System configuration**: modifications to system files in `/etc/`, kernel parameters, etc.

Summarize each category with specific details from the script.

## Step 5: Create the blog post

Build a slug from the domain: lowercase, replace dots with dashes. Example: `openclaw.ai` → `openclaw-ai`.

Get today's date in YYYY-MM-DD format using: `date +%Y-%m-%d`

Create the file `docs/blog/posts/YYYY-MM-<slug>.md` with this structure:

```
---
title: "Script: <domain>"
categories:
  - Analysis
date: <YYYY-MM-DD>
---

<summary paragraph: 2-4 sentences describing what this script does, how it's invoked
(`curl ... | bash`), and the key things it changes on the system. Keep it factual and concise.>

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `<full URL>` |
| **Invocation** | `curl -sL <URL> \| bash` |
| **Total lines** | <N> |
| **Comments** | <N> lines |
| **Blank** | <N> lines |
| **Boilerplate** | <N> lines (output formatting, colors, usage text) |
| **Installation** | <N> lines (actual work) |

## What does it change?

<For each category of system change found, write a subsection with bullet points
listing the specific files, packages, downloads, or changes. Only include categories
that actually apply. Use these subsection headers as appropriate:>

### Files and folders
### Packages installed
### Downloads
### Environment changes
### Services
### Permissions

## Full source

The full script source is saved as [`scripts/<filename>.txt`](../../scripts/<filename>.txt).
```

Write this file using the Write tool. Do not create any other files besides the script download and the blog post.
