# NAVI Graphify — engineering documentation

Independent integrated fork of Graphify. Development preview, not production certification.

| Document | Purpose |
|---|---|
| [Architecture](ARCHITECTURE.md) | Ownership, local/public boundaries and data flow |
| [Operations](OPERATIONS.md) | Installation, graph usage, export, verification and recovery |
| [Roadmap](../ROADMAP.md) | Acceptance criteria and pending work |
| [Handoff](../HANDOFF.md) | Reproducible continuation and current integration status |
| [Decisions](DECISIONS.md) | Architectural decisions and trade-offs |
| [NAVI pilot](../NAVI_PILOT.md) | Complementary engineering gate |
| [Portfolio bridge](../../integrations/portfolio/README.md) | Public exporter contract |
| [Universe contract](../../integrations/portfolio/UNIVERSE.md) | Public snapshot schema |
| [Engine architecture](../../ARCHITECTURE.md) | Inherited technical reference |
| [Security](../../SECURITY.md) | Security policy and threat model |
| [Release policy](../../RELEASING.md) | Fork distribution boundaries |

Framework references: [NEF](https://github.com/Neguchads/navi-core/blob/main/docs/NEF.md), [Universal Agent Interface](https://github.com/Neguchads/navi-core/blob/main/docs/UNIVERSAL_AGENT_INTERFACE.md), [Adaptive Knowledge Engine](https://github.com/Neguchads/navi-core/blob/main/docs/ADAPTIVE_KNOWLEDGE.md).

The local project manifest is [`.navi/project.toml`](../../.navi/project.toml). It declares experimental maturity and a complementary Python verification profile. It does not authorize publication of local knowledge.
