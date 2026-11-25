# NAVI Graphify handoff

Snapshot: 2026-11-25. This is a dated continuation record, not live CI status.

## Goal

Make NAVI Graphify the knowledge layer of NAVI-OS, preserve engine compatibility and isolate public portfolio data from private project knowledge.

## References at handoff

- Default branch: `v8`; observed base before identity changes: `7225f0ebad7d0e8f6a8e47d004158a64588b41ee`.
- [PR #8](https://github.com/Neguchads/navi-graphify/pull/8): identity and project documentation, branch `docs/navi-graphify-identity`.
- [PR #6](https://github.com/Neguchads/navi-graphify/pull/6) and [PR #7](https://github.com/Neguchads/navi-graphify/pull/7): overlapping public catalog/name changes; reconcile before merge.
- [PR #2](https://github.com/Neguchads/navi-graphify/pull/2): end-to-end public AST proposal; re-evaluate against current base.

## Decisions

Keep the inherited engine, package name and CLI. Publish our presentation without upstream commercial promotion. Preserve upstream author and license notices. Treat catalog edges as editorial and local graph edges as structural/inferred. Keep Core/NEF policy portable rather than duplicating a second framework.

## Evidence and blockers

The first identity commit had 44 local reference checks and local SVG checks; engine CI was still running when reviewed, while the NAVI pilot, skillgen, pi-guard and security-scan jobs had succeeded. These results apply only to that commit and must not be reused as final evidence for subsequent commits.

No end-to-end engine run or final GitHub render has been established by this document. The public catalog on the original base still contains old names; those changes are owned by PRs #6/#7. Publishing the inherited PyPI package is not approved. Check current PR status before acting.

## Next steps

1. Check the latest PR #8 head and its CI; review documentation and SVG rendering.
2. Merge identity only after accepted gates, then reconcile the catalog PRs without losing Core membership or canonical names.
3. Rebase/review the AST smoke proposal and run targeted validation.
4. Validate public snapshots with consumers and record exact source commits.
5. Record actual commands, results, limitations and next action in the handoff.

Use [NEF](https://github.com/Neguchads/navi-core/blob/main/docs/NEF.md) and the [agent interface](https://github.com/Neguchads/navi-core/blob/main/docs/UNIVERSAL_AGENT_INTERFACE.md) for portable context. No private sessions, credentials or graph data belong here.
