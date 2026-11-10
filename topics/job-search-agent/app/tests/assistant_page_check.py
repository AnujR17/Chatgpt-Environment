"""Dedicated assistant route, shared private data and history on desktop/mobile."""
import json
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright, expect

BASE=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/').rstrip('/')
JOB_ID='shramiksathi-4469701295'
POSTING='Full employer posting: conduct user research and prototype a product flow.'
with sync_playwright() as p, TemporaryDirectory() as temp:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1050},timezone_id='Asia/Kolkata')
    page=context.new_page();errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.add_init_script('''if(!localStorage.getItem('route-qa')){
      localStorage.setItem('route-qa','yes');
      localStorage.setItem('design-jobs.profile.v1',JSON.stringify({name:'Fictional Candidate',email:'example@example.com',portfolio:'https://example.com',resume:'',availability:'December, three months',background:'Built a prototype.'}));
      localStorage.setItem('design-jobs.overrides.v1',JSON.stringify({'shramiksathi-4469701295':{status:'interview',notes:'Keep private notes',nextAction:'Keep next step'}}));
    }''')
    page.goto(BASE+'/assistant',wait_until='networkidle')
    expect(page.get_by_role('heading',name='Application assistant',exact=True)).to_be_visible()
    expect(page.get_by_role('heading',name='Start with a role',exact=True)).to_be_visible()
    page.get_by_label('Search assistant roles').fill('ShramikSathi')
    page.locator('.assistant-role').click()
    expect(page).to_have_url(re.compile('/assistant\\?role='+JOB_ID+'$'))
    page.get_by_label('Full job description',exact=True).fill(POSTING)
    page.get_by_role('button',name='Discover',exact=True).click()
    expect(page.get_by_role('heading',name='Discover roles',exact=True)).to_be_visible()
    card=page.locator('.role-card').filter(has=page.get_by_text('ShramikSathi',exact=True))
    card.get_by_role('button',name='Review role',exact=True).click()
    page.get_by_role('button',name='Open assistant',exact=True).click()
    expect(page.get_by_role('dialog')).to_have_count(0)
    expect(page.get_by_label('Full job description',exact=True)).to_have_value(POSTING)
    page.go_back(wait_until='networkidle')
    expect(page.get_by_role('heading',name='Discover roles',exact=True)).to_be_visible()
    page.go_forward(wait_until='networkidle')
    expect(page.get_by_role('heading',name='Application assistant',exact=True)).to_be_visible()
    page.reload(wait_until='networkidle')
    expect(page.get_by_label('Full job description',exact=True)).to_have_value(POSTING)
    page.get_by_role('button',name='Review your profile',exact=True).click()
    expect(page.get_by_label('Name',exact=True)).to_have_value('Fictional Candidate')
    page.get_by_role('button',name='Assistant',exact=True).click()
    page.get_by_label('I reviewed this posting',exact=False).check()
    with page.expect_download() as event:
        page.get_by_role('button',name='Download Codex request',exact=True).click()
    request_path=Path(temp)/'request.json';event.value.save_as(request_path)
    request=json.loads(request_path.read_text())
    assert request['jobId']==JOB_ID
    result={**request['responseSchema'],'documents':{'evaluation':'Prototype requirement: evidence F001. Other requirements unknown.','cv':'Built a prototype.','coverLetter':'I built a prototype.','interview':'Discuss prototype tradeoffs.'},'review':{'factualAccuracy':True,'requirementsCoverage':True,'claims':[{'document':'cv','quote':'Built a prototype.','factIds':['F001']}],'notes':'Fictional QA only.'}}
    result_path=Path(temp)/'result.json';result_path.write_text(json.dumps(result))
    page.locator('.application-workspace input[type=file]').set_input_files(result_path)
    page.get_by_role('button',name='Tailored CV',exact=True).click()
    expect(page.get_by_label('Tailored CV',exact=True)).to_have_value('Built a prototype.')
    page.screenshot(path='/tmp/job-assistant-page-desktop.png',full_page=True)
    page.get_by_role('button',name='Export',exact=True).click()
    with page.expect_download() as event:
        page.get_by_role('button',name='Back up saved progress (JSON)',exact=True).click()
    backup_path=Path(temp)/'backup.json';event.value.save_as(backup_path)
    overrides=page.evaluate("JSON.parse(localStorage.getItem('design-jobs.overrides.v1'))")
    assert overrides[JOB_ID]['status']=='interview' and overrides[JOB_ID]['notes']=='Keep private notes'
    mobile=browser.new_context(viewport={'width':390,'height':844},timezone_id='Asia/Kolkata').new_page()
    mobile.on('pageerror',lambda error:errors.append(str(error)))
    mobile.goto(BASE+'/assistant?role='+JOB_ID,wait_until='networkidle')
    mobile.locator('main > input[type=file]').set_input_files(backup_path)
    expect(mobile.get_by_label('Full job description',exact=True)).to_have_value(POSTING)
    mobile.get_by_role('button',name='Tailored CV',exact=True).click()
    expect(mobile.get_by_label('Tailored CV',exact=True)).to_have_value('Built a prototype.')
    assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Mobile assistant overflow'
    mobile.screenshot(path='/tmp/job-assistant-page-mobile.png',full_page=True)
    mobile.reload(wait_until='networkidle')
    expect(mobile.get_by_label('Full job description',exact=True)).to_have_value(POSTING)
    assert not errors,errors
    print('PASS: independent /assistant route and navigation, role deep links, back/forward/reload, board-to-assistant entry, shared profile/progress, request/result round trip and mobile backup restore; no runtime errors. Synthetic model output only.')
    browser.close()
