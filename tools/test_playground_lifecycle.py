"""Focused tests for the exact public Playground lifecycle module (no network)."""
import argparse
import base64
import hashlib
import unittest
from unittest.mock import patch

import playground_lifecycle as lc

HEAD = "a" * 40
COMMIT = "b" * 40
ID = "experiment_001"


def args():
    return argparse.Namespace(id=ID, expected_head=HEAD, owner_approved=True,
        select=["README.md"], question="what?", author="Cody-directed session",
        consumer="Lab research intake", findings="Finding", limitations="Limitations",
        next_action="Investigate", proof="One observed run")


def packet():
    a = args()
    return lc.build_packet(a.id, a.expected_head, [("README.md", b"foo")],
        question=a.question, author=a.author, consumer=a.consumer,
        findings=a.findings, limitations=a.limitations,
        next_action=a.next_action, proof=a.proof).encode("utf-8")


class LifecycleTests(unittest.TestCase):
    def test_safe_ids_and_selection(self):
        for bad in ("", "../lab", "/tmp/foo", "a", "a/b", "A_upper"):
            with self.subTest(id=bad), self.assertRaises(lc.LifecycleError):
                lc.validate_id(bad)
        for bad in ("../secret", "/etc/passwd", r"a\..\b", "file/../secret", ".", "./foo", "foo//bar"):
            with self.subTest(path=bad), self.assertRaises(lc.LifecycleError):
                lc.validate_selection([bad])
        self.assertEqual(["README.md", "demo.py"],
                         lc.validate_selection(["README.md", "demo.py", "README.md"]))

    def test_packet_is_deterministic_and_precisely_attributed(self):
        first = packet()
        self.assertEqual(first, packet())
        self.assertIn(hashlib.sha256(b"foo").hexdigest().encode(), first)
        self.assertIn(HEAD.encode(), first)
        self.assertIn(b"NOT implementation", first)

    def test_owner_approval_refuses_before_contacting_remote(self):
        a = args()
        a.owner_approved = False
        with patch.object(lc, "get_head") as remote:
            with self.assertRaises(lc.LifecycleError):
                lc.extract(a)
            remote.assert_not_called()

    def test_live_status_lists_only_active_experiment_directories(self):
        tree = [
            {"path": "experiments/experiment_001/a.py", "type": "blob", "size": 4},
            {"path": "experiments/experiment_001/b.md", "type": "blob", "size": 8},
            {"path": "experiments/experiment_002/a.py", "type": "blob", "size": 5},
            {"path": "experiments/README.md", "type": "blob", "size": 123},
            {"path": "notes/foo.md", "type": "blob", "size": 5},
        ]
        with patch.object(lc, "get_head", return_value=HEAD), patch.object(lc, "get_tree", return_value=(COMMIT, tree)):
            result = lc.status()
        self.assertEqual("READ_ONLY", result["result"])
        self.assertEqual([{"id": "experiment_001", "files": 2, "bytes": 12},
                          {"id": "experiment_002", "files": 1, "bytes": 5}], result["active_experiments"])

    def test_preview_has_no_write_and_exact_digest(self):
        with patch.object(lc, "get_head", return_value=HEAD), patch.object(lc, "load_selection", return_value=[("README.md", b"foo")]), patch.object(lc, "api") as mutation:
            result = lc.preview(args())
        mutation.assert_not_called()
        self.assertTrue(result["no_write_performed"])
        self.assertEqual(hashlib.sha256(packet()).hexdigest(), result["packet_sha256"])

    def test_preview_refuses_stale_head(self):
        with patch.object(lc, "get_head", return_value=COMMIT), patch.object(lc, "load_selection") as selected:
            with self.assertRaisesRegex(lc.LifecycleError, "differs"):
                lc.preview(args())
            selected.assert_not_called()

    def test_corrupt_blob_fails_integrity_check(self):
        fake = {"type": "file", "encoding": "base64", "size": 3,
                "content": base64.b64encode(b"foo").decode(), "sha": "f" * 40}
        with patch.object(lc, "api", return_value=fake):
            with self.assertRaisesRegex(lc.LifecycleError, "Git blob SHA"):
                lc.read_bytes(lc.PLAYGROUND, "file", HEAD)

    def test_valid_blob_has_verified_git_sha(self):
        data = b"foo"
        git_sha = hashlib.sha1(b"blob 3\0" + data).hexdigest()
        fake = {"type": "file", "encoding": "base64", "size": 3,
                "content": base64.b64encode(data).decode() + "\n", "sha": git_sha}
        with patch.object(lc, "api", return_value=fake):
            self.assertEqual(data, lc.read_bytes(lc.PLAYGROUND, "file", HEAD))

    def test_extract_readback_mismatch_keeps_source(self):
        a = args()
        def api(method, path, data=None):
            if method == "PUT": return {"commit": {"sha": COMMIT}}
            raise AssertionError((method, path))
        def read(repo, path, sha, **kwargs):
            if path.endswith("/README.md"): return b"owner present"
            if path.endswith(".md"): return b"wrong bytes"
            raise lc.GitHubNotFound("not found")
        with patch.object(lc, "get_head", return_value=HEAD), patch.object(lc, "load_selection", return_value=[("README.md", b"foo")]), patch.object(lc, "api", side_effect=api), patch.object(lc, "read_bytes", side_effect=read), patch.object(lc, "remove_experiment") as removed:
            with self.assertRaisesRegex(lc.LifecycleError, "readback does not match"):
                lc.extract(a)
            removed.assert_not_called()

    def test_existing_matching_packet_resumes_and_retires(self):
        def read(repo, path, sha, **kwargs):
            if path.endswith("/README.md"): return b"Lab owner present"
            return packet()
        with patch.object(lc, "get_head", return_value=HEAD), patch.object(lc, "load_selection", return_value=[("README.md", b"foo")]), patch.object(lc, "api") as mutation, patch.object(lc, "read_bytes", side_effect=read), patch.object(lc, "remove_experiment", return_value=COMMIT) as retired:
            result = lc.extract(args())
        mutation.assert_not_called()
        retired.assert_called_once()
        self.assertTrue(result["resumed"])
        self.assertEqual("EXTRACTED_AND_RETIRED", result["result"])

    def test_existing_different_packet_refuses_to_overwrite(self):
        def read(repo, path, sha, **kwargs):
            if path.endswith("/README.md"): return b"Lab owner present"
            return b"different"
        with patch.object(lc, "get_head", return_value=HEAD), patch.object(lc, "load_selection", return_value=[("README.md", b"foo")]), patch.object(lc, "api") as mutation, patch.object(lc, "read_bytes", side_effect=read), patch.object(lc, "remove_experiment") as retired:
            with self.assertRaisesRegex(lc.LifecycleError, "DIFFERENT bytes"):
                lc.extract(args())
            mutation.assert_not_called()
            retired.assert_not_called()

    def test_new_packet_write_then_retire(self):
        observed = {}
        def write(method, path, data=None):
            self.assertEqual("PUT", method)
            observed["bytes"] = base64.b64decode(data["content"])
            return {"commit": {"sha": COMMIT}}
        def read(repo, path, sha, **kwargs):
            if path.endswith("/README.md"): return b"Lab owner present"
            if "bytes" not in observed: raise lc.GitHubNotFound("not found")
            return observed["bytes"]
        with patch.object(lc, "get_head", return_value=HEAD), patch.object(lc, "load_selection", return_value=[("README.md", b"foo")]), patch.object(lc, "api", side_effect=write), patch.object(lc, "read_bytes", side_effect=read), patch.object(lc, "remove_experiment", return_value=COMMIT) as retired:
            result = lc.extract(args())
        self.assertFalse(result["resumed"])
        self.assertEqual("EXTRACTED_AND_RETIRED", result["result"])
        retired.assert_called_once()

    def test_retire_exact_directory_nonforced(self):
        files = [{"path":"experiments/experiment_001/a.py","type":"blob","mode":"100644"},
                 {"path":"experiments/experiment_001/nested/b.py","type":"blob","mode":"100644"},
                 {"path":"experiments/experiment_002/keep.py","type":"blob","mode":"100644"}]
        def api(method, path, data=None):
            if method == "POST" and path.endswith("/git/trees"):
                self.assertEqual(2, len(data["tree"]))
                self.assertTrue(all("experiment_001/" in f["path"] for f in data["tree"]))
                return {"sha":"c"*40}
            if method == "POST" and path.endswith("/git/commits"): return {"sha":COMMIT}
            if method == "PATCH":
                self.assertFalse(data["force"])
                return {"ref":"refs/heads/master"}
            raise AssertionError((method, path))
        with patch.object(lc, "get_head", side_effect=[HEAD, COMMIT]), patch.object(lc, "get_tree", side_effect=[("d"*40, files), ("e"*40, [files[2]])]), patch.object(lc, "api", side_effect=api):
            self.assertEqual(COMMIT, lc.remove_experiment(ID, HEAD, "unworthy"))

    def test_retire_stale_head_never_writes(self):
        with patch.object(lc, "get_head", return_value=COMMIT), patch.object(lc, "api") as remote:
            with self.assertRaisesRegex(lc.LifecycleError, "master moved"):
                lc.remove_experiment(ID, HEAD, "unworthy")
            remote.assert_not_called()

    def test_blank_experiment_id_does_not_erase_every_experiment(self):
        with patch.object(lc, "get_head") as remote:
            with self.assertRaises(lc.LifecycleError):
                lc.remove_experiment("", HEAD, "unworthy")
            remote.assert_not_called()


if __name__ == "__main__":
    unittest.main()
