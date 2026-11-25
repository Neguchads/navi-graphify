# NAVI Graphify roadmap

Status vocabulary: **implemented** means present in the referenced source; **pending validation** means evidence is still required; **planned** means no implementation is claimed. Maturity: experimental.

| Phase | Deliverable | Acceptance |
|---|---|---|
| 0 — Foundation | Existing engine and NAVI public bridge | Engine CI and bridge unit tests pass; preserve license and notices |
| 1 — Identity | Bilingual landing, NAVI SVGs, project docs | Render both pages; check references and attribution; review PR #8 |
| 2 — Catalog | Canonical repo names, consumer provenance and Core membership | Reconcile overlapping PRs #6/#7; verify catalog endpoints and downstream schema compatibility |
| 3 — Structural evidence | Public AST smoke test | Fresh public checkout, nonempty graph with valid counts, no raw export; review PR #2 |
| 4 — Knowledge bridge | Core reviewed local Graphify ingest | Reproduce digest approval, retrieval and revocation on a synthetic project; no public data flow |
| 5 — Consumer integration | Homepage / profile / optional Abyss | Pin reviewed source commits and validate public snapshot/rendering; verify missing summary handling |
| 6 — Distribution | Independent install/update and release policy | Review package identity, licensing, rollback, workflow guard and artifacts before publishing anything |

Phases 0–3 have existing source or open implementation proposals; they are not certified complete. Phases 4–6 require separate acceptance evidence across repositories. Core's local ingestion capability already exists; cross-project acceptance remains separate.

Do not merge conflicting catalog changes independently without reviewing their combined diff. Do not claim performance gains without a reproducible NAVI benchmark. Do not expose private graphs to demonstrate the public presentation.

See [handoff](HANDOFF.md) for the continuation state and [architecture](navi/ARCHITECTURE.md) for ownership.
