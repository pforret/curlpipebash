# Invocation Styles

Different projects use different styles to invoke their installer scripts. This page catalogs the common patterns and their trade-offs.

## The three main patterns

### 1. Direct pipe

```bash
curl -sL https://example.com/install.sh | bash
```

The script streams directly from curl into bash. Simple and common, but vulnerable to partial downloads — if the connection drops mid-script, bash may execute a truncated script with unpredictable results.

**Used by:** [basher](../blog/posts/2026-01-01-basherpm.md), [FrankenPHP](../blog/posts/2026-01-02-frankenphp-dev.md), [Laravel](../blog/posts/2026-01-10-laravel-build.md), [php.new](../blog/posts/2026-01-04-php-new.md), [Google Cloud SDK](../blog/posts/2026-01-13-sdk-cloud-google-com.md)

### 2. Output-to-stdout explicit

```bash
curl -o- https://example.com/install.sh | bash
```

Functionally identical to `-sL`, but `-o-` explicitly writes to stdout instead of relying on curl's default behavior. Some consider this more explicit and readable.

**Used by:** [nvm](../blog/posts/2026-01-12-nvm.md)

### 3. Command substitution

```bash
/bin/bash -c "$(curl -fsSL https://example.com/install.sh)"
```

Downloads the entire script first, then passes it to bash. This **eliminates the partial download problem** — if curl fails or the connection drops, bash receives nothing (or an error message) instead of a truncated script.

**Used by:** [Homebrew](../blog/posts/2025-12-31-homebrew.md)

## curl flag combinations

| Flags | Meaning | Example users |
|-------|---------|---------------|
| `-sL` | Silent mode, follow redirects | basher, FrankenPHP, php.new, Laravel, Google Cloud SDK |
| `-fsSL` | Fail on HTTP error, silent (show errors), follow redirects | Docker, Claude Code, OpenClaw, Homebrew |
| `-o-` | Output to stdout (explicit) | nvm |

### Flag breakdown

| Flag | Purpose |
|------|---------|
| `-s` | Silent mode — no progress meter or error messages |
| `-S` | Show errors even when `-s` is used |
| `-L` | Follow HTTP redirects (essential for URL shorteners or CDNs) |
| `-f` | Fail silently on HTTP errors (4xx/5xx) — returns exit code 22 |
| `-o-` | Write output to stdout (explicit, same as default behavior) |

The `-fsSL` combination is the most defensive: it follows redirects, stays quiet on success, but surfaces errors and fails properly on HTTP errors.

## wget equivalents

Some scripts support both curl and wget. Here are the equivalent commands:

| curl | wget |
|------|------|
| `curl -sL URL` | `wget -qO- URL` |
| `curl -fsSL URL` | `wget -qO- URL` (wget fails on HTTP errors by default) |
| `curl -o- URL` | `wget -O- URL` |

## Script-level partial download protection

Well-designed scripts protect themselves against partial downloads, independent of invocation style:

### Function wrapper

Wrap the entire script body in a function, call it at the end:

```bash
#!/bin/bash
do_install() {
    # ... entire script here ...
}
do_install
```

**Used by:** [Docker](../blog/posts/2026-01-03-get-docker-com.md) — If the download is truncated before the final `do_install` call, nothing executes.

### Brace wrapper

Wrap the script in braces:

```bash
{
    # ... entire script here ...
}
```

**Used by:** [nvm](../blog/posts/2026-01-12-nvm.md) — bash won't execute the block until it sees the closing brace.

### Multi-stage bootstrap

A small stub script downloads and executes the real installer:

```bash
#!/bin/bash
# Stage 1: tiny stub
curl -sL https://example.com/real-installer.sh > /tmp/installer.sh
bash /tmp/installer.sh
rm /tmp/installer.sh
```

**Used by:** [Google Cloud SDK](../blog/posts/2026-01-13-sdk-cloud-google-com.md), [Claude Code](../blog/posts/2026-01-28-claude-ai.md) — The stub is small enough to survive partial downloads; the real installer is downloaded as a file and verified before execution.

## Server-side pipe detection

A malicious server can detect whether you're piping to bash or downloading to a file, and serve different content accordingly. This is a real attack vector.

### How detection works

When you run `curl URL | bash`, bash executes commands as they arrive — it doesn't wait for the full download. A server can exploit this timing difference:

1. Send a payload containing `sleep 1` followed by buffer-filling data
2. Measure how long the response takes to complete
3. If it takes >1 second, bash is executing (sleeping); serve malicious payload
4. If it completes instantly, user is just downloading; serve harmless payload

```go
// Simplified server-side detection (Go)
started := time.Now()
res.Write(detect_payload)  // contains sleep + buffer filler
elapsed := time.Since(started)

if elapsed.Seconds() > 1 {
    res.Write(malicious_payload)
} else {
    res.Write(harmless_payload)
}
```

This means **reviewing a script by downloading it first doesn't guarantee you'll see the same script that runs when piped**.

### Which patterns are vulnerable?

| Pattern | Detectable? | Why |
|---------|-------------|-----|
| `curl URL \| bash` | **Yes** | Bash executes during download |
| `curl -o- URL \| bash` | **Yes** | Same streaming behavior |
| `/bin/bash -c "$(curl URL)"` | **No** | curl completes before bash starts |
| `curl URL > file && bash file` | **No** | Download completes before execution |

The **command substitution** pattern (`$(curl ...)`) defeats this attack because curl must finish entirely before bash receives any content. The server cannot distinguish this from a direct download.

### Reference

See [The Dangers of curl|bash](https://lukespademan.com/blog/the-dangers-of-curlbash/) for a detailed proof-of-concept.

## Recommendations

**For script authors:**

1. Use the function wrapper or brace wrapper pattern
2. If distributing via CDN with redirects, ensure your docs use `-L` / `-fsSL`
3. Consider a multi-stage bootstrap with checksum verification for high-security scenarios
4. Publish checksums so users can verify downloads independently

**For users:**

1. Prefer `-fsSL` over `-sL` to catch HTTP errors
2. Use **command substitution** to defeat pipe detection attacks:
   ```bash
   /bin/bash -c "$(curl -fsSL https://example.com/install.sh)"
   ```
3. For maximum security, download, verify checksum, inspect, then execute:
   ```bash
   curl -fsSL https://example.com/install.sh -o install.sh
   sha256sum install.sh  # compare against published checksum
   less install.sh       # review the script
   bash install.sh
   rm install.sh
   ```
4. Be aware that downloading first doesn't guarantee you see what `curl | bash` would execute — a malicious server can detect the difference

## Interactive scripts

Some installers need user input during execution. When piped through bash, stdin is consumed by the script content. Solutions:

- **TTY redirection:** The script redirects stdin from `/dev/tty` to restore interactivity. Used by [Google Cloud SDK](../blog/posts/2026-01-13-sdk-cloud-google-com.md).
- **Environment variables:** Accept configuration via env vars instead of prompts. Example: `CLOUDSDK_CORE_DISABLE_PROMPTS=1`
- **Command-line flags:** Pass `--non-interactive` or similar flags.
