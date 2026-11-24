# NAVI public portfolio bridge

NAVI owns the versioned public catalog. The catalog is editorial sector membership and explicit integration relationships, **not** an extracted dependency graph. The Homepage renderer consumes this contract; the profile displays its SVG and links. Detailed code graphs, MCP, semantic memory and private repositories remain local.

## Public structural summary

From a virtual environment with this fork installed, run:

```powershell
python integrations/portfolio/export_public.py chad-recomp --out public-summary.json
```

The exporter verifies the selected repo anonymously, clones a fresh public checkout into a temporary directory, uses the installed Graphify CLI in code-only mode with backend disabled, and emits only numeric node/edge/community and confidence counts plus the public slug and commit. It does not accept arbitrary local graph paths. The temporary raw graph is removed on exit. Inspect the JSON before sharing; this is not a guarantee that a formerly public repository remains public forever. Never publish raw graph.json, GRAPH_REPORT.md, graph.html, credentials or private-derived data from other workflows.

The public catalog is versioned separately from Graphify's internal graph schema. No cloud service or API token is required. Run `python -m unittest discover -s integrations/portfolio -p 'test_*.py'` for offline adapter tests. The actual AST scan requires Git, Python and the fork's installed dependencies.

Consumers: [github-homepage](https://github.com/Neguchads/github-homepage) · [Neguchads profile](https://github.com/Neguchads/Neguchads).
