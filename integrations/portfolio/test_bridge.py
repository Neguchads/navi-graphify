import unittest
from export_public import summarize, catalog

class BridgeTests(unittest.TestCase):
    def test_no_raw_graph_data(self):
        graph = {"graph": {"schema_version": 1, "secret": "hidden"},
                 "nodes": [{"id": "private/path", "community": 1}, {"label": "SECRET", "community": 2}],
                 "links": [{"confidence": "EXTRACTED", "source": "private/path"},
                           {"confidence": "INFERRED"}, {"confidence": "unexpected"}]}
        result = summarize(graph, "chad-recomp", "a"*40)
        self.assertEqual(result["nodes"], 2)
        self.assertEqual(result["edges"], 3)
        self.assertEqual(result["communities"], 2)
        self.assertEqual(result["confidence"], {"EXTRACTED": 1, "INFERRED": 1, "OTHER": 1})
        self.assertNotIn("private/path", str(result))
        self.assertNotIn("SECRET", str(result))
        self.assertNotIn("hidden", str(result))

    def test_reject_unapproved_and_malformed(self):
        with self.assertRaises(ValueError):
            summarize({}, "private-repo", "a"*40)
        with self.assertRaises(ValueError):
            summarize({"nodes": [], "links": []}, "chad-recomp", "a"*40)

    def test_catalog(self):
        data = catalog()
        names = [r[0] for s in data["sectors"] for r in s["repos"]]
        self.assertEqual(len(names), len(set(names)))
        for link in data["integrations"]:
            self.assertIn(link["source"], names)
            self.assertIn(link["target"], names)
