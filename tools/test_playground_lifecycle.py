import argparse
import base64
import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import playground_lifecycle as lc

HEAD = 'a' * 40
COMMIT = 'b' * 40


class LifecycleTests(unittest.TestCase):
    def test_id_and_selection_reject_traversal(self):
        for bad in ('../lab', '/tmp/foo', 'a', 'a/b', 'A_upper'):
            with self.subTest(bad=bad), self.assertRaises(lc.LifecycleError):
                lc.validate_id(bad)
        for bad in ('../secret', '/etc/passwd', r'a\..\b', 'file/../secret', '.'):
            with self.subTest(bad=bad), self.assertRaises(lc.LifecycleError):
                lc.validate_selection([bad])

    def test_selection_explicit_and_deduped(self):
        with self.assertRaises(lc.LifecycleError):
            lc.validate_selection([])
        self.assertEqual(['README.md', 'demo.py'], lc.validate_selection(['README.md','demo.py','README.md']))

    def test_packet_provenance_and_exact_hash(self):
        data = b'print("hello")\n'
        p = lc.build_packet('experiment_001', HEAD, [('demo.py', data)], question='why', author='agent / claim',
            consumer='research/vault/ingest', findings='found', limitations='limited', next_action='test', proof='one run')
        self.assertIn(hashlib.sha256(data).hexdigest(), p)
        self.assertIn(HEAD, p)
        self.assertIn('owner-selected research staging', p)
        self.assertIn('NOT implementation', p)

    def test_owner_approval_blocks_extraction_before_any_transport(self):
        args = argparse.Namespace(id='experiment_001', owner_approved=False)
        with patch.object(lc, 'get_head') as remote:
            with self.assertRaises(lc.LifecycleError):
                lc.extract(args)
            remote.assert_not_called()

    def test_extract_does_not_retire_when_lab_readback_mismatch(self):
        args = argparse.Namespace(id='experiment_001', expected_head=HEAD, owner_approved=True,
          select=['README.md'], question='what?', author='Cody-approved session', consumer='research/vault/ingest',
          findings='X', limitations='Y', next_action='Z', proof='test')
        def fake_api(method, path, data=None):
            if method == 'GET' and 'contents/research/vault/ingest/' in path:
                raise lc.GitHubNotFound('not found')
            if method == 'PUT':
                return {'commit': {'sha': COMMIT}}
            raise AssertionError((method, path))
        with patch.object(lc,'get_head',return_value=HEAD), patch.object(lc,'load_selection',return_value=[('README.md',b'foo')]), patch.object(lc,'api',side_effect=fake_api), patch.object(lc,'read_bytes',return_value=b'wrong'), patch.object(lc,'remove_experiment') as removed:
            with self.assertRaisesRegex(lc.LifecycleError, 'readback does not match'):
                lc.extract(args)
            removed.assert_not_called()

    def test_extract_lab_readback_then_retire(self):
        args = argparse.Namespace(id='experiment_001', expected_head=HEAD, owner_approved=True,
          select=['README.md'], question='what?', author='Cody-approved session', consumer='research/vault/ingest',
          findings='X', limitations='Y', next_action='Z', proof='test')
        observed = {}
        def fake_api(method,path,data=None):
            if method == 'GET' and 'contents/research/vault/ingest/' in path:
                raise lc.GitHubNotFound('not found')
            if method == 'PUT':
                observed['packet'] = base64.b64decode(data['content'])
                return {'commit':{'sha':COMMIT}}
            raise AssertionError((method,path))
        def fake_read(repo,path,sha,**kw):
            return observed['packet']
        with patch.object(lc,'get_head',return_value=HEAD), patch.object(lc,'load_selection',return_value=[('README.md',b'foo')]), patch.object(lc,'api',side_effect=fake_api), patch.object(lc,'read_bytes',side_effect=fake_read), patch.object(lc,'remove_experiment',return_value=COMMIT) as removed:
            result=lc.extract(args)
            self.assertEqual('EXTRACTED_AND_RETIRED',result['result'])
            removed.assert_called_once()

    def test_retire_exact_directory_only_and_verify(self):
        entries=[{'path':'experiments/experiment_001/a.py','type':'blob','mode':'100644'},
                 {'path':'experiments/experiment_001/nested/b.py','type':'blob','mode':'100644'},
                 {'path':'experiments/experiment_002/keep.py','type':'blob','mode':'100644'}]
        def fake_api(method,path,data=None):
            if method=='POST' and path.endswith('/git/trees'):
                self.assertEqual(2,len(data['tree']))
                self.assertTrue(all('experiment_001/' in f['path'] for f in data['tree']))
                return {'sha': 'c'*40}
            if method=='POST' and path.endswith('/git/commits'):
                return {'sha':COMMIT}
            if method=='PATCH':
                self.assertFalse(data['force'])
                return {'ref':'refs/heads/master'}
            raise AssertionError((method,path))
        with patch.object(lc,'get_head',side_effect=[HEAD,COMMIT]),patch.object(lc,'get_tree',side_effect=[('d'*40,entries),('e'*40,[entries[2]])]),patch.object(lc,'api',side_effect=fake_api):
            commit=lc.remove_experiment('experiment_001',HEAD,'unworthy')
            self.assertEqual(COMMIT,commit)

    def test_retire_stale_head_never_mutates(self):
        with patch.object(lc,'get_head',return_value=COMMIT),patch.object(lc,'api') as remote:
            with self.assertRaisesRegex(lc.LifecycleError, 'master moved'):
                lc.remove_experiment('experiment_001',HEAD,'unworthy')
            remote.assert_not_called()


if __name__=='__main__':
    unittest.main()
