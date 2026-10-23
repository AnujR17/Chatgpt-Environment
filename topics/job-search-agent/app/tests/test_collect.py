import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('collector',Path(__file__).resolve().parents[1]/'scripts/collect.py')
collector=importlib.util.module_from_spec(spec);spec.loader.exec_module(collector)

class CollectorTests(unittest.TestCase):
 def test_relevance(self):
  self.assertTrue(collector.relevant('Interaction Design Intern'))
  self.assertTrue(collector.relevant('UX Design Internship'))
  self.assertFalse(collector.relevant('Senior Product Designer'))
  self.assertFalse(collector.relevant('Graphic Design Intern'))
 def test_remote_requires_supported_eligibility(self):
  self.assertTrue(collector.location_supported('Remote India',True))
  self.assertFalse(collector.location_supported('Remote United States',True))
  self.assertFalse(collector.location_supported('Remote',True))
 def test_schema_handles_arrays_and_does_not_guess_pay(self):
  obj={'@graph':[{'@type':'JobPosting','title':'UX Design Intern','jobLocationType':'TELECOMMUTE','applicantLocationRequirements':{'name':'India'},'url':'/job/design','baseSalary':{'currency':'INR','value':{'value':360000,'unitText':'YEAR'}}}]}
  post=list(collector.job_objects(obj))[0]
  job=collector.extract_schema(post,'https://example.com/careers','Example','2026-10-23')
  self.assertEqual(job['sourceUrl'],'https://example.com/job/design')
  self.assertIsNone(job['payMin']);self.assertFalse(job['payVerified'])
 def test_nonpublic_sources_rejected(self):
  for url in ['file:///etc/passwd','http://example.com','https://127.0.0.1/','https://localhost/','https://user:pass@example.com/']:
   self.assertFalse(collector.safe_remote(url))
 def test_scripts_do_not_pollute_visible_listing(self):
  page=collector.Page();page.feed('<h1>UX Design Intern</h1><script>private_js()</script><style>x</style><p>Remote India</p>')
  self.assertEqual(page.visible(),'UX Design Intern Remote India')
if __name__=='__main__':unittest.main()
