# NAVI Graphify decisions

| ID | Decision | Rationale / consequence |
|---|---|---|
| NG-001 | Preserve upstream engine, CLI and package identity | Minimize upstream merge and host compatibility cost; independent distribution needs explicit migration |
| NG-002 | NAVI identity in public presentation | No borrowed awards, downloads or commercial claims; upstream attribution remains |
| NG-003 | Separate local graph from public catalog | Prevent private source/agent data from entering public artifacts; curated edges are not dependencies |
| NG-004 | Public summaries use numeric allowlist | Reduce disclosure surface; no arbitrary local graph import |
| NG-005 | Core owns engineering policy and reviewed local knowledge | Avoid duplicate governance; Graphify is an optional source, not a mandatory provider |
| NG-006 | Keep full upstream CI plus complementary NAVI gate | A bridge test is not evidence of engine correctness |
| NG-007 | Preserve historical reference at a pinned commit | Retain detailed original documentation and translations without upstream marketing on the landing page |

Revisit decisions through a reviewed PR with evidence and a rollback strategy. The inherited Apache/MIT terms and NOTICE remain authoritative.
