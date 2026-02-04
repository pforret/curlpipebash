---
title: "laravel.build/example-app"
slug: laravelbuildexample-app
categories:
  - script
  - laravel.build
date: 2026-01-30
---

The `laravel.build` installer is a compact 52-line script generated server-side by Laravel's build service, invoked via `curl -sL https://laravel.build/example-app | bash`. The URL path (`example-app`) determines the project name, and query parameters can customize which services are included. The script requires Docker to be running, pulls the `laravelsail/php84-composer:latest` image, runs `laravel new` and `sail:install` inside a container, then uses Laravel Sail to pull and build Docker images for mysql, redis, meilisearch, mailpit, and selenium. No software is installed on the host beyond the project directory — everything runs in Docker. Notably, the script has no shebang line and supports `doas` as a sudo alternative alongside the usual `sudo`.

<!-- more -->

## Script info

| | |
|---|---|
| **URL** | `https://laravel.build/example-app` |
| **Invocation** | `curl -sL https://laravel.build/example-app \| bash` |
| **Total lines** | 52 |
| **Comments** | 2 lines |
| **Blank** | 9 lines |
| **Boilerplate** | 10 lines (color variables, formatted echo output) |
| **Installation** | 31 lines (actual work) |

## What does it change?

### Files and folders

- Creates an `example-app/` directory in the current working directory, containing a full Laravel project with Sail configuration
- The project is scaffolded inside a Docker container (`laravelsail/php84-composer:latest`) with the current directory bind-mounted to `/opt`, so the files end up on the host
- Runs `chown -R $USER:` on the project directory to transfer ownership from root (Docker) to the current user

### Downloads

- Pulls the Docker image `laravelsail/php84-composer:latest` (with `--pull=always`, so it always fetches the newest version)
- Inside the container, `laravel new` downloads the Laravel framework and its Composer dependencies
- `sail pull` downloads Docker images for the configured services: mysql, redis, meilisearch, mailpit, and selenium
- `sail build` builds the application's Docker image

The service list is server-side templated. The URL `https://laravel.build/example-app?with=mysql,redis` would generate a script with only mysql and redis. Passing `?with=none` skips the pull step and only runs `sail build`.

### Services

- No host-level services are installed or started — all services (MySQL, Redis, Meilisearch, Mailpit, Selenium) run as Docker containers managed by Laravel Sail
- After installation, the user starts everything with `./vendor/bin/sail up`

### Permissions

- Uses `sudo` or `doas` (whichever is available, with `doas` checked first) to `chown -R` the project directory to the current user
- If the user's sudo/doas session is already active (`-n true` succeeds), it runs silently; otherwise it prompts for a password

## Uninstall

Remove the project directory:

```bash
cd example-app
./vendor/bin/sail down --rmi all --volumes  # stop containers, remove images and volumes
cd ..
rm -rf example-app
```

Remove the pulled Docker images if no longer needed:

```bash
docker rmi laravelsail/php84-composer:latest
# Plus any service images (mysql, redis, meilisearch, etc.)
docker image prune
```

No shell profile, PATH, or system configuration changes need to be reversed.

## Full source

The full script source is saved as [`docs/scripts/laravel_build_example_app.txt`](../../scripts/laravel_build_example_app.txt).
