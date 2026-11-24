import unittest
from universe_snapshot import make_snapshot
class UniverseTests(unittest.TestCase):
    def test_public_only_and_history(self):
        repo=dict(name="chad-recomp",full_name="Neguchads/chad-recomp",owner={"login":"Neguchads"},private=False,visibility="public",fork=False,archived=False,stargazers_count=5,forks_count=2,open_issues_count=3,language="C",pushed_at=None)
        d=make_snapshot([repo,dict(repo,name="secret",private=True)],{"followers":7},"2026-11-24",[],{})
        self.assertEqual(d["totals"]["stars"],5)
        self.assertEqual(d["totals"]["public_repositories"],1)
        self.assertNotIn("secret",str(d))
        self.assertEqual(d["history"][0]["date"],d["date"])
        self.assertEqual(d["featured"],["chad-recomp"])
