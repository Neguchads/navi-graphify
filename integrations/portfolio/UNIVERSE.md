# NAVI Universe public data contract (v1)

Canonical catalog and daily snapshot producer. Consumers: [Homepage](https://github.com/Neguchads/github-homepage), [Abyss](https://github.com/Neguchads/navyv-abyss), [Profile](https://github.com/Neguchads/Neguchads).

Run universe_snapshot.py with --out, --sources (four source commit SHAs), optional --previous (90 daily aggregate rows) and --summary (verified numeric Graphify exports). No raw graphs or private metadata. Public originals exclude archived repositories, forks and the profile; all public owned repositories are counted separately. Languages count primary repository languages, not bytes. Open items include pull requests. Membership and integration edges are curated, never AST dependencies. Missing AST summaries are unavailable, not zero. GitHub profile orchestrates publication.
