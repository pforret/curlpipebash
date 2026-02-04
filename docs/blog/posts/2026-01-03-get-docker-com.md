---
title: "get.docker.com"
categories:
  - script
  - get.docker.com
date: 2026-01-03
---

The Docker convenience install script at `get.docker.com` is a substantial 764-line shell script that configures Docker's official package repositories and installs Docker Engine, CLI, containerd, Compose, Buildx, rootless extras, and (as of v28.2) the Docker Model plugin on Linux systems via `curl -fsSL https://get.docker.com | bash`. It supports Debian/Ubuntu/Raspbian (apt), CentOS/Fedora/RHEL (dnf/yum), handles architecture detection, version pinning, channel selection (stable/test), and China mirror support (Aliyun, Azure). The entire script body is wrapped in a `do_install()` function as protection against partial downloads during pipe execution — a classic defensive pattern. Roughly 150 lines are comments, including a 97-line header that doubles as thorough usage documentation.

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `https://get.docker.com` |
| **Invocation** | `curl -fsSL https://get.docker.com \| bash` |
| **Total lines** | 764 |
| **Comments** | 150 lines (including 97-line header with usage docs) |
| **Blank** | 50 lines |
| **Boilerplate** | ~50 lines (deprecation notices, post-install info, version comparison helpers) |
| **Installation** | ~513 lines (actual work) |

## What does it change?

### Files and folders

- On Debian/Ubuntu/Raspbian: creates `/etc/apt/keyrings/` (mode 0755), downloads Docker's GPG key to `/etc/apt/keyrings/docker.asc`, and writes the apt source to `/etc/apt/sources.list.d/docker.list`
- On CentOS/Fedora/RHEL: adds the Docker repo file to `/etc/yum.repos.d/` via `dnf config-manager` or `yum-config-manager`, replacing any existing `docker-ce.repo` or `docker-ce-staging.repo`

### Packages installed

On Debian/Ubuntu/Raspbian (via apt):

- `ca-certificates`, `curl` (prerequisites)
- `docker-ce` (Docker Engine)
- `docker-ce-cli` (CLI, for versions >= 18.09)
- `containerd.io` (container runtime, >= 18.09)
- `docker-compose-plugin` (Compose v2, >= 20.10)
- `docker-ce-rootless-extras` (rootless mode, >= 20.10)
- `docker-buildx-plugin` (BuildKit, >= 23.0)
- `docker-model-plugin` (AI model runner, >= 28.2)

On CentOS/Fedora/RHEL (via dnf or yum):

- `dnf-plugins-core` or `yum-utils` (prerequisites)
- Same Docker packages as above, with version-appropriate RPM suffixes

Version pinning is supported via `--version` — the script searches `apt-cache madison` or `dnf/yum list --showduplicates` to resolve the exact package version.

### Downloads

- Docker GPG signing key: `https://download.docker.com/linux/<distro>/gpg` (Debian/Ubuntu/Raspbian only)
- Docker repo file: `https://download.docker.com/linux/<distro>/docker-ce.repo` (CentOS/Fedora/RHEL only)
- Optional mirrors: `https://mirrors.aliyun.com/docker-ce` (Aliyun) or `https://mirror.azure.cn/docker-ce` (Azure China)

### Services

- Enables and starts `docker.service` via `systemctl enable --now` unless `--no-autostart` is passed
- In container environments without systemd, prints a notice that the daemon cannot be auto-started

### Permissions

- Requires root or sudo/su — the script constructs a `sh_c` variable set to `sudo -E sh -c` (or `su -c`) and runs all system commands through it
- After installation, prints instructions for rootless mode (`dockerd-rootless-setuptool.sh install`) for versions >= 20.10

### System configuration

- Reads `/etc/os-release`, `/etc/lsb-release`, and `/etc/debian_version` to detect the distribution and version
- Handles forked distros (e.g., OSMC → Raspbian, unnamed Debian derivatives) via `lsb_release -a -u` and codename mapping (Debian 8–13 → jessie through trixie)
- Prints deprecation notices for EOL distributions: CentOS 7/8, RHEL 7, Debian stretch/buster/jessie, Ubuntu focal and older non-LTS releases, Fedora < 41
- Detects WSL and recommends Docker Desktop for Windows instead

## Uninstall

Remove the Docker packages with your package manager:

```bash
# Debian/Ubuntu
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-buildx-plugin docker-ce-rootless-extras docker-model-plugin
sudo apt-get autoremove

# CentOS/Fedora/RHEL
sudo dnf remove docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-buildx-plugin docker-ce-rootless-extras docker-model-plugin
```

Remove Docker data and configuration:

```bash
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

Remove the repository configuration:

```bash
# Debian/Ubuntu
sudo rm /etc/apt/sources.list.d/docker.list
sudo rm /etc/apt/keyrings/docker.asc

# CentOS/Fedora/RHEL
sudo rm /etc/yum.repos.d/docker-ce.repo
```

## Full source

The full script source is saved as [`docs/scripts/get_docker_com.txt`](../../scripts/get_docker_com.txt).
