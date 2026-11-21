"""Exercise separate internship/junior discovery without changing saved progress."""
import json,os,re,mimetypes
from urllib.parse import urlparse
from urllib.request import urlopen
from pathlib import Path
from playwright.sync_api import sync_playwright,expect

url=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/')
out=Path(os.environ.get('TRACKER_QA_DIR','/tmp/role-tracks-qa'));out.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 cache={}
 def route_public(context):
  if not url.startswith('https:') or os.environ.get('TRACKER_TEST_RELAY')!='1':return
  def fulfill(route):
   request=route.request
   if request.method not in ['GET','HEAD']:route.abort();return
   key=request.url.split('?')[0]
   if key not in cache:
    with urlopen(request.url,timeout=45) as response:cache[key]=response.read()
   route.fulfill(status=200,content_type=mimetypes.guess_type(urlparse(key).path)[0] or 'text/html',body=cache[key])
  context.route(url.rstrip('/')+'/**',fulfill)
 for width in [1440,390,320]:
  context=browser.new_context(viewport={'width':width,'height':1000})
  route_public(context)
  page=context.new_page();errors=[];posts=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda r:posts.append(r.url) if r.method=='POST' else None)
  page.goto(url);page.locator('.role-card').first.wait_for()
  feed=page.evaluate("fetch('/data/jobs.json').then(r=>r.json()).then(d=>d.jobs)")
  internships=[j for j in feed if j['status']!='closed' and j.get('roleType','Internship')=='Internship']
  juniors=[j for j in feed if j['status']!='closed' and j.get('roleType')=='Junior / fresher']
  expect(page.locator('[data-role-track="Internship"] .role-card')).to_have_count(len(internships))
  expect(page.locator('[data-role-track="Junior / fresher"] .role-card')).to_have_count(len(juniors))
  picker=page.get_by_role('region',name='Job categories',exact=True)
  junior=picker.locator('.job-track-option').filter(has_text='Junior / fresher')
  junior.focus();page.keyboard.press('Enter')
  expect(junior).to_have_attribute('aria-pressed','true')
  expect(page.locator('.role-card')).to_have_count(len(juniors))
  expect(page.get_by_label('Role type',exact=True)).to_have_value('Junior / fresher')
  expect(page.locator('[data-role-track="Internship"]')).to_have_count(0)
  # Original annual salary stays annual inside the junior section.
  qoruz=page.locator('.role-card').filter(has_text='Qoruz')
  expect(qoruz).to_have_count(1);expect(qoruz).to_contain_text('year')
  page.get_by_label('Search roles',exact=True).fill('no-such-role-track-qa')
  expect(page.get_by_role('heading',name='No roles match these filters')).to_be_visible()
  page.get_by_role('button',name='Reset filters',exact=True).click()
  expect(page.locator('.role-card')).to_have_count(len(internships)+len(juniors))
  picker.get_by_role('button',name=re.compile('^Internships')).click()
  expect(page.locator('.role-card')).to_have_count(len(internships))
  page.get_by_label('Work mode',exact=True).select_option('remote')
  expect(page.locator('.role-card')).to_have_count(sum(j.get('workMode')=='Remote' for j in internships))
  page.get_by_label('Work mode',exact=True).select_option('all')
  # Existing dropdown and new category buttons share exactly one selection state.
  page.get_by_label('Role type',exact=True).select_option('Junior / fresher')
  expect(junior).to_have_attribute('aria-pressed','true')
  page.get_by_role('button',name=re.compile('^Archived')).click()
  expect(page.locator('.role-card')).to_have_count(sum(j['status']=='closed' and j.get('roleType')=='Junior / fresher' for j in feed))
  picker.get_by_role('button',name=re.compile('^Both categories')).click()
  expect(page.locator('.role-card')).to_have_count(sum(j['status']=='closed' for j in feed))
  page.get_by_role('button',name='Discover',exact=True).click()
  page.screenshot(path=str(out/f'tracks-{width}.png'))
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow {width}'
  page.get_by_role('button',name='Sources and evidence',exact=True).click()
  print('Existing Sources layout',width,page.evaluate('document.documentElement.scrollWidth'))
  assert not errors,errors;assert not posts,posts
  context.close()
 # Seed only synthetic saved state in a separate browser context.
 context=browser.new_context(viewport={'width':1440,'height':1000})
 route_public(context)
 context.add_init_script("""if(!localStorage.getItem('tracks-qa')){
 localStorage.setItem('design-jobs.overrides.v1',JSON.stringify({'careers-studio-carbon-junior-website-designer':{status:'applied',notes:'Synthetic junior application'},'indeed-moontechnolabs-uiux-intern-eaa533209a303dc0':{status:'applied',notes:'Synthetic archived internship'}}));
 localStorage.setItem('design-jobs.companies.v1',JSON.stringify({'lemon-yellow':{blacklisted:true,blacklistReason:'Synthetic QA only'}}));localStorage.setItem('tracks-qa','1');}""")
 page=context.new_page();page.goto(url);page.locator('.role-card').first.wait_for()
 expect(page.locator('.role-card').filter(has_text='Lemon Yellow')).to_have_count(0)
 page.get_by_role('button',name='Applications',exact=True).click()
 for name in ['Studio Carbon','Moon Technolabs']:
  card=page.locator('.role-card').filter(has_text=name);expect(card).to_have_count(1);expect(card).to_contain_text('Applied')
 page.reload();page.locator('.role-card').first.wait_for()
 state=page.evaluate("JSON.parse(localStorage.getItem('design-jobs.overrides.v1'))")
 assert state['careers-studio-carbon-junior-website-designer']['notes']=='Synthetic junior application'
 assert state['indeed-moontechnolabs-uiux-intern-eaa533209a303dc0']['status']=='applied'
 context.close();browser.close()
print('PASS: two role sections,keyboard selection,filters,empty recovery,annual salary,archives,320/390/1440 Discover layouts,synthetic applied/blacklist/notes preservation;no submissions')
