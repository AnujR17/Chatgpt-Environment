"""Offline checks: no real credentials and no API traffic."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('context_tools', ROOT / 'bin/context_tools.py')
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.state = patch.object(tools, 'STATE_ROOT', Path(self.temporary.name))
        self.state.start()
        self.addCleanup(self.state.stop)
        environment = {'MEM0_API_KEY': 'test-mem0-credential', 'CODEX_THREAD_ID': 'task-a'}
        self.environment = patch.dict(os.environ, environment, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.network = patch.object(tools, 'request_json', return_value={'results': [{'memory': 'test context'}]})
        self.send = self.network.start()
        self.addCleanup(self.network.stop)

    def test_status_makes_no_request_and_does_not_expose_credentials(self):
        result = tools.local_status()
        self.send.assert_not_called()
        self.assertNotIn('test-mem0-credential', json.dumps(result))
        self.assertEqual(result['credentials'], {'MEM0_API_KEY': True})
        self.assertEqual(result['environment_entity'], 'Chatgpt-Environment')

    def test_repeated_start_even_rephrased_makes_one_request(self):
        first = tools.start_memory('digital-cheque', 'Current work')
        second = tools.start_memory('digital-cheque', 'A different phrasing')
        self.assertFalse(first['cached'])
        self.assertTrue(second['cached'])
        self.assertEqual(self.send.call_count, 1)

    def test_topic_and_task_are_isolated(self):
        tools.start_memory('digital-cheque', 'Work')
        tools.start_memory('another-topic', 'Work')
        tools.start_memory('digital-cheque', 'Work', session='task-b')
        self.assertEqual(self.send.call_count, 3)
        first = self.send.call_args_list[0].args[3]
        other = self.send.call_args_list[1].args[3]
        self.assertEqual(first['filters'], {'AND': [
            {'user_id': 'Chatgpt-Environment'}, {'agent_id': 'Chatgpt-Environment/topic/digital-cheque'}]})
        self.assertNotEqual(first['filters'], other['filters'])
        self.assertEqual(first['top_k'], 8)

    def test_missing_secret_does_not_consume_call_or_cache(self):
        del os.environ['MEM0_API_KEY']
        with self.assertRaises(tools.SetupError):
            tools.start_memory('digital-cheque', 'Work')
        self.send.assert_not_called()
        os.environ['MEM0_API_KEY'] = 'new-test-credential'
        self.assertEqual(tools.start_memory('digital-cheque', 'Work')['status'], 'ok')
        self.assertEqual(self.send.call_count, 1)

    def test_errors_are_cached_without_retry_storm(self):
        self.send.side_effect = tools.SetupError('HTTP 429')
        self.assertEqual(tools.start_memory('digital-cheque', 'Work')['status'], 'error')
        self.assertTrue(tools.start_memory('digital-cheque', 'Work')['cached'])
        self.assertEqual(self.send.call_count, 1)
        self.send.side_effect = None
        tools.start_memory('digital-cheque', 'Work', refresh=True)
        self.assertEqual(self.send.call_count, 2)

    def test_pending_attempt_is_not_automatically_retried(self):
        self.send.side_effect = RuntimeError('simulated process interruption')
        with self.assertRaises(RuntimeError):
            tools.start_memory('digital-cheque', 'Work')
        self.send.side_effect = None
        outcome = tools.start_memory('digital-cheque', 'Work')
        self.assertEqual(outcome['status'], 'error')
        self.assertTrue(outcome['cached'])
        self.assertEqual(self.send.call_count, 1)

    def test_curated_write_is_scoped_and_deduplicated_across_checkpoints(self):
        tools.save_memory('digital-cheque', 'Decision: no interviews yet.', 'decision')
        result = tools.save_memory('digital-cheque', 'Decision: no interviews yet.', 'handoff', retry=True)
        self.assertTrue(result['cached'])
        self.assertEqual(self.send.call_count, 1)
        url, variable, header, payload = self.send.call_args.args
        self.assertEqual(url, 'https://api.mem0.ai/v3/memories/add/')
        self.assertEqual(variable, 'MEM0_API_KEY')
        self.assertEqual(header, 'Authorization')
        self.assertEqual(payload['filters']['agent_id'], 'Chatgpt-Environment/topic/digital-cheque')
        self.assertEqual(payload['filters']['user_id'], 'Chatgpt-Environment')
        self.assertEqual(payload['metadata']['environment'], 'Chatgpt-Environment')
        self.assertNotIn('user_id', payload)  # v3 identities belong inside filters.

    def test_summary_containing_credential_is_blocked(self):
        for content in ('credential: test-mem0-credential', 'password=not-a-real-password'):
            with self.assertRaises(tools.SetupError):
                tools.save_memory('digital-cheque', content, 'handoff')
        self.send.assert_not_called()

    def test_invalid_topic_or_missing_task_is_blocked(self):
        with self.assertRaises(tools.SetupError):
            tools.start_memory('../another-topic', 'Work')
        del os.environ['CODEX_THREAD_ID']
        with self.assertRaises(tools.SetupError):
            tools.start_memory('digital-cheque', 'Work')
        self.send.assert_not_called()

    def test_new_api_key_does_not_reuse_another_accounts_context(self):
        tools.start_memory('digital-cheque', 'Work')
        os.environ['MEM0_API_KEY'] = 'another-test-credential'
        tools.start_memory('digital-cheque', 'Work')
        self.assertEqual(self.send.call_count, 2)

    def test_api_key_alone_is_enough_without_user_id_or_figma_token(self):
        tools.start_memory('environment-setup', 'Setup')
        self.assertEqual(self.send.call_count, 1)
        self.assertNotIn('MEM0_USER_ID', os.environ)
        self.assertNotIn('FIGMA_ACCESS_TOKEN', tools.local_status()['credentials'])

    def test_bootstrap_creates_environment_and_topic_entity_without_extra_id(self):
        text = (ROOT / 'bootstrap.txt').read_text()
        tools.save_memory('environment-setup', text, 'decision')
        payload = self.send.call_args.args[3]
        self.assertEqual(payload['filters'], {'user_id': 'Chatgpt-Environment',
                                             'agent_id': 'Chatgpt-Environment/topic/environment-setup'})
        self.assertEqual(payload['metadata']['environment'], 'Chatgpt-Environment')

    def test_redirects_are_rejected(self):
        with self.assertRaises(tools.SetupError):
            tools.NoRedirect().redirect_request(Request('https://api.mem0.ai/'), None,
                                                302, 'Found', {}, 'https://other.example/')

    def test_http_failure_does_not_print_service_body_or_token(self):
        with patch.object(tools, 'build_opener') as opener:
            opener.return_value.open.side_effect = HTTPError('https://api.mem0.ai/', 403,
                                                             'test-mem0-credential', {}, None)
            with self.assertRaises(tools.SetupError) as outcome:
                self.network.stop()
                try:
                    tools.request_json('https://api.mem0.ai/v3/memories/search/', 'MEM0_API_KEY',
                                       'Authorization', {'query': 'Work'})
                finally:
                    self.network.start()
            self.assertIn('HTTP 403', str(outcome.exception))
            self.assertNotIn('test-mem0-credential', str(outcome.exception))


class InstallerTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('installer', ROOT / 'install.py')
        self.installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.installer)
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.installer.TARGET = root / 'installed'
        self.installer.AGENTS = root / 'AGENTS.md'

    def test_repeatable_install_preserves_existing_instructions(self):
        self.installer.AGENTS.write_text('User instructions remain here.\n')
        self.installer.install()
        original = self.installer.AGENTS.read_bytes()
        self.installer.install()
        self.assertEqual(self.installer.AGENTS.read_bytes(), original)
        self.assertIn('User instructions remain here.', original.decode())

    def test_locally_edited_installed_file_is_preserved(self):
        self.installer.install()
        target = self.installer.TARGET / 'bin/context_tools.py'
        target.write_text('A user edit must survive.\n')
        with self.assertRaises(SystemExit):
            self.installer.install()
        self.assertEqual(target.read_text(), 'A user edit must survive.\n')


if __name__ == '__main__':
    unittest.main()
