"""A private, fictional-data browser round trip; does not call an LLM or send applications."""
import json
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright, expect

URL = os.environ.get('TRACKER_TEST_URL', 'http://127.0.0.1:4173/')
JOB_ID = 'shramiksathi-4469701295'
with sync_playwright() as p, TemporaryDirectory() as temp:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 1050})
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.add_init_script('''if (!localStorage.getItem('qa-initialized')) {
      localStorage.setItem('design-jobs.profile.v1',JSON.stringify({name:'Fictional Candidate',email:'example@example.com',portfolio:'https://example.com',resume:'',availability:'December, three months',background:'Built a prototype.\\nInterviewed five users.'}));
      localStorage.setItem('design-jobs.overrides.v1',JSON.stringify({'shramiksathi-4469701295':{status:'interview',notes:'Private QA note',nextAction:'Keep next action'}}));
      localStorage.setItem('design-jobs.companies.v1',JSON.stringify({microsoft:{tier:'Workable',following:true},'blocked-qa':{name:'QA Excluded Employer',blacklisted:true,reason:'Private reason'}}));
      localStorage.setItem('qa-initialized','yes');
    }''')
    page.goto(URL, wait_until='networkidle')

    def open_workspace(target):
        target.get_by_role('button', name='Discover', exact=True).click()
        card = target.locator('.role-card').filter(has=target.get_by_text('ShramikSathi', exact=True))
        card.get_by_role('button', name='Review role').click()
        target.get_by_role('button', name='Prepare with Codex', exact=True).click()
        return target.get_by_role('dialog')

    dialog = open_workspace(page)
    expect(dialog.get_by_role('button', name='Download Codex request')).to_be_disabled()
    dialog.get_by_label('Full job description', exact=True).fill('Full employer posting: design and research prototypes. Stipend remains as in original source.')
    dialog.get_by_label('I reviewed this posting', exact=False).check()
    with page.expect_download() as event:
        dialog.get_by_role('button', name='Download Codex request').click()
    request_file = Path(temp) / 'request.json'
    event.value.save_as(request_file)
    request = json.loads(request_file.read_text())
    assert request['jobId'] == JOB_ID
    assert 'Private QA note' not in json.dumps(request)
    assert 'Private reason' not in json.dumps(request)
    result = dict(request['responseSchema'])
    result['documents'] = {'evaluation': 'Research evidence F002; unknowns must be confirmed.', 'cv': 'Built a prototype.', 'coverLetter': 'I interviewed five users.', 'interview': 'Discuss prototype tradeoffs.'}
    result['review'] = {'factualAccuracy': True, 'requirementsCoverage': True, 'claims': [{'document': 'cv', 'quote': 'Built a prototype.', 'factIds': ['F001']}, {'document': 'coverLetter', 'quote': 'interviewed five users', 'factIds': ['F002']}], 'notes': 'Fictional data review only.'}
    result['status'] = 'applied'
    result['notes'] = 'Injected replacement note'
    result_file = Path(temp) / 'result.json'
    result_file.write_text(json.dumps({**result, 'jobId': 'another-job'}))
    dialog.locator('input[type=file]').set_input_files(result_file)
    expect(dialog.get_by_role('alert')).to_contain_text('different role or an older request')
    result_file.write_text(json.dumps(result))
    verified = subprocess.run(['node', 'scripts/check_application_result.mjs', str(request_file), str(result_file)], check=True, capture_output=True, text=True)
    assert json.loads(verified.stdout)['valid'] is True
    dialog.locator('input[type=file]').set_input_files(result_file)
    dialog.get_by_role('button', name='Tailored CV', exact=True).click()
    expect(dialog.get_by_label('Tailored CV', exact=True)).to_have_value('Built a prototype.')
    dialog.get_by_label('These are the exact documents I submitted.').check()
    dialog.get_by_role('button', name='Save submitted copy', exact=True).click()
    expect(dialog.get_by_role('heading', name='Submitted copy saved')).to_be_visible()
    dialog.get_by_label('Tailored CV', exact=True).fill('Later draft edit.')
    expect(dialog.get_by_role('status')).to_contain_text('Edited since review')
    page.screenshot(path='/tmp/job-agent-workspace-desktop.png')
    dialog.get_by_role('button', name='Close opportunity').click()
    page.reload(wait_until='networkidle')
    dialog = open_workspace(page)
    dialog.get_by_role('button', name='Tailored CV', exact=True).click()
    expect(dialog.get_by_label('Tailored CV', exact=True)).to_have_value('Later draft edit.')
    with page.expect_download() as event:
        dialog.get_by_role('button', name='Download submitted copy').click()
    submitted_file = Path(temp) / 'submitted.json'
    event.value.save_as(submitted_file)
    assert json.loads(submitted_file.read_text())['result']['documents']['cv'] == 'Built a prototype.'
    overrides = page.evaluate("JSON.parse(localStorage.getItem('design-jobs.overrides.v1'))")
    assert overrides[JOB_ID]['status'] == 'interview'
    assert overrides[JOB_ID]['notes'] == 'Private QA note'
    assert overrides[JOB_ID]['nextAction'] == 'Keep next action'
    dialog.get_by_role('button', name='Application draft', exact=True).click()
    dialog.get_by_label('Application draft', exact=True).fill('Keep these email edits after closing the drawer.')
    dialog.get_by_role('button', name='Close opportunity').click()
    page.reload(wait_until='networkidle')
    dialog = open_workspace(page)
    dialog.get_by_role('button', name='Application draft', exact=True).click()
    expect(dialog.get_by_label('Application draft', exact=True)).to_have_value('Keep these email edits after closing the drawer.')
    dialog.get_by_role('button', name='Close opportunity').click()
    page.get_by_role('button', name='Export', exact=True).click()
    with page.expect_download() as event:
        page.get_by_role('button', name='Back up saved progress (JSON)').click()
    backup_file = Path(temp) / 'backup.json'
    event.value.save_as(backup_file)

    mobile_context = browser.new_context(viewport={'width': 390, 'height': 844})
    mobile = mobile_context.new_page()
    mobile.on('pageerror', lambda error: errors.append(str(error)))
    mobile.goto(URL, wait_until='networkidle')
    mobile.locator('input[type=file]').set_input_files(backup_file)
    dialog = open_workspace(mobile)
    expect(dialog.get_by_role('heading', name='Submitted copy saved')).to_be_visible()
    dialog.get_by_role('button', name='Tailored CV', exact=True).click()
    expect(dialog.get_by_label('Tailored CV', exact=True)).to_have_value('Later draft edit.')
    assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Mobile page overflow'
    assert dialog.evaluate('(el)=>el.scrollWidth<=el.clientWidth'), 'Mobile drawer overflow'
    mobile.screenshot(path='/tmp/job-agent-workspace-mobile.png')
    companies = mobile.evaluate("JSON.parse(localStorage.getItem('design-jobs.companies.v1'))")
    assert companies['blocked-qa']['reason'] == 'Private reason'
    assert companies['microsoft']['following'] is True
    assert not errors, errors
    print('PASS: desktop/mobile request export, wrong-role rejection, reviewed import, private-state preservation, draft persistence, review invalidation, immutable submitted copy and JSON backup/restore; no JS errors. Synthetic model output only; no LLM/application/employer interaction.')
    browser.close()
