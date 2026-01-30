---
title: "sdk.cloud.google.com"
categories:
  - script
  - sdk.cloud.google.com
date: 2026-01-30
---

The Google Cloud SDK installer uses a two-stage bootstrap: a 17-line stub at `sdk.cloud.google.com` (invoked via `curl -sL https://sdk.cloud.google.com | bash`) downloads and executes the real 218-line installer from `dl.google.com`, which in turn downloads a `google-cloud-sdk.tar.gz` tarball and runs the bundled `install.sh` from inside it — three layers deep. The stage 2 script is interactive: it prompts for an installation directory and handles TTY redirection so that prompts work even when the script is piped through bash. It supports both `curl` and `wget` for downloads, accepts `--disable-prompts` and `--install-dir` flags, and can be configured entirely through environment variables (`CLOUDSDK_CORE_DISABLE_PROMPTS`, `CLOUDSDK_INSTALL_DIR`).

<!-- more -->

## Script info

**Stage 1 — bootstrap stub** (`sdk.cloud.google.com`):

| | |
|---|---|
| **URL** | `https://sdk.cloud.google.com` |
| **Invocation** | `curl -sL https://sdk.cloud.google.com \| bash` |
| **Total lines** | 17 |
| **Comments** | 0 lines |
| **Blank** | 5 lines |
| **Boilerplate** | 0 lines |
| **Installation** | 11 lines |

**Stage 2 — actual installer** (`dl.google.com/dl/cloudsdk/channels/rapid/install_google_cloud_sdk.bash`):

| | |
|---|---|
| **URL** | `https://dl.google.com/dl/cloudsdk/channels/rapid/install_google_cloud_sdk.bash` |
| **Total lines** | 218 |
| **Comments** | 21 lines |
| **Blank** | 21 lines |
| **Boilerplate** | 21 lines (usage text, echo formatting) |
| **Installation** | 154 lines (actual work) |

## What does it change?

### Files and folders

- Creates `$HOME/google-cloud-sdk/` (or `$CLOUDSDK_INSTALL_DIR/google-cloud-sdk/` if specified) by extracting the tarball with `tar -zxvf`
- If the destination directory already exists, the script prompts to remove it (or aborts in non-interactive mode)
- After extraction, runs `google-cloud-sdk/install.sh` — the bundled installer, which handles shell completion, PATH setup, and component installation
- Stage 1 creates a temporary directory via `mktemp -d` for the download; stage 2 also creates one, both cleaned up via `trap` on exit

### Downloads

**Stage 1 downloads stage 2:**

- `https://dl.google.com/dl/cloudsdk/channels/rapid/install_google_cloud_sdk.bash` — the 218-line interactive installer, saved to a temp directory

**Stage 2 downloads the SDK tarball:**

- `https://dl.google.com/dl/cloudsdk/channels/rapid/google-cloud-sdk.tar.gz` — the full Google Cloud SDK
- Uses `curl` if available, falls back to `wget`

### Environment changes

The stage 2 script itself does not modify environment files — it delegates to the bundled `install.sh` inside the extracted tarball, which:

- Adds `google-cloud-sdk/bin` to `PATH` in your shell profile
- Sets up shell completion for `gcloud`, `gsutil`, and `bq`
- Modifies `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish` depending on the detected shell

The stage 2 script handles TTY detection: when piped via `curl | bash`, it redirects stdin from `/dev/tty` so interactive prompts still work. If no TTY is available, it sets `CLOUDSDK_CORE_DISABLE_PROMPTS=1` and runs non-interactively.

### Permissions

- No `sudo` is used — everything installs into the user's home directory
- Stage 1 sets `chmod 775` on the downloaded stage 2 script

## Uninstall

Remove the SDK directory:

```bash
rm -rf ~/google-cloud-sdk
```

Remove the shell profile lines. The bundled installer adds sourcing lines for `path.bash.inc` and `completion.bash.inc` (or the zsh/fish equivalents). Check and remove from your profile:

```bash
# Look for lines referencing google-cloud-sdk in your profile
grep -n "google-cloud-sdk" ~/.bashrc ~/.zshrc ~/.profile 2>/dev/null
# Edit the file(s) to remove those lines
```

Optionally remove cached configuration:

```bash
rm -rf ~/.config/gcloud
```

## Full source

The full script source is saved as [`docs/scripts/sdk_cloud_google_com.txt`](../../scripts/sdk_cloud_google_com.txt).
