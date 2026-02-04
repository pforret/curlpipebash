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

1. Create the `docs/scripts/` directory if it doesn't exist: `mkdir -p docs/scripts`
2. Build a sanitized filename from the full URL (after removing the scheme): replace all `/`, `.`, and `-` with `_`. Append `.txt`. Example: `https://openclaw.ai/install.sh` → `docs/scripts/openclaw_ai_install_sh.txt`
3. Download: `curl -sL <URL> -o docs/scripts/<filename>.txt`
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

**Writing tone**: Write like a friendly tech enthusiast sharing discoveries with a curious friend. Be warm, conversational, and sprinkle in light humor where appropriate (puns welcome!). Use words like install/copy/overwrite/delete/find/admin permissions — but make it fun, not dry. Don't talk about sudo, grep, cp, mv, rm -fr.

Point out dangerous or irreversible steps, but do it with a helpful "heads up!" vibe rather than alarming language. Think "before you yolo this into your terminal..." rather than "WARNING: DANGER".

You will need to propose an 'uninstall' procedure at the end of the blog post — frame it as "Changed your mind? Here's how to undo things" with a helpful, non-judgmental tone. Keep track of what gets changed/installed/renamed.

## Step 5: create a placeholder image

Create an image with the installed `splashmark` script: 

```
cd docs/images/ && splashmark -i "<title>" unsplash <common word related to this scriupt> <slug>.jpg
magick <slug>.jpg -resize 400x400 <slug>_small.jpg
```

This will create an image `docs/images/<slug>.jpg` which we will use in the blog post.
This will also create an image `docs/images/<slug>_small.jpg` which we will use on the homepage later.

## Step 6: Create the blog post

**Overall tone for the entire post**: Write with enthusiasm and warmth! Imagine you're a curious developer who just discovered something cool and can't wait to share it. Use casual, conversational language. Rhetorical questions are great ("Ever wanted to...?"). Light jokes and wordplay are encouraged. But stay informative — the reader should learn something useful while having a good time.

Build a slug from the domain: lowercase, replace dots with dashes. Example: `openclaw.ai` → `openclaw-ai`.
If the domain is a GitHub subdomain, use the repository's name like <author/repo_name> as title and <repo_name> as slug

Get today's date in YYYY-MM-DD format using: `date +%Y-%m-%d`

Create the file `docs/blog/posts/YYYY-MM-DD-<slug>.md` with this structure:

```markdown
---
title: "<title>"
image: "/images/<slug>.jpg"
categories:
  - script
  - <domain>
date: <YYYY-MM-DD>
---

<summary paragraph: 2-4 sentences describing what this script does, how it's invoked
(`curl ... | bash`), and the key things it changes on the system. Be engaging and hook the reader —
start with what problem this solves or why someone would want it. Keep it punchy but informative.>

![<slug>](../../images/<slug>.jpg)

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
that actually apply. Add brief, friendly commentary — don't just list things, give context
about why it matters or what to watch out for. Use these subsection headers as appropriate:>

### Files and folders
### Packages installed
### Downloads
### Environment changes
### Services
### Permissions

## Changed your mind?

<Write a friendly uninstall/rollback guide. Explain how to undo what the script did —
remove installed files, unset environment changes, etc. Keep it practical and reassuring.
If some changes are hard to reverse, mention that honestly but helpfully.>

## Full source

The full script source is saved as [`scripts/<filename>.txt`](../../scripts/<filename>.txt).
```

Write this file using the Write tool. Do not create any other files besides the script download and the blog post.
