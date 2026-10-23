"""Browser smoke test against a running preview; uses an isolated temporary profile."""
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright, expect

url=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/')
with sync_playwright() as p, TemporaryDirectory() as temp:
 browser=p.chromium.launch(headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1000})
 page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(url,wait_until='networkidle')
 expect(page.locator('.job-card')).to_have_count(13)
 page.get_by_role('button',name='View remote stipend matches').click()
 expect(page.locator('.job-card')).to_have_count(1)
 expect(page.locator('.company-name')).to_have_text('ShramikSathi')
 page.get_by_role('button',name='Clear',exact=True).click()
 page.get_by_role('button',name='View ShramikSathi role details').click()
 dialog=page.get_by_role('dialog')
 expect(dialog.get_by_role('link',name='Open application')).to_have_attribute('href','mailto:info@shramiksathi.com')
 dialog.get_by_label('Status',exact=True).select_option('applied')
 dialog.get_by_label('Next action',exact=True).fill('Follow up with recruiter')
 dialog.get_by_label('Action due',exact=True).fill('2026-10-23')
 dialog.get_by_label('Notes',exact=True).fill('Browser verification note')
 dialog.get_by_role('button',name='Save changes',exact=True).click()
 dialog.get_by_role('button',name='Close opportunity',exact=True).click()
 page.reload(wait_until='networkidle')
 expect(page.get_by_label('Applied column').locator('.company-name')).to_have_text('ShramikSathi')
 page.get_by_role('button',name='Next actions',exact=False).click()
 expect(page.get_by_role('button',name='Follow up with recruiter',exact=False)).to_be_visible()
 page.get_by_role('button',name='Add opportunity',exact=True).click()
 dialog=page.get_by_role('dialog')
 dialog.get_by_label('Company *',exact=True).fill('Browser QA Company')
 dialog.get_by_label('Role *',exact=True).fill('Interaction Design Intern')
 dialog.get_by_label('Source URL',exact=True).fill('https://example.com/test-internship')
 dialog.get_by_role('button',name='Add to discovered').click()
 page.get_by_role('dialog').get_by_role('button',name='Close opportunity').click()
 page.get_by_role('button',name='Export',exact=True).click()
 with page.expect_download() as download:
  page.get_by_role('button',name='JSON backup (includes your updates)').click()
 backup_path=Path(temp)/'backup.json';download.value.save_as(backup_path)
 backup=json.loads(backup_path.read_text())
 assert backup['overrides']['shramiksathi-4469701295']['notes']=='Browser verification note'
 assert backup['custom'][0]['company']=='Browser QA Company'
 page.get_by_role('button',name='Export',exact=True).click()
 with page.expect_download() as download:
  page.get_by_role('button',name='Excel-compatible CSV (current board)').click()
 csv_path=Path(temp)/'board.csv';download.value.save_as(csv_path)
 assert 'Browser verification note' in csv_path.read_text()
 # Restore into another browser context to verify the portability path.
 second=browser.new_context(viewport={'width':390,'height':844})
 mobile=second.new_page();mobile.goto(url,wait_until='networkidle')
 mobile.locator('input[type=file]').set_input_files(backup_path)
 expect(mobile.get_by_label('Applied column').locator('.company-name')).to_have_text('ShramikSathi')
 assert mobile.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Mobile page overflows'
 mobile.screenshot(path='/tmp/design-internship-mobile.png',full_page=True)
 # Original context: return to board, exercise actual HTML drag-and-drop.
 page.get_by_role('button',name='Opportunities',exact=False).click()
 card=page.locator('.job-card').filter(has=page.get_by_role('button',name='View More Retail role details'))
 target=page.get_by_label('Shortlisted column')
 card.drag_to(target)
 expect(target.locator('.company-name')).to_have_text('More Retail')
 page.screenshot(path='/tmp/design-internship-board-qa.png',full_page=False)
 assert not errors,errors
 print('PASS: filters, role details, stage changes, persistence, due actions, adding roles, CSV, JSON backup/restore, mobile layout, drag and drop, no JavaScript errors.')
 browser.close()
