"""NAVI daily public snapshot. No private enumeration or raw graph export."""
import argparse, collections, datetime as dt, json, os, pathlib, re, urllib.request
from export_public import catalog

OWNER = "Neguchads"
def api(path):
    headers = {"User-Agent": "NAVI-Universe", "Accept": "application/vnd.github+json"}
    token = os.environ.get("NAVI_PUBLIC_METADATA_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com"+path, headers=headers), timeout=30) as response:
        return json.load(response)

def count(item, field):
    n = item[field]
    if type(n) is not int or n < 0:
        raise ValueError("Invalid metric: "+field)
    return n

def public(item):
    return (item.get("private") is False and item.get("visibility") == "public"
            and item.get("owner", {}).get("login", "").casefold() == OWNER.casefold()
            and item.get("full_name", "").casefold() == (OWNER+"/"+item.get("name","")).casefold())

def make_snapshot(items, profile, day, history, sources, summaries=()):
    repos = {}
    for item in items:
        if not public(item):
            continue
        name = item["name"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", name):
            raise ValueError("Invalid repository slug")
        repos[name.casefold()] = {"slug":name, "stars":count(item,"stargazers_count"),
            "forks":count(item,"forks_count"), "open_items":count(item,"open_issues_count"),
            "language":item.get("language"), "pushed_at":item.get("pushed_at"),
            "fork":item["fork"] is True, "archived":item["archived"] is True}
    c = catalog()
    sectors = []
    approved = set()
    for s in c["sectors"]:
        projects = []
        for slug, title in s["repos"]:
            if slug.casefold() not in repos:
                continue
            projects.append({**repos[slug.casefold()], "title":title})
            approved.add(slug.casefold())
        sectors.append({k:s[k] for k in ("id","en","pt","color","pos")} | {"projects":projects})
    original = [v for v in repos.values() if not v["fork"] and not v["archived"] and v["slug"].casefold()!=OWNER.casefold()]
    languages = collections.Counter(v["language"] for v in original if v["language"])
    totals = {"public_repositories":len(repos), "active_originals":len(original),
        "stars":sum(v["stars"] for v in original), "forks":sum(v["forks"] for v in original),
        "open_items":sum(v["open_items"] for v in original),
        "followers":count(profile,"followers")}
    metrics = {}
    for m in summaries:
        slug = m.get("repository","")
        keys = {"schema_version","scope","repository","commit","nodes","edges","communities","confidence"}
        if set(m)!=keys or m["scope"]!="public-code-only" or m["schema_version"]!=1 or slug.casefold() not in approved or not re.fullmatch(r"[a-f0-9]{40}",m["commit"]):
            raise ValueError("Invalid structural summary")
        if set(m["confidence"])!={"EXTRACTED","INFERRED","OTHER"} or any(type(n) is not int or n<0 for n in [m["nodes"],m["edges"],m["communities"],*m["confidence"].values()]) or sum(m["confidence"].values())!=m["edges"]:
            raise ValueError("Invalid structural counts")
        metrics[slug] = m
    rows = {r["date"]:r for r in history if isinstance(r,dict) and set(r)=={"date",*totals} and all(type(r[k]) is int and r[k]>=0 for k in totals) and re.fullmatch(r"\d{4}-\d{2}-\d{2}",r["date"])}
    rows[day] = {"date":day,**totals}
    return {"schema_version":1,"scope":"public-only","owner":OWNER,"date":day,"sources":sources,
        "totals":totals,"languages":dict(languages.most_common()),"history":[rows[k] for k in sorted(rows)[-90:]],
        "sectors":sectors,"integrations":[e for e in c["integrations"] if e["source"].casefold() in approved and e["target"].casefold() in approved],
        "structural":metrics,"featured":[s for s in ("chad-recomp","cdos-nintendods-recomp","ccod-xbox-recomp","csotn-saturn-recomp","starlight-bi","spec-to-proof") if s.casefold() in approved]}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=pathlib.Path,required=True)
    p.add_argument("--previous",type=pathlib.Path)
    p.add_argument("--sources",type=pathlib.Path,required=True)
    p.add_argument("--summary",type=pathlib.Path,action="append",default=[])
    a=p.parse_args()
    items=[]
    for page in range(1,101):
        batch=api(f"/users/{OWNER}/repos?type=owner&per_page=100&page={page}")
        if not isinstance(batch,list): raise ValueError("Invalid public API response")
        items.extend(batch)
        if len(batch)<100: break
    else: raise ValueError("Pagination limit")
    old=json.loads(a.previous.read_text()) if a.previous and a.previous.exists() else {}
    sources=json.loads(a.sources.read_text())
    if set(sources)!={"navi-graphify","github-homepage","navi-abyss","Neguchads"} or not all(re.fullmatch(r"[a-f0-9]{40}",v) for v in sources.values()):
        raise ValueError("Invalid source provenance")
    data=make_snapshot(items,api("/users/"+OWNER),dt.datetime.now(dt.timezone.utc).date().isoformat(),old.get("history",[]),sources,[json.loads(x.read_text()) for x in a.summary])
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__": main()
