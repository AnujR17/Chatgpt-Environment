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
  assert await page.title()=='Regen / Gaming, feeling, trying again'
  assert not await page.get_by_text('classroom',exact=False).count()
  assert await page.evaluate('regenCase.state.mode')=='brief'
  for key,expected in [('exhausted','small'),('calm','choice'),('excited','choice'),('mixed','choice'),('frustrated','brief')]:
   await page.locator(f'#presets [data-key="{key}"]').click()
   assert await page.evaluate('regenCase.state.mode')==expected
  await page.locator('#try-cue').click()
  assert await page.evaluate('regenCase.state.phase')=='playing'
  assert await page.locator('#presets button').first.is_disabled()
  await page.locator('#lesson').fill('Settle before pulling')
  await page.locator('#stuck').click()
  assert await page.evaluate('regenCase.state.mode')=='small'
  await page.locator('#try-cue').click();await page.locator('#helped').click()
  assert 'Marked helpful' in await page.locator('#demo-status').inner_text()
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
  await page.set_viewport_size({'width':1440,'height':1000});await page.locator('#cma').scroll_into_view_if_needed()
  await page.screenshot(path=str(OUT/'case-cma.png'))
  assert not errors,errors
  await browser.close()
 result={'fixture':'Authored local case-study demo, no real camera/game data','cma_presets_and_rules':'passed','in_flight_stability':'passed','feedback_and_smaller_target':'passed','theme_preview':'passed','reduced_motion':'passed','reflow':'1440, 390 and 320px passed','javascript_errors':errors}
 (OUT/'visual-case-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))


if __name__=='__main__':asyncio.run(main())
