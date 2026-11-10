"""Broad source coverage must expose limits, original pay units and dated leads."""
import json,os,re
from playwright.sync_api import sync_playwright,expect
url=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);context=browser.new_context(viewport={'width':1440,'height':1000});page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url,wait_until='networkidle')
 jobs=page.evaluate("fetch('/data/jobs.json').then(r=>r.json()).then(d=>d.jobs)")
 active=[j for j in jobs if j.get('status')!='closed']
 coverage=page.evaluate("fetch('/data/sources.json').then(r=>r.json()).then(d=>d.coverage)")
 # Genuine cross-posts enrich existing cards instead of becoming duplicates.
 page.locator('.source-chips>button').filter(has_text=re.compile('^Indeed')).click()
 expect(page.locator('.role-card')).to_have_count(sum('indeed' in ' '.join([j.get('sourceType','')]+[s.get('platform',s.get('url','')) for s in j.get('additionalSources',[])]).lower() for j in active))
 expect(page.locator('.role-card').filter(has=page.get_by_text('project44',exact=True))).to_have_count(1)
 page.locator('.source-chips>button').filter(has_text=re.compile('^YC / Work at a Startup')).click()
 expect(page.locator('.role-card')).to_have_count(sum(j.get('sourceType')=='YC / Work at a Startup' for j in active))
 expect(page.get_by_text('Older listing: verify intake',exact=True)).to_have_count(2)
 expect(page.locator('.state-on_hold')).to_have_count(2)
 expect(page.get_by_text('USD 8,000–USD 12,000/year',exact=True)).to_be_visible()
 page.get_by_role('button',name='All sources',exact=True).click()
 page.get_by_label('Pay evidence',exact=True).select_option('annual')
 expect(page.locator('.role-card')).to_have_count(sum(j.get('advertisedCompensation',{}).get('period')=='year' and j.get('advertisedCompensation',{}).get('verified') is True for j in active))
 expect(page.get_by_text('₹4,00,000–₹6,00,000/year',exact=True)).to_be_visible()
 page.get_by_label('Pay evidence',exact=True).select_option('all')
 page.locator('.source-chips>button').filter(has_text=re.compile('^Remote boards')).click()
 remote_terms=['remote boards','remoteok','remote ok','weworkremotely','we work remotely','remotive','himalayas','workingnomads','working nomads','remote.co']
 expect(page.locator('.role-card')).to_have_count(sum(any(term in ' '.join([j.get('sourceType','')]+[s.get('platform',s.get('url','')) for s in j.get('additionalSources',[])]).lower() for term in remote_terms) for j in active))
 expect(page.get_by_text('Energise.pro',exact=True)).to_be_visible()
 # Only documented site/source access is claimed; no account requirement is invented.
 page.get_by_role('button',name='Source coverage',exact=True).click()
 expect(page.get_by_role('heading',name='Sources checked',exact=True)).to_be_visible()
 expect(page.locator('.coverage-source-card')).to_have_count(len(coverage))
 naukri=page.locator('.coverage-source-card').filter(has=page.get_by_role('heading',name='Naukri',exact=True))
 expect(naukri).to_contain_text(next(c['status'] for c in coverage if c['source']=='Naukri'))
 hn=page.locator('.coverage-source-card').filter(has=page.get_by_role('heading',name='Hacker News Who is hiring, October 2026',exact=True))
 expect(hn).to_contain_text(next(c['findings'] for c in coverage if c['source']=='Hacker News Who is hiring, October 2026'))
 expect(page.get_by_role('heading',name='StartupMap.in',exact=True)).to_be_visible()
 expect(page.get_by_role('heading',name='Wellfound',exact=True)).to_be_visible()
 expect(page.get_by_role('heading',name='We Work Remotely',exact=True)).to_be_visible()
 page.screenshot(path='/tmp/source-coverage-desktop.png',full_page=True)
 mobile=browser.new_context(viewport={'width':390,'height':844}).new_page();mobile.on('pageerror',lambda e:errors.append(str(e)))
 mobile.goto(url,wait_until='networkidle');mobile.get_by_role('button',name='Source coverage',exact=True).click()
 expect(mobile.locator('.coverage-source-card')).to_have_count(len(coverage))
 assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
 mobile.screenshot(path='/tmp/source-coverage-mobile.png',full_page=True)
 assert not errors,errors
 browser.close()
print('PASS: Indeed cross-post dedupe, YC older/hold labels, original annual USD/INR units, remote-board filter, current source coverage records, Naukri restrictions, HN evidence, directories and mobile layout.')
