import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('social_plan', Path(__file__).resolve().parents[1]/'scripts/social_search_plan.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class SocialPlanTest(unittest.TestCase):
    def test_posts_are_separate_and_generation_never_claims_search(self):
        config = {'version':1,'targets':[{'id':'studio','name':'Example Studio','careersUrl':'https://example.com/careers'}]}
        plan = mod.build_plan(config, '2026-11-12')
        queries = {q['id']:q for q in plan['queries']}
        self.assertIn('site:linkedin.com/posts/', queries['studio-linkedin-posts']['query'])
        self.assertIn('site:linkedin.com/feed/update/', queries['linkedin-updates-broad']['query'])
        self.assertIn('site:x.com', queries['studio-x-posts']['query'])
        self.assertTrue(all(q['status']=='not_searched' for q in plan['queries']))
        self.assertEqual(plan['timezone'], 'Asia/Kolkata')

    def test_invalid_identity_and_credential_links_are_rejected(self):
        for targets in [[{'id':'a','name':''}], [{'id':'a','name':'A'},{'id':'a','name':'B'}], [{'id':'a','name':'A','careersUrl':'https://user:secret@example.com'}]]:
            with self.assertRaises(ValueError):
                mod.build_plan({'version':1,'targets':targets}, '2026-11-12')


if __name__ == '__main__':
    unittest.main()
