# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **curlpipebash.com** — a documentation site that catalogs and analyzes "curl | bash" installation scripts from popular open-source projects (Docker, Homebrew, Laravel, nvm, etc.). Each example page shows the script's purpose, `cloc` stats, and full source code. Built with MkDocs + Material for MkDocs theme, deployed to GitHub Pages.

## Commands

### Build and serve the site locally
```bash
mkdocs serve
```

### Build static site (output to ./site/)
```bash
mkdocs build
```

### Generate all example documentation pages
```bash
cd docs/examples && ./generate_all.sh
```

### Analyze a single curl|bash script and generate its markdown page
```bash
cd docs/examples && ./curlbash.sh -D "description of what script does" -R "https://reference-url" markdown https://example.com/install.sh
```

The output filename is auto-generated as `<domain>.<2char-md5-digest>.md` (e.g., `get.docker.com.ff.md`).

### Deploy
Deployment is automatic via GitHub Actions on push to `main`. The workflow (`.github/workflows/static.yml`) uploads the pre-built `./site/` directory to GitHub Pages — it does **not** run `mkdocs build` in CI.

## Architecture

### Content Generation Pipeline

1. `docs/examples/curlbash.sh` — the core analysis tool, built on the [bashew](https://github.com/pforret/bashew) framework (v1.21.2). It:
   - Downloads a script from a given URL via `curl`
   - Runs `cloc` on the downloaded script to produce code statistics
   - Wraps everything (description, reference link, stats, full source via `fold -sw 110`) into a markdown file
   - Requires: `awk`, `cloc`

2. `docs/examples/generate_all.sh` — batch script that calls `curlbash.sh` for each known URL to regenerate all example pages

3. Generated `.md` files land in `docs/examples/` and follow a fixed structure: heading, description with curl command, reference link, cloc stats block, full code listing

### Site Structure

- `docs/` — MkDocs source: `index.md` (homepage), `about/` (about page + feature demos), `blog/` (news posts with RSS), `examples/` (generated script analyses + the generator tools)
- `overrides/` — Material theme partial overrides (analytics integration)
- `site/` — pre-built static output checked into the repo (this is what gets deployed)
- `mkdocs.yml` — site configuration (theme, plugins, markdown extensions)

### Key MkDocs Plugins

- `awesome-pages` — custom page ordering
- `blog` — blog section with date-based URLs (`yyyy/MM`)
- `rss` — RSS feed generation for blog posts

### bashew Framework Conventions (in curlbash.sh)

The script below `DO NOT MODIFY BELOW THIS LINE` (line ~158) is the bashew boilerplate providing:
- `IO:*` functions for output/logging
- `Os:*` functions for OS detection, dependency checking
- `Str:*` functions for string manipulation
- `Option:*` for CLI flag/option parsing
- Automatic `.env` file loading

Custom logic goes in `Script:main()` and helper functions above that line. New actions are added as cases in the `Script:main()` switch statement and registered in `Option:config()`.
