"""Static case-study rendering, responsive layout and resource checks."""
import asyncio,json,os,re
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/design-review';OUT.mkdir(parents=True,exist_ok=True)

async def main():
 errors=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=os.environ.get('CHECKPOINT_BROWSER','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
  page.on('pageerror',lambda error:errors.append(str(error)))
  base=os.environ.get('REGEN_CASE_URL','http://127.0.0.1:8123/')
  response=await page.goto(base,wait_until='networkidle');assert response.status==200
  await page.evaluate('document.fonts.ready')
  assert await page.title()=='AI for behavior design / Anuj Rai / Regen'
  assert await page.locator('.hero-credits').get_by_text('Anuj Rai',exact=True).count()==1
  assert await page.locator('.hero-credits').get_by_text('Anupam Rana',exact=True).count()==1
  assert await page.locator('.ia-branches > li').count()==5
  assert await page.locator('.research-findings > article').count()==4
  assert await page.locator('.people > article').count()==5
  assert await page.locator('header,nav,button,input,select,textarea,details').count()==0
  assert await page.locator('.desktop-mockup').count()==4
  assert await page.locator('.cma-scene').count()==3
  assert await page.locator('#character-family .look span').all_text_contents()==['Neutral','Happy','Frustrated','Sad','Confused']
  assert not re.search(r'\b(fictional|hypotheticals?)\b',await page.locator('body').inner_text(),re.I)
  for width,height,name in [(1440,1000,'case-desktop'),(1024,768,'case-tablet'),(390,844,'case-mobile'),(320,700,'case-320')]:
   await page.set_viewport_size({'width':width,'height':height});await page.evaluate('scrollTo(0,0)');await page.wait_for_timeout(100)
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Overflow at {width}'
   assert await page.locator('.hero .world').evaluate("e=>getComputedStyle(e).opacity==='1'&&getComputedStyle(e).filter==='none'&&getComputedStyle(e).objectFit==='contain'")
   for selector in ('.desktop-mockup','.display-bezel img','.phone-mockup','.phone-mockup img','.overlay-screen'):
    for node in await page.locator(selector).all():assert await node.evaluate("e=>getComputedStyle(e).transform==='none'")
   assert await page.locator('img').evaluate_all('nodes=>nodes.every(e=>e.complete&&e.naturalWidth>0)')
   await page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
   if width in (1440,390):
    for selector,label in [('#top','hero'),('#architecture','architecture'),('#prototype','flat-mockup'),('#cma','cma-static')]:
     await page.locator(selector).screenshot(path=str(OUT/(label+'-'+str(width)+'.png')))
  if os.environ.get('REGEN_CASE_SITE'):
   for note in ('evidence.html','interview-guide.html','research.html','project.html','feasibility.html'):
    response=await page.goto(base+note);assert response.status==200
    assert await page.locator('header,nav').count()==0
    assert not re.search(r'\b(fictional|hypotheticals?)\b',await page.locator('body').inner_text(),re.I)
    await page.set_viewport_size({'width':390,'height':844});assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors
  await browser.close()
 result={'hero_authorship':'passed','full_visible_artwork':'passed','static_presentation_without_navigation_or_demo_controls':'passed','flat_desktop_and_phone_mockups':'passed','information_architecture_and_research':'passed','reflow':'1440, 1024, 390 and 320px passed','javascript_errors':errors}
 (OUT/'visual-case-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':asyncio.run(main())
