import json
import tempfile
import unittest
from pathlib import Path
from review_manifest import validate, scan


def sample(experiment):
    (experiment / "demo.py").write_text("print('ok')\n", encoding="utf-8")
    return {"schema":"umd.playground.review.v1","id":experiment.name,"title":"Review",
            "status":"REVIEW_READY","question":"Does it work?","summary":"Scoped result",
            "evidence":[{"kind":"EXECUTION","environment":"Python","observation":"ok","source":"demo.py"}],
            "limitations":["No Lab run"],"next_actions":["Consider outcome"],
            "recommended_action":"REVIEW","recommendation_reason":"Needs owner decision",
            "files":[{"path":"demo.py","label":"Source"}],"issue_number":None}


class ReviewManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.experiment = self.root / "test_experiment"
        self.experiment.mkdir()

    def test_valid(self):
        self.assertEqual([], validate(sample(self.experiment), self.experiment))

    def test_missing_source(self):
        d = sample(self.experiment)
        d["files"] = [{"path":"missing.md","label":"Source"}]
        self.assertTrue(any("missing" in e for e in validate(d,self.experiment)))

    def test_path_traversal(self):
        for path in ("../secret", "/tmp/secrets", "a/../demo.py", "a//demo.py", "a\\demo.py"):
            with self.subTest(path=path):
                d = sample(self.experiment)
                d["files"] = [{"path":path,"label":"Forbidden"}]
                self.assertTrue(validate(d,self.experiment))

    def test_recommendation_not_approval(self):
        d = sample(self.experiment)
        d["recommended_action"] = "EXTRACT"
        self.assertEqual([],validate(d,self.experiment))
        self.assertNotIn("owner_approved", d)

    def test_bad_evidence_and_status(self):
        d = sample(self.experiment)
        d["evidence"] = [{"kind":"EXECUTION"}]
        d["status"] = "EXTRACTED"
        self.assertEqual(2, len(validate(d,self.experiment)))

    def test_scan(self):
        d = sample(self.experiment)
        (self.experiment / "review.json").write_text(json.dumps(d),encoding="utf-8")
        results = scan(self.root)
        self.assertEqual(1,len(results))
        self.assertEqual([],results[0][1])


if __name__ == "__main__":
    unittest.main()
