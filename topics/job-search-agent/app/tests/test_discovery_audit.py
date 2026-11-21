import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('discovery_audit', Path(__file__).resolve().parents[1]/'scripts/discovery_audit.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


class DiscoveryAuditTest(unittest.TestCase):
    def inventory(self):
        return mod.candidates({'batches':[{'id':'broad', 'result':{'content':[{'type':'text','text':
            'Design colleague - Example | LinkedIn (https://example.org/person)\n【r1】 We are hiring Product Design Interns.\n'
            +'\n'+'-'*80+'\n'+'UI/UX Design Intern (https://example.org/job)\n【r2】 Remote India internship, pay unknown.'}]}}]})

    def test_profile_snippet_cannot_disappear_when_job_is_reviewed(self):
        inventory = self.inventory(); self.assertEqual(len(inventory['candidates']),2)
        candidate = inventory['candidates'][1]
        decisions = {'entries':[{**candidate,'checkedAt':'2026-11-21','disposition':'unresolved',
                     'reason':'Pay/intake unknown','nextAction':'Verify employer terms','recheckAfter':'2026-11-22'}]}
        result = mod.audit(inventory, decisions)
        self.assertFalse(result['passed']); self.assertEqual(result['missing'][0]['sourceUrl'],'https://example.org/person')

    def test_geography_or_age_can_be_accounted_without_creating_vacancy(self):
        inventory=self.inventory();entries=[]
        for candidate in inventory['candidates']:
            entries.append({**candidate,'checkedAt':'2026-11-21','disposition':'historical',
                            'reason':'Original post older than14days; outside geography','nextAction':'Watch for renewed intake'})
        self.assertTrue(mod.audit(inventory,{'entries':entries})['passed'])
        entries[0]['disposition']='feed';entries[0]['jobId']='invented'
        self.assertFalse(mod.audit(inventory,{'entries':entries},jobs=set())['passed'])

    def test_errors_and_sampling_remain_explicit(self):
        inventory=mod.candidates({'batches':[{'result':{'isError':True,'content':[{'type':'text','text':'Unavailable'}]}}]})
        self.assertFalse(mod.audit(inventory,{'entries':[]})['passed'])
        original=self.inventory();self.assertFalse(original['sampleOnly'])
        original['omittedCandidates']=1
        self.assertFalse(mod.audit(original,{'entries':[]})['passed'])


if __name__ == '__main__':unittest.main()
