"""Verify company research, private evidence and blacklist behavior end to end."""
import json,os,re
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright,expect
url=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/')
with sync_playwright() as p, TemporaryDirectory() as temp:
 browser=p.chromium.launch(headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1050});page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(url,wait_until='networkidle')
 page.get_by_role('button',name='Companies',exact=True).click()
 expect(page.locator('.company-card')).to_have_count(92)
 assert page.locator('.company-card').first.inner_text().find('Product company')>=0
 page.get_by_label('Company type',exact=True).select_option('product')
 expect(page.locator('.company-card')).to_have_count(58)
 page.get_by_label('Company type',exact=True).select_option('all')
 page.get_by_label('Search companies').fill('Gravity')
 card=page.locator('.company-card');expect(card).to_have_count(1)
 card.get_by_role('button',name='Roles & fit').click()
 expect(card.get_by_text('Personal fit unassessed',exact=True)).to_be_visible()
 selectors=card.locator('.requirement-row select');assert selectors.count()>=4
 selectors.nth(0).select_option('met')
 card.locator('.requirement-row input').nth(0).fill('Portfolio case study: prototype and final UI')
 selectors.nth(1).select_option('partial')
 expect(card.get_by_role('meter')).to_have_attribute('aria-valuenow','1')
 expect(card.get_by_role('meter')).to_have_attribute('aria-valuetext',re.compile('1 met, 1 partial'))
 # Export current evidence with public role/source data.
 with page.expect_download() as download:page.get_by_role('button',name='Export filtered list').click()
 csv=Path(temp)/'companies.csv';download.value.save_as(csv)
 text=csv.read_text();assert 'Gravity' in text and 'Portfolio case study' in text and 'careers.gravity.fast' in text
 # Save the role first, then blacklist: discovery hides it but pipeline remains.
 page.get_by_role('button',name='Discover',exact=True).click()
 page.get_by_label('Search roles').fill('Gravity')
 expect(page.locator('.role-card')).to_have_count(1)
 page.get_by_role('button',name='Save Gravity role',exact=True).click()
 page.get_by_role('button',name='Blacklist company',exact=True).click()
 expect(page.locator('.role-card')).to_have_count(0)
 page.get_by_role('button',name='Applications',exact=True).click()
 expect(page.locator('.company-name').filter(has_text='Gravity')).to_have_count(1)
 page.reload(wait_until='networkidle')
 page.get_by_label('Search roles').fill('Gravity');expect(page.locator('.role-card')).to_have_count(0)
 page.get_by_role('button',name='Companies',exact=True).click()
 expect(page.locator('.company-card')).to_have_count(91)
 page.locator('.section-tabs').get_by_role('button',name=re.compile('^Blacklist')).click()
 expect(page.locator('.company-card')).to_have_count(1)
 page.get_by_label('Blacklist reason for Gravity').fill('Personal preference')
 page.get_by_role('button',name='Export',exact=True).click()
 with page.expect_download() as download:page.get_by_role('button',name='Back up saved progress (JSON)').click()
 backup_path=Path(temp)/'backup.json';download.value.save_as(backup_path);backup=json.loads(backup_path.read_text())
 assert backup['companyOverrides']['gravity']['blacklisted'] is True
 assert backup['companyOverrides']['gravity']['blacklistReason']=='Personal preference'
 assert backup['companyOverrides']['gravity']['assessments']
 # Restore to another device context and reverse a blacklist safely.
 mobile_context=browser.new_context(viewport={'width':390,'height':844});mobile=mobile_context.new_page()
 mobile.on('pageerror',lambda e:errors.append(str(e)))
 mobile.goto(url,wait_until='networkidle');mobile.locator('input[type=file]').set_input_files(backup_path)
 mobile.get_by_role('button',name='Companies',exact=True).click()
 mobile.locator('.section-tabs').get_by_role('button',name=re.compile('^Blacklist')).click()
 mobile.get_by_role('button',name='Unblock Gravity',exact=True).click()
 mobile.get_by_role('button',name='Company directory',exact=True).click()
 mobile.get_by_label('Search companies').fill('Gravity')
 mobile.get_by_role('button',name='Roles & fit').click()
 expect(mobile.get_by_role('meter')).to_have_attribute('aria-valuenow','1')
 expect(mobile.locator('.requirement-row input').nth(0)).to_have_value('Portfolio case study: prototype and final UI')
 assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
 mobile.screenshot(path='/tmp/company-directory-mobile.png',full_page=True)
 mobile.locator('.section-tabs').get_by_role('button',name=re.compile('^Blacklist')).click()
 mobile.get_by_label('Company to blacklist').fill('Future Employer')
 mobile.get_by_role('button',name='Add to blacklist',exact=True).click()
 expect(mobile.get_by_role('heading',name='Future Employer',exact=True)).to_be_visible()
 mobile.reload(wait_until='networkidle');mobile.get_by_role('button',name='Companies',exact=True).click()
 mobile.locator('.section-tabs').get_by_role('button',name=re.compile('^Blacklist')).click()
 expect(mobile.get_by_role('heading',name='Future Employer',exact=True)).to_be_visible()
 assert not errors,errors
 browser.close()
print('PASS: 92 companies, 58 product teams, source requirements, evidence meter, filtered CSV, blacklist persistence, saved applications retained, backup/restore, unblock, custom exclusions and mobile layout.')
