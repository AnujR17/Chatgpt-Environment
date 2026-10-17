from pathlib import Path
from playwright.sync_api import sync_playwright
import json
src=Path(__file__).resolve().parents[2]/'source/incoming/2026-10-17/S2 Wireframe · Third Iteration.html'
html=src.read_text()
# Expose existing local model functions only in the test document, never in the preserved source.
pos=html.rfind('})();')
assert pos>0
hook='window.__audit={get:SKey=>S[SKey],conds,condsRaw,riderRules,trigs,amt,paid,rangeOf,costLine,render,ACT,resetAll,closingMsgs};\n'
html=html[:pos]+hook+html[pos:]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1480,'height':1100});page.set_default_timeout(8000)
 page.route('http://**/*',lambda r:r.abort());page.route('https://**/*',lambda r:r.abort())
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html,wait_until='domcontentloaded')
 checks={}
 checks['scenarios']=page.evaluate('''()=>['S2','S5','S3','S8','S9'].map(k=>{const x=__audit.get(k);return {id:k,subject:x.subject,paid:__audit.paid(x),conditions:__audit.conds(x).map(c=>({id:c.id,status:c.st,source:c.src})),rider:__audit.riderRules(x)}})''')
 page.keyboard.press('Alt+ArrowDown');page.keyboard.press('Alt+ArrowDown')
 page.locator('[data-act="fault"][data-arg="Swiggy"]').click()
 page.locator('[data-act="dec"][data-arg="full"]').click()
 page.locator('[data-chg="reason"]').select_option(label='Evidence supports the claim')
 checks['S3_over_limit_confirm']={'confirm_enabled':page.locator('[data-act="confirm"]').is_enabled(),'triggers':page.evaluate('__audit.trigs(__audit.get("S3"))'),'P8':page.evaluate('__audit.conds(__audit.get("S3")).find(c=>c.id==="P8")')}
 page.locator('[data-act="confirm"]').click()
 checks['S3_over_limit_confirm']['decision_recorded']=page.evaluate('__audit.get("S3").decided')
 page.keyboard.press('Alt+ArrowDown')
 page.locator('[data-act="fault"][data-arg="Restaurant"]').click()
 page.locator('[data-act="dec"][data-arg="full"]').click()
 checks['S8_no_refund_terms']=page.evaluate('''()=>{const s=__audit.get('S8');return {P6:__audit.conds(s).find(c=>c.id==='P6'),cost:__audit.costLine(s),amount:__audit.amt(s)}}''')
 page.keyboard.press('Alt+ArrowDown');page.keyboard.press('Alt+ArrowDown')
 checks['P5_before_assessment']=page.evaluate('__audit.conds(__audit.get("S2")).find(c=>c.id==="P5")')
 page.locator('[data-act="drawer"][data-arg="star"]').click()
 checks['star_before_subject_change']=page.locator('.drw').inner_text()
 page.locator('[data-act="close"]').first.click()
 page.locator('[data-chg="subject"]').select_option(label='Charged, order not placed / charged twice')
 page.locator('[data-act="drawer"][data-arg="star"]').click()
 checks['star_after_unrelated_subject_change']=page.locator('.drw').inner_text()
 checks['manual_override_without_reason']=page.evaluate('''()=>{const s=__audit.get('S2');s.dec='full';s.fault='Restaurant';__audit.ACT.setov('P8:na');return {condition:__audit.conds(s).find(c=>c.id==='P8'),lastLog:s.log.slice(-1)}}''')
 checks['javascript_errors']=errors
 checks['method']='Headless Chromium; external requests blocked; in-memory test-only hook exposes existing model functions; preserved HTML unchanged. S3 confirmation and star subject changes exercised through UI.'
 Path('/tmp/swiggy-third-iteration-behavior.json').write_text(json.dumps(checks,indent=2))
 print(json.dumps({k:v for k,v in checks.items() if k!='scenarios'},indent=2))
 b.close()
