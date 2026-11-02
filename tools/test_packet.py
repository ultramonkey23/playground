import unittest
from packet import make_packet, fingerprint, validate


class PacketTests(unittest.TestCase):
    def sample(self):
        return make_packet("Test", "local-test", "EXPERIMENT", claim="A", observed="run", state="OBSERVED", timestamp="2026-11-02T00:00:00+00:00")

    def test_valid(self):
        self.assertEqual([], validate(self.sample()))

    def test_tampered_observation_rejected(self):
        p = self.sample()
        p["observation"] = "altered result"
        self.assertIn("content_sha256 mismatch", validate(p))

    def test_order_independent_digest(self):
        p = self.sample()
        self.assertEqual(fingerprint(p), fingerprint(dict(reversed(list(p.items())))))

    def test_authority_forgery_rejected(self):
        p = self.sample()
        p["authority"] = "LAB_CANON"
        self.assertIn("authority must remain advisory", validate(p))

    def test_naive_timestamp_rejected(self):
        p = self.sample()
        p["created_utc"] = "2026-11-02T00:00:00"
        p["content_sha256"] = fingerprint(p)
        self.assertIn("created_utc must be an offset-aware UTC timestamp", validate(p))


if __name__ == "__main__":
    unittest.main()
