# Release maintenance

This public repository holds documentation, release automation, and binary downloads. The conversion engine remains in the private `jetformat/jetformat-tool` repository.

## Build and publish a version

1. Test the engine in its private repository and push a stable version tag such as `v0.1.8`.
2. Open this repository's **Actions → Build and release Jetformat → Run workflow**. Select `main` and enter `0.1.8` (without `v`). Or run:

   ```bash
   gh workflow run release.yml -R jetformat/jetformat --ref main -f version=0.1.8
   ```

3. The workflow checks out that exact tag, builds production binaries for macOS/Linux/Windows on amd64/arm64, and packages six archives. It runs native smoke tests on Linux x64, macOS ARM64, and Windows x64. Other architectures are cross-compiled and their archive formats are checked.
4. After all checks pass, it writes `SHA256SUMS`, uploads assets to a draft release, and publishes the complete release. Existing releases are never overwritten.

The public repository's release tag identifies the documentation/workflow commit. The matching version tag in the private engine identifies the engine source. They are separate repositories and commits.

The first public download version is `0.1.7`, built from the existing private engine tag. Later engine development is not included until explicitly tagged and released.

## Engine access

The `engine-source` GitHub environment holds `ENGINE_SOURCE_TOKEN`, configured from the owner-authorized `allentatakai` GitHub credential. The public workflow uses this secret only to check out the private engine. Release uploads use the job-scoped `GITHUB_TOKEN`.

The environment permits deployments only from `main`. The workflow is manually dispatched, restricted to `main`, and never runs private builds for pull requests. Only the publish job receives `contents: write`; builds receive read-only public repository permissions.

Source is checked out on ephemeral GitHub-hosted runners, with credentials not persisted. Go caches are disabled. Compiler diagnostics remain in a temporary runner file because errors can quote source; neither the source nor that log is uploaded. Only six named binary archives and the checksum manifest reach Releases. A failed build must be reproduced and debugged in the private engine repository.

To rotate access, replace `ENGINE_SOURCE_TOKEN` in the `engine-source` environment with a GitHub token that can read `jetformat/jetformat-tool`. A fine-grained token limited to that repository with Contents: read is sufficient. Never paste tokens into a workflow, issue, or log. The current credential was configured by the repository owner; its GitHub account permissions are distinct from the workflow job permissions above.

## Failed runs

Inspect the failing job. A missing tag requires pushing the engine tag first; a checkout failure may require updating the environment token. Native smoke failures or compilation failures must be fixed in the private engine before releasing a new version.

If publication failed after creating a **draft**, inspect the draft and its assets before retrying. The workflow rejects any existing release (including drafts) to avoid replacing an already shipped build. Remove only the failed draft after confirming it was never published, then rerun. Never replace an existing public release's assets to fix an engine bug; publish a new version.

## npm and Homebrew

This workflow publishes GitHub download archives. npm and Homebrew have separate publishing flows, so their version may briefly differ from GitHub Releases.

For npm, the existing private publishing workflow accepts this repository as its binary source:

```bash
gh workflow run publish-npm.yml -R jetformat/jetformat-publish \
  -f version=0.1.8 -f binary_repo=jetformat/jetformat
```

For Homebrew, update the formula in `jetformat/homebrew-tap` with the new version, archive URLs under `jetformat/jetformat/releases/download/v<version>/`, and hashes from `SHA256SUMS`. Keep existing historical release assets available so pinned installations continue to work.
