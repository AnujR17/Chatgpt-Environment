"""Exercise the role-review, company-watchlist and application workflow in an isolated browser."""
import json
import os
import re
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright, expect

url=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/')
with sync_playwright() as p, TemporaryDirectory() as temp:
 browser=p.chromium.launch(headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1050})
 page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(url,wait_until='networkidle')
 data=page.evaluate("fetch('/data/jobs.json').then(r=>r.json())")
 company_data=page.evaluate("fetch('/data/companies.json').then(r=>r.json())")
 expected=len([j for j in data['jobs'] if j.get('status')!='closed'])
 expect(page.locator('.role-card')).to_have_count(expected)
 # Platform filters include cross-posted evidence without duplicating roles.
 for platform,count in [('Indeed',4),('Naukri',1),('X',2)]:
  page.get_by_role('button',name=re.compile('^'+platform+r'\b')).click()
  expect(page.locator('.role-card')).to_have_count(count)
 page.get_by_role('button',name='All sources',exact=True).click()
 page.get_by_label('Role type',exact=True).select_option('Junior / fresher')
 expect(page.locator('.role-card')).to_have_count(2)
 page.get_by_label('Role type',exact=True).select_option('all')
 page.get_by_label('Pay evidence',exact=True).select_option('estimated')
 expect(page.locator('.role-card')).to_have_count(3)
 # Historical reports remain separate from current pay, and stay on hold.
 tech=page.locator('.role-card').filter(has=page.get_by_text('Techolution',exact=True))
 expect(tech.get_by_text('Pay not disclosed',exact=True)).to_be_visible()
 expect(tech.get_by_text('Reported pay only',exact=True)).to_be_visible()
 expect(tech.locator('.state-on_hold')).to_be_visible()
 page.get_by_label('Pay evidence',exact=True).select_option('all')
 shramik=page.locator('.role-card').filter(has=page.get_by_text('ShramikSathi',exact=True))
 shramik.get_by_role('button',name='Save ShramikSathi role').click()
 page.get_by_role('button',name='Applications',exact=True).click()
 expect(page.get_by_label('Shortlisted column').locator('.company-name')).to_have_text('ShramikSathi')
 card=page.get_by_label('Shortlisted column').locator('[draggable=true]')
 card.drag_to(page.get_by_label('Applied column'))
 expect(page.get_by_label('Applied column').locator('.company-name')).to_have_text('ShramikSathi')
 page.get_by_label('Applied column').get_by_role('button',name='Review role').click()
 dialog=page.get_by_role('dialog')
 expect(dialog.get_by_role('link',name='Open application')).to_have_attribute('href','mailto:info@shramiksathi.com')
 dialog.get_by_label('Next action',exact=True).fill('Follow up with recruiter')
 dialog.get_by_label('Action due',exact=True).fill((date.today()-timedelta(days=1)).isoformat())
 dialog.get_by_label('Notes',exact=True).fill('Browser verification note')
 dialog.get_by_role('button',name='Save changes',exact=True).click()
 dialog.get_by_role('button',name='Close opportunity',exact=True).click()
 page.reload(wait_until='networkidle')
 page.get_by_role('button',name='Applications',exact=True).click()
 expect(page.get_by_label('Applied column').locator('.company-name')).to_have_text('ShramikSathi')
 page.get_by_role('button',name=re.compile('^Next actions')).click()
 expect(page.get_by_role('button',name=re.compile('Follow up with recruiter'))).to_be_visible()
 # Company categories and following are editable and durable.
 page.get_by_role('button',name='Companies',exact=True).click()
 expect(page.locator('.company-card')).to_have_count(len(company_data['companies']))
 page.get_by_role('button',name=re.compile(r'^Dream\b')).click()
 expect(page.locator('.company-card')).to_have_count(3)
 page.get_by_label('Category for Microsoft',exact=True).select_option('Workable')
 expect(page.locator('.company-card')).to_have_count(2)
 page.get_by_role('button',name=re.compile('^All companies')).click()
 page.get_by_role('button',name='Follow Microsoft',exact=True).click()
 page.get_by_role('button',name='Following',exact=True).click()
 expect(page.locator('.company-card')).to_have_count(1)
 expect(page.get_by_label('Category for Microsoft')).to_have_value('Workable')
 # Backup includes legacy role progress plus new company preferences.
 page.get_by_role('button',name='Export',exact=True).click()
 with page.expect_download() as download:
  page.get_by_role('button',name='Back up saved progress (JSON)').click()
 backup_path=Path(temp)/'backup.json';download.value.save_as(backup_path)
 backup=json.loads(backup_path.read_text())
 assert backup['overrides']['shramiksathi-4469701295']['notes']=='Browser verification note'
 assert backup['companyOverrides']['microsoft']['tier']=='Workable'
 assert backup['companyOverrides']['microsoft']['following'] is True
 page.get_by_role('button',name='Export',exact=True).click()
 with page.expect_download() as download:
  page.get_by_role('button',name='Export roles to CSV',exact=True).click()
 csv_path=Path(temp)/'board.csv';download.value.save_as(csv_path)
 assert 'Browser verification note' in csv_path.read_text()
 # Verify restoration and mobile layout in another browser context.
 second=browser.new_context(viewport={'width':390,'height':844})
 mobile=second.new_page();mobile.on('pageerror',lambda e:errors.append(str(e)))
 mobile.goto(url,wait_until='networkidle')
 mobile.locator('input[type=file]').set_input_files(backup_path)
 mobile.get_by_role('button',name='Applications',exact=True).click()
 expect(mobile.get_by_label('Applied column').locator('.company-name')).to_have_text('ShramikSathi')
 mobile.get_by_role('button',name='Companies',exact=True).click()
 expect(mobile.get_by_label('Category for Microsoft')).to_have_value('Workable')
 assert mobile.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),'Company view overflows on mobile'
 mobile.screenshot(path='/tmp/design-search-mobile-companies.png',full_page=False)
 mobile.get_by_role('button',name='Discover',exact=True).click()
 assert mobile.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),'Role view overflows on mobile'
 mobile.screenshot(path='/tmp/design-search-mobile-discover.png',full_page=False)
 # Add a junior role; source URL duplicate checking and manual entries remain available.
 page.get_by_role('button',name='Add role',exact=True).click()
 dialog=page.get_by_role('dialog')
 dialog.get_by_label('Company *',exact=True).fill('Browser QA Company')
 dialog.get_by_label('Role *',exact=True).fill('Interaction Designer')
 dialog.get_by_label('Source URL',exact=True).fill('https://example.com/test-role')
 dialog.get_by_label('Role type',exact=True).select_option('Junior / fresher')
 dialog.get_by_role('button',name='Add to discovered',exact=True).click()
 expect(page.get_by_role('dialog')).to_contain_text('Browser QA Company')
 page.get_by_role('dialog').get_by_role('button',name='Close opportunity').click()
 assert not errors,errors
 print('PASS: Indeed/Naukri/X filters, junior roles, reported pay separation, on-hold roles, save to pipeline, drag/drop, persistence, due actions, editable company tiers/following, CSV, backup/restore, mobile layout, manual junior role, no JS errors.')
 browser.close()
