<div align="center">

# Jetformat

### Documents in. PDFs, text, and answers out.

Local document tools for your terminal, Codex, Claude Code, and DeepSeek Harness.

[![Release](https://img.shields.io/github/v/release/jetformat/jetformat)](https://github.com/jetformat/jetformat/releases/latest)
[![Build](https://github.com/jetformat/jetformat/actions/workflows/release.yml/badge.svg)](https://github.com/jetformat/jetformat/actions/workflows/release.yml)
[![npm](https://img.shields.io/npm/v/jetformat)](https://www.npmjs.com/package/jetformat)

[Website](https://jetformat.com) · [Download](https://github.com/jetformat/jetformat/releases/latest) · [Documentation](https://jetformat.com/docs/models) · [中文](README.zh-CN.md)

</div>

Turn a Word contract, Excel workbook, or PowerPoint deck into a PDF with one command. Extract structured text for an AI agent, inspect a document, or merge and preview PDFs—all with the same CLI.

```bash
npm install -g jetformat
jetformat login
jetformat word to-pdf contract.docx -o contract.pdf
```

**No Microsoft Office or LibreOffice installation. Local Office and PDF processing. Native binaries for macOS, Linux, and Windows.**

## What you can do

| Task | Example |
| --- | --- |
| Word → PDF | `jetformat word to-pdf contract.docx -o contract.pdf` |
| Excel → PDF | `jetformat excel to-pdf workbook.xlsx -o workbook.pdf` |
| PowerPoint → PDF | `jetformat ppt to-pdf slides.pptx -o slides.pdf` |
| PDF → editable Word | `jetformat pdf to-word report.pdf -o report.docx` |
| Give documents to an agent as Markdown | `jetformat text report.docx --format markdown` |
| Extract spreadsheet data as JSON | `jetformat text workbook.xlsx --format json` |
| Inspect a PDF | `jetformat pdf info report.pdf --json` |
| Merge PDFs | `jetformat pdf merge a.pdf b.pdf -o combined.pdf` |
| Extract a page range | `jetformat pdf extract report.pdf --pages 2-5 -o chapter.pdf` |
| Render preview images | `jetformat pdf render report.pdf --pages 1,last --width 1600 -o preview` |
| Validate a document | `jetformat validate contract.docx` |

[More workflows: templates, mail merge, spreadsheet edits, slide edits, and batch conversion →](docs/usage.md)

## See the output

Real Jetformat conversion previews from our [website showcase](https://jetformat.com), using sample documents. Rendering depends on the document and installed fonts.

| Word contract | Excel report | PowerPoint deck |
| :---: | :---: | :---: |
| ![Word contract converted to PDF](assets/word-preview.webp) | ![Excel revenue report converted to PDF](assets/excel-preview.webp) | ![PowerPoint board deck converted to PDF](assets/ppt-preview.webp) |

## Install

**npm** · macOS, Linux, Windows · Node.js 18+

```bash
npm install -g jetformat
jetformat --version
```

**Homebrew** · macOS, Linux

```bash
brew install jetformat/tap/jetformat
```

**Standalone binary** · no Node.js or Go required

Download an archive from [GitHub Releases](https://github.com/jetformat/jetformat/releases/latest), extract it, and add the executable to your `PATH`.

| Platform | Choose the asset ending in |
| --- | --- |
| macOS / Apple Silicon | `darwin_arm64.tar.gz` |
| macOS / Intel | `darwin_amd64.tar.gz` |
| Linux / x64 | `linux_amd64.tar.gz` |
| Linux / ARM64 | `linux_arm64.tar.gz` |
| Windows / x64 | `windows_amd64.zip` |
| Windows / ARM64 | `windows_arm64.zip` |

[Full installation guide, checksums, updates, and troubleshooting →](docs/installation.md)

## Connect your AI agent

Install the CLI first. The integrations below let an agent call `jetformat` on the machine where the agent runs. They do not add a hosted conversion API or MCP server.

### Claude Code

```bash
claude plugin marketplace add jetformat/jetformat-agent
claude plugin install jetformat@jetformat
```

### Codex

```bash
codex plugin marketplace add jetformat/jetformat-agent
codex plugin add jetformat@jetformat
```

On clients without `codex plugin add`, add the marketplace, open the plugin browser, select **Jetformat**, and install it. Start a new session after installation.

### DeepSeek Harness

```bash
dsh plugin --profile web add github:jetformat/dsh-plugin
```

Use the profile in which you run your agent. This integration is for **DeepSeek Harness**, a local agent host; it is not an extension for the DeepSeek chat website.

Then ask your agent:

> Convert `proposal.docx` to PDF, render the first page as a preview, and tell me where both files were saved.

> Read `quarterly-report.xlsx` as structured data and summarize the visible worksheets.

[Agent setup, verification, and troubleshooting →](docs/agents.md)

## Local files, clear pricing

Office and PDF commands process your files locally. Sign-in, credit metering, and anonymous command telemetry contact Jetformat services; document contents, file names, and paths are not included in that telemetry. Disable it with `jetformat telemetry off`.

Reading, inspecting, and validating documents is free and requires no sign-in. Converting, rendering, and writing documents require `jetformat login` and consume credits. See [pricing](https://jetformat.com/pricing), [credits](https://jetformat.com/help/billing/credits), and [telemetry details](https://jetformat.com/help/security/telemetry).

## Know the boundaries

- Modern Office formats: `.docx`, `.xlsx`, `.pptx`. Legacy `.doc` / `.xls` / `.ppt` and macro-enabled formats are not supported.
- Text extraction and PDF-to-Word use an existing text layer; they do not perform OCR. PDF-to-Word does not promise pixel-perfect reconstruction.
- Excel-to-PDF includes visible worksheets. PDF page extraction accepts a contiguous range.
- Fonts affect layout. Use fonts you are licensed to use; see [font troubleshooting](docs/installation.md#fonts-and-layout).
- HTML-to-PDF is a separate renderer-backed workflow; see the [command reference](https://jetformat.com/docs/models) for its server requirements.

## Help and releases

[Open an issue](https://github.com/jetformat/jetformat/issues) for a reproducible bug or feature request. Include the CLI version, operating system, command, and error message. Use a small, non-sensitive sample when possible.

This is Jetformat's public documentation, downloads, and issue tracker. **The conversion engine is closed-source**; its source is not included here. [GitHub Actions](.github/workflows/release.yml) builds versioned release binaries from the private engine. [Release maintenance →](docs/releasing.md)

The CLI is governed by the [Jetformat terms](https://jetformat.com/terms). Agent adapters have their own licenses: [Claude / Codex](https://github.com/jetformat/jetformat-agent), [DeepSeek Harness](https://github.com/jetformat/dsh-plugin).
