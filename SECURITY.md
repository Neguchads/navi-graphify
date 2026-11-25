# Security Policy — NAVI Graphify

NAVI Graphify is an experimental independent fork. The inherited engine threat model below is reference material, not a security certification of the NAVI integration.

## NAVI-specific reporting and data boundaries

Use [fork security advisories](https://github.com/Neguchads/navi-graphify/security/advisories) for private reporting if enabled. If a private channel is unavailable, request a private channel without disclosing vulnerability details publicly. Upstream-only vulnerabilities may also require coordinated reporting to the original maintainers.

The public portfolio bridge validates catalog membership and public visibility, clones a fresh public checkout with isolated Git configuration, disables semantic extraction and reconstructs numeric-only output. Optional metadata credentials are not forwarded to the extraction subprocess. These are controls, not guarantees against every leak. Never publish raw local graphs, cache, private source paths, agent sessions or unreviewed evidence. Check visibility and provenance again before publication. See [NAVI architecture](docs/navi/ARCHITECTURE.md) and [operations](docs/navi/OPERATIONS.md).

## Inherited engine version policy

| Version | Supported |
|---------|-----------|
| Latest 0.9.x | Yes       |
| < 0.9        | No        |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report security issues via a verified private channel as described above. Please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

Coordinate disclosure and remediation privately; no response-time commitment is established by this policy.

## Security Model

graphify is a **local development tool**. It runs as a Claude Code skill and optionally as a local MCP stdio server. Its network boundaries are: AST/code extraction is local and deterministic; semantic extraction may send content to a configured model/backend; `ingest` uses explicit outbound fetch; HTTP MCP is an opt-in network listener.

### Threat Surface

| Vector | Mitigation |
|--------|-----------|
| SSRF via URL fetch | `security.validate_url()` allows only `http` and `https` schemes, blocks private/loopback/link-local IPs, and blocks cloud metadata endpoints. It also rejects embedded credentials, port 0, and missing hostnames. Redirect targets are re-validated. All fetch paths including tweet oEmbed go through `safe_fetch()`. |
| Oversized downloads | `safe_fetch()` streams responses and aborts at 50 MB. `safe_fetch_text()` aborts at 10 MB. |
| Non-2xx HTTP responses | `safe_fetch()` raises `HTTPError` on non-2xx status codes - error pages are not silently treated as content. |
| Path traversal in MCP server | `security.validate_graph_path()` resolves paths and requires them to be inside `graphify-out/`. Also requires the `graphify-out/` directory to exist. |
| XSS in graph HTML output | `security.sanitize_label()` strips control characters and caps at 256 chars. (Note: HTML escaping happens separately in the HTML exporter, not in `sanitize_label()`). |
| Prompt injection via node labels | `sanitize_label()` also applied to MCP text output - node labels from user-controlled source files cannot break the text format returned to agents. |
| Prompt injection via source file content | During the semantic pass, source files are attacker-controlled text mixed into the LLM context. `_read_files()` in `llm.py` wraps every file in a hash-stamped `<untrusted_source path=... sha256=...>` delimiter block, the extraction system prompt instructs the model to treat that block as inert data and never as instructions, and `_neutralise_injection_sentinels()` defangs known chat-template/jailbreak tokens (`<\|im_start\|>`, `[INST]`, `<<SYS>>`, forged `</untrusted_source>`, etc.) before insertion. This is the table-stakes defense (issue #1210): it does not make injection impossible, but changes it from "works on first try" to "requires evasion." |
| YAML frontmatter injection | `_yaml_str()` escapes backslashes, double quotes, and newlines before embedding user-controlled strings (webpage titles, query questions) in YAML frontmatter. |
| Encoding crashes on source files | All tree-sitter byte slices decoded with `errors="replace"` - non-UTF-8 source files degrade gracefully instead of crashing extraction. |
| Symlink traversal | `os.walk(..., followlinks=False)` is parameterized to avoid unchecked traversal where appropriate. |
| Symlink escape during ingest | `ingest` checks names with `lstat` and creates capture files exclusively. If another entry takes the selected name, the capture retries with a numbered name. |
| Credentials in persisted text | `security.redact_secrets()` replaces credential-shaped substrings in labels and rationale text before they are written to `graph.json`. |
| Destructive uninstall | `uninstall --purge` refuses to delete the project folder, the home directory, or a filesystem root, including when `GRAPHIFY_OUT` points outside the project. |
| Corrupted graph.json | `_load_graph()` in `serve.py` wraps `json.JSONDecodeError` and prints a clear recovery message instead of crashing. |

### What graphify does NOT do

- Does not run a network listener by default (stdio transport); `--transport http` is opt-in, documented in the README, and binds to `127.0.0.1` unless `--host 0.0.0.0` is passed
- Does not execute code from source files (tree-sitter parses ASTs - no eval/exec)
- Does not use `shell=True` in any subprocess call
- Does not store credentials or API keys

### Optional network calls

- `ingest` subcommand: fetches URLs explicitly provided by the user
- PDF extraction: reads local files only (pypdf does not make network calls)
- watch mode: local filesystem events only (watchdog does not make network calls)
