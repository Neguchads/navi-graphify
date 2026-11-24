"""Public-only Graphify bridge. Never accepts a local graph or private checkout."""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OWNER = "Neguchads"


def catalog():
    return json.loads((HERE / "catalog.json").read_text(encoding="utf-8"))


def public_repo(slug):
    if slug not in {r[0] for s in catalog()["sectors"] for r in s["repos"]}:
        raise ValueError("Repository not approved in public catalog")
    # Anonymous API request; no local GitHub credentials or authorization header.
    req = urllib.request.Request(f"https://api.github.com/repos/{OWNER}/{slug}",
                                 headers={"User-Agent": "NAVI-public-bridge",
                                          "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        info = json.load(response)
    if (info.get("private") is not False or info.get("visibility") != "public"
            or info.get("full_name", "").lower() != f"{OWNER}/{slug}".lower()):
        raise ValueError("Repository is not verified public")
    return info


def summarize(graph, slug, commit):
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("Invalid commit")
    if slug not in {r[0] for s in catalog()["sectors"] for r in s["repos"]}:
        raise ValueError("Unapproved repository")
    if not isinstance(graph.get("graph"), dict) or "schema_version" not in graph["graph"]:
        raise ValueError("Missing Graphify schema version")
    nodes, links = graph.get("nodes"), graph.get("links")
    if not isinstance(nodes, list) or not isinstance(links, list):
        raise ValueError("Unsupported graph format")
    if any(not isinstance(x, dict) for x in nodes + links):
        raise ValueError("Invalid graph records")
    counts = {"EXTRACTED": 0, "INFERRED": 0, "OTHER": 0}
    for link in links:
        confidence = link.get("confidence")
        counts[confidence if confidence in ("EXTRACTED", "INFERRED") else "OTHER"] += 1
    communities = {n["community"] for n in nodes if type(n.get("community")) is int}
    # Reconstruct allowlisted numeric output. No IDs, source paths, labels,
    # prompts, edge endpoints, arbitrary metadata, or source text are copied.
    return {"schema_version": 1, "scope": "public-code-only", "repository": slug,
            "commit": commit, "nodes": len(nodes), "edges": len(links),
            "communities": len(communities), "confidence": counts}


def scan(slug):
    public_repo(slug)
    with tempfile.TemporaryDirectory(prefix="navi-public-") as tmp:
        root = pathlib.Path(tmp)
        source = root / "source"
        out = root / "out"
        env = {k: v for k, v in os.environ.items()
               if k in ("PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "TMPDIR", "PATHEXT", "LANG", "LC_ALL")}
        env.update({"HOME": tmp, "USERPROFILE": tmp, "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": str(root / "no-git-config"),
                    "GIT_TERMINAL_PROMPT": "0", "GRAPHIFY_BACKEND": "none"})
        subprocess.run(["git", "-c", "credential.helper=", "-c", "core.hooksPath=" + str(root / "no-hooks"),
                        "clone", "--depth=1", "--no-recurse-submodules",
                        f"https://github.com/{OWNER}/{slug}.git", str(source)],
                       env=env, check=True, timeout=300)
        commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"],
                                         env=env, text=True).strip()
        subprocess.run([sys.executable, "-m", "graphify", "extract", str(source),
                        "--code-only", "--out", str(out), "--max-workers", "2"],
                       env=env, check=True, timeout=900)
        graph_path = out / "graphify-out" / "graph.json"
        if graph_path.stat().st_size > 128 * 1024 * 1024:
            raise ValueError("Graph exceeds bridge size cap")
        result = summarize(json.loads(graph_path.read_text(encoding="utf-8")), slug, commit)
        public_repo(slug)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", help="Explicit public catalog slug")
    parser.add_argument("--out", required=True, type=pathlib.Path)
    args = parser.parse_args()
    data = scan(args.repository)
    args.out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
