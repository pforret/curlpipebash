---
title: "frankenphp.dev/install.sh"
slug: frankenphp
categories:
  - script
  - frankenphp.dev
date: 2026-01-02
---

The FrankenPHP installer is a 154-line POSIX shell script that installs the FrankenPHP application server — a modern PHP app server built on Caddy — via `curl -sL https://frankenphp.dev/install.sh | bash`. It takes three different installation paths depending on what it finds: on Linux with dnf, it adds an RPM repository from `rpm.henderkes.com` and installs a native package with systemd integration; on Linux with apt, it does the equivalent via a DEB repository at `deb.henderkes.com`; and on all other systems (macOS, or Linux without apt/dnf), it downloads a static binary from GitHub releases directly into the current directory. The script uses `tput` for terminal formatting instead of raw ANSI codes, and on Linux it applies `setcap cap_net_bind_service` to let the binary bind ports 80/443 without root.

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `https://frankenphp.dev/install.sh` |
| **Invocation** | `curl -sL https://frankenphp.dev/install.sh \| bash` |
| **Total lines** | 154 |
| **Comments** | 3 lines |
| **Blank** | 19 lines |
| **Boilerplate** | 9 lines (tput formatting variables, empty echo lines) |
| **Installation** | 122 lines (actual work) |

## What does it change?

### Files and folders

**Via package manager (Linux with dnf or apt):**

- Installs the `frankenphp` binary to `/usr/bin/frankenphp`
- Installs a systemd service that reads `/etc/frankenphp/Caddyfile`
- PHP configuration at `/etc/php-zts/php.ini`

**Via dnf:**

- Adds the RPM repo package from `https://rpm.henderkes.com/static-php-1-0.noarch.rpm`

**Via apt:**

- Downloads GPG signing key to `/usr/share/keyrings/static-php.gpg`
- Creates `/etc/apt/sources.list.d/static-php.list` pointing to `https://deb.henderkes.com/`

**Via direct download (macOS or Linux without apt/dnf):**

- Downloads a single static binary to `$BIN_DIR/frankenphp`, where `$BIN_DIR` defaults to the current working directory (`$(pwd)`)
- Marks the binary executable with `chmod +x`
- On Linux with glibc, downloads the `-gnu` variant; on musl-based systems, downloads the standard variant
- Suggests moving the binary to `/usr/local/bin/` if it's not already in `$PATH`
- Reads `/etc/frankenphp/php.ini` if it exists (no file is created)

### Packages installed

**On Linux with dnf (Fedora, RHEL, etc.):**

- `static-php-1-0.noarch.rpm` — the repository package from `rpm.henderkes.com`
- Enables the `php-zts:static-8.4` module stream
- `frankenphp` — the main package

**On Linux with apt (Debian, Ubuntu, etc.):**

- `frankenphp` — installed from the `deb.henderkes.com` repository

### Downloads

- **dnf path:** RPM repo package from `https://rpm.henderkes.com/static-php-1-0.noarch.rpm`
- **apt path:** GPG key from `https://key.henderkes.com/static-php.gpg`
- **Direct download:** Binary from `https://github.com/php/frankenphp/releases/latest/download/` — one of six variants:
    - `frankenphp-linux-x86_64-gnu` (Linux x86_64, glibc)
    - `frankenphp-linux-x86_64` (Linux x86_64, musl)
    - `frankenphp-linux-aarch64-gnu` (Linux ARM64, glibc)
    - `frankenphp-linux-aarch64` (Linux ARM64, musl)
    - `frankenphp-mac-arm64` (macOS Apple Silicon)
    - `frankenphp-mac-x86_64` (macOS Intel)

### Permissions

- Uses `sudo` when not running as root (detected via `id -u`)
- For the direct download path, does a writability check on `$DEST` via `touch` — if it fails, escalates to sudo for the download destination
- On Linux, applies `setcap 'cap_net_bind_service=+ep'` to the binary if `setcap` is available, allowing the binary to bind to ports 80 and 443 without running as root

## Uninstall

**If installed via package manager:**

```bash
# dnf
sudo dnf remove frankenphp

# apt
sudo apt remove frankenphp
sudo rm /etc/apt/sources.list.d/static-php.list
sudo rm /usr/share/keyrings/static-php.gpg
```

**If installed via direct download:**

```bash
# Remove the binary (wherever BIN_DIR pointed, default is where you ran the script)
rm ./frankenphp

# Or if you moved it:
sudo rm /usr/local/bin/frankenphp
```

Remove the optional configuration directory if created:

```bash
sudo rm -rf /etc/frankenphp
```

## Full source

The full script source is saved as [`docs/scripts/frankenphp_dev_install_sh.txt`](../../scripts/frankenphp_dev_install_sh.txt).
