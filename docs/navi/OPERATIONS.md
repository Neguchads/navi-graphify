# NAVI Graphify operations

## Install the fork

Requires Git and Python 3.11.5–3.14. Review the checkout and dependencies first.

```sh
git clone https://github.com/Neguchads/navi-graphify.git
cd navi-graphify
python -m venv .venv
# Activate for your shell.
python -m pip install .
graphify --help
```

PowerShell activation: `.\.venv\Scripts\Activate.ps1`. POSIX: `source .venv/bin/activate`. For reproducibility, check out a reviewed commit before installing. Upstream PyPI `graphifyy` does not include the NAVI portfolio integration. Do not install the fork over an existing shared upstream environment.

## Local graph and agent integration

In a trusted project:

```sh
graphify extract . --code-only
graphify query "What are the main components?"
graphify update .
```

Review ignore rules and graph output before sharing. Use `graphify --help` and the inherited [technical reference](https://github.com/Neguchads/navi-graphify/blob/7225f0ebad7d0e8f6a8e47d004158a64588b41ee/README.md) for platform-specific commands. Optional project-level setup: `graphify install --project --platform codex`. This modifies project guidance; inspect the changes. The default Claude integration and local MCP are alternatives, not extra mandatory subscriptions. Install the MCP extra from the fork (`python -m pip install ".[mcp]"`) if required.

For reviewed local ingestion into Core, follow the [AKE guide](https://github.com/Neguchads/navi-core/blob/main/docs/ADAPTIVE_KNOWLEDGE.md). Do not copy raw project graphs into the public portfolio.

## Public bridge

Run from the fork checkout:

```sh
python integrations/portfolio/export_public.py chad-recomp --out public-summary.json
python -m unittest discover -s integrations/portfolio -p "test_*.py"
```

The exporter requires network access to GitHub, Git and installed engine dependencies. The unit suite is offline; it is not an end-to-end AST integration test. The public summary should be reviewed for exact allowlisted fields and public visibility. The snapshot CLI requires an explicit source-commit JSON and optional reviewed summaries; see [Universe contract](../../integrations/portfolio/UNIVERSE.md).

## Verification before merge

- Run the bridge unit suite for integration changes.
- Use a trusted environment and run engine CI parity (`uv sync --all-extras --frozen`, `uv run --frozen pytest tests/ -q`) for engine-affecting changes.
- Verify both landing pages and SVGs in GitHub; check local links and canonical repository names.
- For generated skills follow [CONTRIBUTING.md](../../CONTRIBUTING.md) and the skill generator checks.
- Check GitHub Actions on the actual proposed commit; do not treat queued, skipped or failed tests as evidence of success.

## Recovery and distribution

Record the last reviewed commit and preserve local data outside Git before updates. Revert a faulty integration PR or recreate the isolated environment at the reviewed commit. Do not delete graph caches or use purge without backing up any needed local data. No NAVI PyPI release is authorized by this guide. Follow the [release policy](../../RELEASING.md).
