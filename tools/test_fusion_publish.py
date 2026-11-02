"""Pure Python tests for public-only synthetic result publication."""
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = (Path(__file__).resolve().parent.parent /
          "experiments/002_word_math_connected_attachments/publish_results.py")
SPEC = importlib.util.spec_from_file_location("playground_public_fusion_publisher", SCRIPT)
publisher = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = publisher
SPEC.loader.exec_module(publisher)


def complete():
    return {
        "schema": publisher.SCHEMA, "status": "OBSERVED",
        "lab_head": "a" * 40, "branch": "master",
        "proof_ceiling": "Synthetic only",
        "explicit_lab_write_operations": 0,
        "private_source_in_output": False,
        "probes": [
            {"probe": name, "state": "OBSERVED",
             "observation": {"measured": True, "value": 0.4}}
            for name in sorted(publisher.EXPECTED_PROBES)
        ],
    }


def review():
    return {
        "schema": "umd.playground.review.v1",
        "id": publisher.EXPERIMENT,
        "status": "ACTIVE",
        "summary": "Old result needs review.",
        "evidence": [],
        "limitations": ["Synthetic results only."],
        "next_actions": [],
        "files": [{"path": "probe_fusions.py", "label": "Probe"}],
        "recommended_action": "IMPROVE",
        "recommendation_reason": "Needs evidence",
    }


class PublishResultTests(unittest.TestCase):
    def test_accept_exact_complete_synthetic_schema(self):
        self.assertEqual("OBSERVED", publisher.validate_result(complete())["status"])

    def test_refuse_partial_result(self):
        data = complete()
        data["status"] = "PARTIAL"
        with self.assertRaises(publisher.PublishError):
            publisher.validate_result(data)

    def test_refuse_missing_probe(self):
        data = complete()
        data["probes"].pop()
        with self.assertRaises(publisher.PublishError):
            publisher.validate_result(data)

    def test_refuse_unexpected_nested_private_key(self):
        data = complete()
        data["probes"][0]["observation"]["password"] = "do not publish"
        with self.assertRaises(publisher.PublishError):
            publisher.validate_result(data)

    def test_refuse_sensitive_path_or_token(self):
        for text in ("/data/data/com.termux/files/home/private.py",
                     "ghp_" + "z" * 25):
            with self.subTest(text=text):
                data = complete()
                data["probes"][0]["observation"]["evidence"] = text
                with self.assertRaises(publisher.PublishError):
                    publisher.validate_result(data)

    def test_refuse_extra_unexpected_top_level(self):
        data = complete()
        data["source_code"] = "internal"
        with self.assertRaises(publisher.PublishError):
            publisher.validate_result(data)

    def test_prepare_review_keeps_selection_and_no_lab_authority(self):
        data = publisher.prepare_review(review(), "a" * 40, "b" * 64)
        self.assertEqual("REVIEW_READY", data["status"])
        self.assertEqual("REVIEW", data["recommended_action"])
        self.assertEqual("latest_results.json", data["files"][0]["path"])
        self.assertEqual(2, len(data["files"]))
        self.assertFalse(data.get("owner_approved", False))
        self.assertEqual("latest_results.json", data["evidence"][0]["source"])
        # Idempotent evidence/selection when the same experiment is republished.
        data2 = publisher.prepare_review(data, "a" * 40, "b" * 64)
        self.assertEqual(1, len([
            x for x in data2["evidence"]
            if x["kind"] == "OPERATOR_PUBLISHED_COMPLETE_TERMUX_RUN"
        ]))
        self.assertEqual(2, len(data2["files"]))

    def test_invalid_result_never_reaches_git_commands(self):
        invalid = complete()
        invalid["status"] = "BLOCKED"
        with patch.object(publisher, "_command") as git_command:
            with self.assertRaises(publisher.PublishError):
                publisher.publish_result(invalid)
            git_command.assert_not_called()


if __name__ == "__main__":
    unittest.main()
