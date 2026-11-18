"""Check the visual case-study interaction and reflow. No player-study claim."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/design-review';OUT.mkdir(parents=True,exist_ok=True)


async def main():
 errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=os.environ.get('CHECKPOINT_BROWSER','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(os.environ.get('REGEN_CASE_URL','http://127.0.0.1:8123/'),wait_until='networkidle')
  await page.evaluate('document.fonts.ready')
  assert await page.title()=='AI for behavior design / Anuj Rai / Regen'
  assert await page.locator('.hero-credits').get_by_text('Anuj Rai',exact=True).count()==1
  assert await page.locator('.hero-credits').get_by_text('Anupam Rana',exact=True).count()==1
  assert await page.locator('.hero-credits').get_by_text('Interaction design',exact=True).count()==1
  assert await page.locator('.ia-branches > li').count()==5
  assert await page.locator('.research-findings > article').count()==4
  assert await page.locator('.people > article').count()==5
  assert not await page.get_by_text('classroom',exact=False).count()
  await page.locator('#simulate-fall').click()
  assert 'Waiting for a steadier view' in await page.locator('#play-message').inner_text()
  await page.wait_for_function("document.querySelector('#play-message').textContent.includes('One secure hold')")
  await page.locator('#mute-play').click()
  await page.locator('#simulate-fall').click()
  assert await page.locator('#play-message').inner_text()=='Tips are muted. Keep playing.'
  await page.locator('#mute-play').click()
  assert await page.evaluate('regenCase.state.mode')=='brief'
  for key,expected in [('exhausted','small'),('calm','choice'),('excited','choice'),('mixed','choice'),('frustrated','brief')]:
   await page.locator(f'#presets [data-key="{key}"]').click()
   assert await page.evaluate('regenCase.state.mode')==expected
  await page.locator('#try-cue').click()
  assert await page.evaluate('regenCase.state.phase')=='playing'
  assert await page.locator('#presets button').first.is_disabled()
  await page.locator('#follow-up').click()
  assert await page.evaluate('regenCase.state.phase')=='followup'
  await page.locator('#presets [data-key="calm"]').click()
  await page.locator('#lesson').fill('A pause gave me a choice')
  await page.locator('#helped').click()
  assert await page.evaluate('regenCase.state.outcome')=='yes'
  assert 'Later: Calm' in await page.locator('#demo-status').inner_text()
  await page.locator('#reset').click()
  await page.locator('#smaller').click()
  assert await page.evaluate('regenCase.state.response')=='smaller_goal'
  await page.locator('#follow-up').click();await page.locator('#stuck').click()
  assert await page.evaluate('regenCase.state.outcome')=='no'
  await page.locator('#reset').click()
  assert await page.evaluate('regenCase.state.mode')=='brief'
  await page.locator('[data-theme="dark"]').click()
  assert await page.locator('#app-screen').get_attribute('src')=='assets/dark.png'
  await page.locator('[data-theme="light"]').click()
  assert await page.locator('#motion').get_attribute('aria-pressed')=='true'
  # Exact viewport bounds and screenshots, including narrow reflow.
  for width,height,name in [(1440,1000,'case-desktop'),(390,844,'case-mobile'),(320,700,'case-320')]:
   await page.set_viewport_size({'width':width,'height':height});await page.evaluate('scrollTo(0,0)');await page.wait_for_timeout(150)
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Overflow at {width}'
   await page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
   if width in (1440,390):
    for selector,label in [('#top','hero'),('#architecture','architecture'),('#empathize','research')]:
     await page.locator(selector).screenshot(path=str(OUT/(label+'-'+str(width)+'.png')))
  await page.set_viewport_size({'width':1440,'height':1000});await page.locator('#cma').scroll_into_view_if_needed()
  await page.screenshot(path=str(OUT/'case-cma.png'))
  if os.environ.get('REGEN_CASE_SITE'):
   for note in ('evidence.html','interview-guide.html'):
    response=await page.goto(os.environ['REGEN_CASE_URL']+note)
    assert response.status==200
    assert await page.locator('table').count()>0 if note!='interview-guide.html' else await page.locator('h1').count()==1
    await page.set_viewport_size({'width':390,'height':844})
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors
  await browser.close()
 result={'fixture':'Authored local case-study demo, no real camera/game data','hero_authorship_and_subject':'passed','five_destination_architecture':'passed','source_linked_insights_and_design_personas':'passed','cma_presets_and_rules':'passed','in_flight_stability':'passed','choice_followup_and_helpfulness':'passed','theme_preview':'passed','reduced_motion':'passed','reflow':'1440, 390 and 320px passed','javascript_errors':errors}
 (OUT/'visual-case-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))


if __name__=='__main__':asyncio.run(main())
