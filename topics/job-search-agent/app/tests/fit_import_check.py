"""A reviewed-criteria import must preserve private progress and work in role details."""
import json,os
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright,expect
url=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/')
with sync_playwright() as p, TemporaryDirectory() as temp:
 browser=p.chromium.launch(headless=True);context=browser.new_context(viewport={'width':1440,'height':1000});page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url,wait_until='networkidle')
 companies=page.evaluate("fetch('/data/companies.json').then(r=>r.json()).then(d=>d.companies)")
 gravity=next(c for c in companies if c['id']=='gravity');role=gravity['roles'][0];criterion=role['requirements'][0]['id']
 page.evaluate("""() => {
 localStorage.setItem('design-jobs.companies.v1',JSON.stringify({gravity:{blacklisted:true,blacklistReason:'Keep my reason',tier:'Dream',following:true,assessments:{unrelated:{criterion:{state:'met',evidence:'Keep this'}}}}}));
 localStorage.setItem('design-jobs.overrides.v1',JSON.stringify({'shramiksathi-4469701295':{status:'applied',notes:'Preserve application notes'}}));
 localStorage.setItem('design-jobs.profile.v1',JSON.stringify({name:'Local profile',availability:'My recorded date'}));
 }""")
 page.reload(wait_until='networkidle')
 fixture={'version':1,'custom':[],'overrides':{},'companyOverrides':{'gravity':{'assessments':{role['id']:{criterion:{'state':'partial','evidence':'Reviewed prototype; higher proficiency unverified'}}}},'fit-hevodata':{'assessments':{'hevo-433ffdef':{'listing-summary':{'state':'partial','evidence':'Relevant dashboard work; tokens not evidenced'}}}}}}
 octet=next(c for c in companies if c['id']=='octet-design-studio');octet_role=next(r for r in octet['roles'] if r['title']=='UI UX Designer');octet_criterion=octet_role['requirements'][0]['id']
 fixture['companyOverrides']['octet-design-studio']={'assessments':{octet_role['id']:{octet_criterion:{'state':'gap','evidence':'Distinct role criterion on a shared careers URL'}}}}
 source=Path(temp)/'fit.json';source.write_text(json.dumps(fixture))
 page.locator('input[type=file]').set_input_files(source)
 saved=page.evaluate("JSON.parse(localStorage.getItem('design-jobs.companies.v1'))")
 assert saved['gravity']['blacklisted'] is True and saved['gravity']['blacklistReason']=='Keep my reason'
 assert saved['gravity']['tier']=='Dream' and saved['gravity']['following'] is True
 assert saved['gravity']['assessments']['unrelated']['criterion']['evidence']=='Keep this'
 assert page.evaluate("JSON.parse(localStorage.getItem('design-jobs.overrides.v1'))['shramiksathi-4469701295'].status")=='applied'
 assert page.evaluate("JSON.parse(localStorage.getItem('design-jobs.profile.v1')).name")=='Local profile'
 # Existing public-company role uses the same criterion record in the directory and drawer.
 page.get_by_role('button',name='Companies',exact=True).click()
 page.locator('.section-tabs').get_by_role('button',name='Blacklist',exact=False).click()
 page.get_by_role('button',name='Unblock Gravity',exact=True).click()
 page.get_by_role('button',name='Company directory',exact=True).click()
 page.get_by_label('Search companies').fill('Gravity');page.get_by_role('button',name='Roles & fit',exact=True).click()
 expect(page.locator('.requirement-row input').first).to_have_value('Reviewed prototype; higher proficiency unverified')
 page.get_by_role('button',name='Review role',exact=True).click()
 dialog=page.get_by_role('dialog');expect(dialog.get_by_role('meter')).to_have_attribute('aria-valuetext',f"0 met, 1 partial, 0 gaps, {len(role['requirements'])-1} unassessed")
 expect(dialog.locator('.requirement-row input').first).to_have_value('Reviewed prototype; higher proficiency unverified')
 dialog.get_by_role('button',name='Close opportunity',exact=True).click()
 # A role outside the public company list still accepts private criteria in its own drawer.
 page.get_by_role('button',name='Discover',exact=True).click();page.get_by_label('Search roles').fill('Hevo')
 page.get_by_role('button',name='Review role',exact=True).click();dialog=page.get_by_role('dialog')
 expect(dialog.get_by_role('meter')).to_have_attribute('aria-valuetext','0 met, 1 partial, 0 gaps, 0 unassessed')
 expect(dialog.locator('.requirement-row input')).to_have_value('Relevant dashboard work; tokens not evidenced')
 dialog.get_by_role('button',name='Close opportunity',exact=True).click()
 page.get_by_label('Search roles').fill('Octet')
 page.locator('.role-card').filter(has=page.get_by_role('heading',name='UI UX Designer',exact=True)).get_by_role('button',name='Review role',exact=True).click()
 dialog=page.get_by_role('dialog');expect(dialog.get_by_role('meter')).to_have_attribute('aria-valuetext','0 met, 0 partial, 1 gaps, 0 unassessed')
 expect(dialog.locator('.requirement-row input')).to_have_value('Distinct role criterion on a shared careers URL')
 dialog.get_by_role('button',name='Close opportunity',exact=True).click()
 page.get_by_role('button',name='Export',exact=True).click()
 with page.expect_download() as download:page.get_by_role('button',name='Back up saved progress (JSON)',exact=True).click()
 target=Path(temp)/'export.json';download.value.save_as(target);exported=json.loads(target.read_text())
 assert exported['companyOverrides']['gravity']['tier']=='Dream'
 assert exported['overrides']['shramiksathi-4469701295']['notes']=='Preserve application notes'
 assert not errors,errors
 browser.close()
print('PASS: reviewed fit import preserves blacklist/reason, category/follow, unrelated evidence, stages, notes and profile; meters share criteria in company/role views and support unlisted companies.')
