# NAVI Graphify release policy

NAVI Graphify is an independent development-preview fork. The inherited Python package is still named `graphifyy` and the executable is `graphify`. **Do not publish to upstream PyPI or create releases in the upstream repository.** No independent NAVI distribution namespace is established by this policy.

## Review gates

1. Identify the exact reviewed fork commit and intended artifact; use branch `v8` as the integration base.
2. Verify relevant engine CI, public portfolio unit tests, security checks, licenses and notice preservation.
3. Review changes to package metadata, generated skills and dependencies; keep the lock consistent if changed.
4. Build and inspect artifacts in an isolated trusted environment; do not upload before approval.
5. Record the commit, verification evidence, limitations, release notes and rollback instructions.

The inherited `.github/workflows/publish.yml` is configured for upstream trusted publishing. Its presence is not permission to use it. Before creating a fork release or triggering publish manually, explicitly disable or isolate that upstream publication path and review any future independent workflow. Use a reviewed source checkout for installation today.

The historical upstream release process is preserved at [the original revision](https://github.com/Neguchads/navi-graphify/blob/7225f0ebad7d0e8f6a8e47d004158a64588b41ee/RELEASING.md) for reference only. See [operations](docs/navi/OPERATIONS.md), [security](SECURITY.md) and [roadmap](docs/ROADMAP.md).
