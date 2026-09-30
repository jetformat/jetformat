# Jetformat for AI agents

[Home](../README.md) · [中文](../README.zh-CN.md) · [Install the CLI](installation.md)

The agent integrations teach your agent to invoke the local `jetformat` executable. Install the CLI in the same environment where the agent executes commands, including inside a container or remote workspace when applicable.

```bash
npm install -g jetformat
jetformat --version
jetformat login
```

Sign-in is needed for paid commands; reading and validation work without it. Use `jetformat login --device-auth` on a headless machine.

## Claude Code

Run in your terminal:

```bash
claude plugin marketplace add jetformat/jetformat-agent
claude plugin install jetformat@jetformat
claude plugin list
```

Start a new Claude Code session after installation. In an interactive Claude Code session, the corresponding commands are `/plugin marketplace add jetformat/jetformat-agent` and `/plugin install jetformat@jetformat`.

Plugin source: [jetformat-agent](https://github.com/jetformat/jetformat-agent). Host reference: [Claude Code plugin installation](https://code.claude.com/docs/en/discover-plugins).

## Codex

Add the Jetformat marketplace and install the plugin:

```bash
codex plugin marketplace add jetformat/jetformat-agent
codex plugin add jetformat@jetformat
codex plugin list
```

Some Codex clients expose installation through the plugin browser instead of `plugin add`. If that subcommand is unavailable, add the marketplace, open the plugin browser, find **Jetformat**, and install it. Start a new session before testing the skill. Adding a marketplace alone is not the same as installing its plugin.

Plugin source: [jetformat-agent](https://github.com/jetformat/jetformat-agent). Host reference: [OpenAI plugin packaging and marketplace setup](https://developers.openai.com/plugins/build/plugins). CLI command availability can be checked with `codex plugin --help`.

## DeepSeek Harness

With DeepSeek Harness installed:

```bash
dsh plugin --profile web add github:jetformat/dsh-plugin
```

Use the profile you actually run; replace `web` if necessary. Follow the host's dependency/build prompts, then restart that profile. This is an integration with the **local DeepSeek Harness agent runtime**, not the DeepSeek chat website or a direct DeepSeek model API integration.

The adapter provides:

| Tool | Purpose |
| --- | --- |
| `jetformat_to_pdf` | Convert DOCX, XLSX, or PPTX to PDF. |
| `jetformat_text` | Extract text from supported documents. |
| `jetformat_validate` | Validate supported files. |
| `jetformat_pdf` | Inspect, merge, extract, or render PDFs. |

Set `JETFORMAT_BIN` if the adapter should use an executable outside `PATH`. The adapter was tested with DeepSeek Harness `0.1.5-rc.3`; consult its repository for compatibility updates.

Plugin source: [dsh-plugin](https://github.com/jetformat/dsh-plugin). Host reference: [DeepSeek Harness plugin installation](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish).

## Verify with a real document

First try a free task:

> Use Jetformat to validate `report.docx` and extract its text as Markdown. Report any CLI errors.

Then, after signing in:

> Use Jetformat to convert `report.docx` to `output/report.pdf`, inspect its page count, and render the first page into `output/preview`. Tell me the paths of the generated files.

Give the agent actual input files. The integration should invoke `jetformat`, check the exit status, and report real output paths. It should not claim a conversion succeeded when the CLI failed.

## Permissions and privacy

The agent needs permission to run the CLI and read/write the selected paths. Office and PDF processing happens locally. Login, credit checks, and anonymous usage telemetry contact Jetformat services. Telemetry contains command metadata, not document contents, file names, or paths. Disable it with `jetformat telemetry off`.

These adapters do not require an MCP endpoint. If your host only accepts a custom instruction, give it the [model command reference](https://jetformat.com/docs/models); it still needs a real local shell and the installed CLI.
