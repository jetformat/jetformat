# Install Jetformat

[Home](../README.md) · [中文](../README.zh-CN.md) · [Agent setup](agents.md)

## npm

With Node.js 18 or newer:

```bash
npm install -g jetformat
jetformat --version
```

npm installs the native binary for your platform via an optional platform package. Keep optional dependencies enabled. You can also run `npx jetformat --version` without a global installation.

Update with `npm install -g jetformat@latest`.

## Homebrew

On macOS or Linux:

```bash
brew install jetformat/tap/jetformat
jetformat --version
```

Update with `brew update` followed by `brew upgrade jetformat`.

## Direct download

Open [the latest release](https://github.com/jetformat/jetformat/releases/latest). Choose one of the six `jetformat_<version>_<os>_<arch>` archives, plus `SHA256SUMS`. The CLI runs without Node.js, Go, or a desktop Office application.

- `darwin` means macOS; `linux` means Linux; `windows` means Windows.
- `arm64` means Apple Silicon or another ARM64 CPU; `amd64` means Intel/AMD x64.
- macOS and Linux use `.tar.gz`; Windows uses `.zip`.
- Do not download GitHub's **Source code** archives when you want the executable.

### macOS and Linux

In the directory containing your downloaded archive, set the filename to the one you downloaded. For example, for macOS Apple Silicon v0.1.7:

```bash
ARCHIVE=jetformat_0.1.7_darwin_arm64.tar.gz
# macOS:
shasum -a 256 "$ARCHIVE"
# Linux:
# sha256sum "$ARCHIVE"
```

Compare the result with the matching line in `SHA256SUMS`. These are integrity checksums, not a code-signing or notarization claim. After verification:

```bash
tar -xzf "$ARCHIVE"
mkdir -p "$HOME/.local/bin"
install -m 755 jetformat "$HOME/.local/bin/jetformat"
export PATH="$HOME/.local/bin:$PATH"
jetformat --version
```

Add the `export PATH` line to your shell configuration (`~/.zshrc` or `~/.bashrc`) if that directory is not already on your `PATH`. A browser-downloaded unsigned binary may trigger a macOS security prompt; verify the source and checksum before allowing it through System Settings → Privacy & Security.

### Windows (PowerShell)

For the x64 v0.1.7 archive:

```powershell
Get-FileHash .\jetformat_0.1.7_windows_amd64.zip -Algorithm SHA256
Get-Content .\SHA256SUMS
```

Compare the matching hash, then extract and run:

```powershell
Expand-Archive .\jetformat_0.1.7_windows_amd64.zip -DestinationPath .\jetformat-cli
.\jetformat-cli\jetformat.exe --version
```

Move the executable to a permanent directory, add that directory to your user `Path` in **Environment Variables**, and reopen your terminal. Use the ARM64 archive on Windows ARM64.

## Sign in and try it

Reading and validating files requires no account:

```bash
jetformat text report.docx --format markdown
jetformat validate report.docx
```

For conversion, rendering, or writing files:

```bash
jetformat login
jetformat status
jetformat word to-pdf report.docx -o report.pdf
```

On a machine without a browser, use `jetformat login --device-auth` and follow the printed URL and code. Account and credit information: [billing help](https://jetformat.com/help/billing/credits).

## Fonts and layout

Use the fonts expected by your input document, including CJK fonts for Chinese, Japanese, or Korean text. To supply an additional font directory:

```bash
jetformat word to-pdf report.docx -o report.pdf --font-dir /path/to/fonts
```

The directory must exist; `--font-dir` can be repeated. Font substitution can change line breaks and pagination. Only install or distribute fonts you have permission to use.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `jetformat: command not found` | Reopen your terminal; verify the executable directory is on `PATH`. |
| Wrong architecture / cannot execute | Confirm your OS and CPU, then download the matching archive. |
| npm platform package missing | Reinstall with optional dependencies enabled. |
| Agent cannot find CLI | The CLI must be on `PATH` in the agent's own execution environment. |
| Sign-in or insufficient credits | Run `jetformat status`; follow the CLI error and billing help. |
| Missing glyphs / changed layout | Install the document fonts or use `--font-dir`. |
| PDF has no extracted text | It may contain scanned images. Jetformat text extraction is not OCR. |
| Output file already exists | Choose a new path, or add `--force` when you intend to replace it. |

Report reproducible problems in [Issues](https://github.com/jetformat/jetformat/issues).
