# Best Practices Topics

Future articles for `docs/best-practices/` based on patterns observed in analyzed scripts.

## 1. Partial Download Protection

Techniques to prevent execution of truncated scripts.

- Function wrapper pattern (Docker)
- Brace wrapper pattern (nvm)
- Why both work and when to use each

**Examples:** Docker, nvm

## 2. Multi-Stage Bootstrapping

Small verified stub downloads and executes larger installer.

- Keeping the stub small and simple
- Checksum verification between stages
- Temp file cleanup via `trap`

**Examples:** Google Cloud SDK, Claude Code

## 3. Platform Detection

Detecting OS, architecture, and libc variant.

- `uname -s` / `uname -m` patterns
- Detecting musl vs glibc on Linux
- macOS Intel vs Apple Silicon
- WSL detection

**Examples:** FrankenPHP, Claude Code, Homebrew, Docker

## 4. Shell Profile Management

Finding and modifying the correct shell configuration file.

- Detection order: `.bashrc` vs `.bash_profile` vs `.profile`
- Zsh: `.zshrc` vs `.zprofile`
- Fish: `config.fish`
- Tagging added lines for clean removal (basher's `##basher5ea843`)
- Idempotency: checking before appending

**Examples:** basher, nvm, php.new, Homebrew

## 5. Permission Handling

Running with minimal privileges, escalating only when needed.

- Detecting root vs non-root
- Building a `sh_c` wrapper for sudo/doas
- User-space installs vs system installs
- Refusing to run as root (Homebrew)

**Examples:** Docker, FrankenPHP, Homebrew, Laravel

## 6. Download Tool Abstraction

Supporting both curl and wget transparently.

- Feature detection: `command -v curl`
- Flag translation between tools
- Consistent error handling
- Timeout and retry policies

**Examples:** nvm, Google Cloud SDK, Claude Code

## 7. Existing Installation Detection

Handling upgrades vs fresh installs gracefully.

- Checking for existing directories/binaries
- Prompting before overwriting
- Backup strategies (`*.bak-<timestamp>`)
- Clean upgrade paths

**Examples:** basher, php.new, Homebrew, OpenClaw

## 8. Clean Uninstall Support

Making removal as easy as installation.

- Generated uninstall scripts (php.new)
- Tagged config lines for grep-based removal (basher)
- Documenting manual steps
- Reversible system changes

**Examples:** basher, php.new, Docker

## 9. Interactive Mode Handling

Supporting both interactive and automated execution.

- TTY detection and `/dev/tty` redirection
- Environment variable overrides (`CLOUDSDK_CORE_DISABLE_PROMPTS`)
- `--non-interactive` / `--yes` flags
- Sensible defaults for CI/CD

**Examples:** Google Cloud SDK, Homebrew

## 10. Dependency Verification

Checking prerequisites before starting installation.

- Required tools: git, curl/wget, tar
- Minimum version checks (git 2.7+, glibc 2.13+)
- Graceful failure with actionable error messages
- Optional dependencies and degraded modes

**Examples:** Docker, Homebrew, nvm
