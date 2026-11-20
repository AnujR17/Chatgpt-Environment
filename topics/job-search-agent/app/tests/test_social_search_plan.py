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

    def test_social_window_crosses_month_and_year_without_dating_board_results(self):
        plan = mod.build_plan({'version':1,'targets':[]}, '2027-01-05')
        queries = {q['id']:q for q in plan['queries']}
        self.assertEqual(plan['socialPublicationCutoff'], '2026-12-22')
        social = queries['linkedin-posts-broad']
        self.assertEqual(social['publicationWindow'], {'from':'2026-12-22','through':'2027-01-05'})
        self.assertIn('after:2026-12-21 before:2027-01-06', social['query'])
        self.assertNotIn('publicationWindow', queries['indeed-design-broad'])
        for key in ['indeed','wellfound','cutshort','unstop','internshala','instahyre','prosple','hirist','foundit','apna','shine','peerlist','freshersworld']:
            self.assertIn(key+'-design-broad', queries)

    def test_invalid_identity_and_credential_links_are_rejected(self):
        for targets in [[{'id':'a','name':''}], [{'id':'a','name':'A'},{'id':'a','name':'B'}], [{'id':'a','name':'A','careersUrl':'https://user:secret@example.com'}]]:
            with self.assertRaises(ValueError):
                mod.build_plan({'version':1,'targets':targets}, '2026-11-12')

    def test_new_employer_discovery_precedes_targets_and_keeps_eligibility_separate(self):
        config = {'version':1,'targets':[{'id':'brand','name':'Brand','aliases':['Previous Brand','Parent Company'], 'publicHiringPeople':['Public Design Lead']}]}
        plan = mod.build_plan(config, '2026-11-20')
        queries = {q['id']:q for q in plan['queries']}
        self.assertEqual(plan['queries'][0]['phase'], 'discovery')
        self.assertIn('"Parent Company"', queries['brand-alias-1-careers']['query'])
        self.assertIn('"Public Design Lead"', queries['brand-person-0-posts']['query'])
        self.assertIn('site:linkedin.com/posts/', queries['brand-linkedin-authors']['query'])
        self.assertNotIn('India', queries['discovery-linkedin-posts']['query'])
        self.assertEqual(queries['discovery-linkedin-posts']['publicationWindow']['from'], '2026-11-06')
        self.assertNotIn('publicationWindow', queries['brand-alias-1-careers'])
        self.assertTrue(all(q['status']=='not_searched' for q in plan['queries']))
        self.assertEqual(len(queries), len(plan['queries']))

    def test_alias_and_author_fields_reject_malformed_config(self):
        for fields in [{'aliases':'Name'}, {'aliases':['']}, {'publicHiringPeople':{}}, {'publicHiringPeople':[None]}]:
            with self.assertRaises(ValueError):
                mod.build_plan({'version':1,'targets':[{'id':'a','name':'A',**fields}]}, '2026-11-20')


if __name__ == '__main__':
    unittest.main()
