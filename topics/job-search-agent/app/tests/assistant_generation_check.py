"""Website generation transport with controlled server fixtures, no paid calls."""
import json
import os
from playwright.sync_api import sync_playwright, expect

BASE=os.environ.get('TRACKER_TEST_URL','http://127.0.0.1:4173/').rstrip('/')
JOB_ID='shramiksathi-4469701295'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1050},timezone_id='Asia/Kolkata')
    page=context.new_page();errors=[];requests=[];pending=[];mode={'value':'success'}
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.add_init_script('''localStorage.setItem('design-jobs.profile.v1',JSON.stringify({name:'Fictional Candidate',email:'example@example.com',background:'Built a prototype.',availability:'Three months'}));localStorage.setItem('design-jobs.overrides.v1',JSON.stringify({'shramiksathi-4469701295':{status:'interview',notes:'Preserve this private note'}}));''')

    def api(route):
        if route.request.method=='GET':
            route.fulfill(json={'available':True,'model':'fixture-model'});return
        data=route.request.post_data_json;requests.append(data)
        if mode['value']=='credits':
            route.fulfill(status=503,json={'error':{'code':'gateway_credits_required','message':'AI Gateway needs available credits.','settingsUrl':'https://vercel.com/anujrai1701-gmailcoms-projects/~/ai-gateway'}});return
        if mode['value']=='hold':pending.append(route);return
        result={**data['responseSchema'],'documents':{'evaluation':'Prototype requirement: evidence F001. Pay remains unknown.','cv':'Built a prototype.','coverLetter':'I built a prototype.','interview':'Discuss prototype tradeoffs.'},'review':{'factualAccuracy':True,'requirementsCoverage':True,'claims':[{'document':'cv','quote':'Built a prototype.','factIds':['F001']}],'notes':'Controlled server fixture, not a live model.'}}
        route.fulfill(json={'result':result,'model':'fixture-model','usage':{'inputTokens':100,'outputTokens':80}})

    page.route('**/api/assistant',api)
    page.goto(BASE+'/assistant?role='+JOB_ID,wait_until='networkidle')
    button=page.get_by_role('button',name='Generate application',exact=True)
    expect(button).to_be_disabled();assert not requests
    page.get_by_label('Full job description',exact=True).fill('Design a prototype and explain decisions. Full fictional posting.')
    page.get_by_label('I reviewed this posting',exact=False).check()
    expect(button).to_be_enabled();button.click()
    page.get_by_role('button',name='Tailored CV',exact=True).click()
    expect(page.get_by_label('Tailored CV',exact=True)).to_have_value('Built a prototype.')
    assert len(requests)==1 and requests[0]['jobId']==JOB_ID
    assert 'Preserve this private note' not in json.dumps(requests)
    page.get_by_label('Tailored CV',exact=True).fill('User revised draft.')
    mode['value']='credits'
    button.click()
    expect(page.get_by_role('alert')).to_contain_text('needs available credits')
    expect(page.get_by_label('Tailored CV',exact=True)).to_have_value('User revised draft.')
    expect(page.get_by_role('link',name='Open AI settings',exact=True)).to_be_visible()
    mode['value']='hold';button.click()
    page.get_by_role('button',name='Cancel generation',exact=True).click()
    expect(page.get_by_role('alert')).to_contain_text('cancelled')
    for route in pending:
        try:route.abort('aborted')
        except Exception:pass  # The browser may already have cancelled it.
    expect(page.get_by_label('Tailored CV',exact=True)).to_have_value('User revised draft.')
    overrides=page.evaluate("JSON.parse(localStorage.getItem('design-jobs.overrides.v1'))")
    assert overrides[JOB_ID]['status']=='interview' and overrides[JOB_ID]['notes']=='Preserve this private note'
    assert not errors,errors
    page.screenshot(path='/tmp/job-assistant-generation-desktop.png',full_page=True)
    page.unroute_all(behavior='ignoreErrors')
    browser.close()
    print('PASS: website generation POST, confirmed-source payload, reviewed documents, credit-error recovery, cancellation and preservation of drafts/stages/private notes. Provider responses are controlled fixtures, not live AI.')
