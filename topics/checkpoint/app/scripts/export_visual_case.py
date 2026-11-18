"""Export the visual web story as a secondary shareable PDF. Needs Playwright."""
import asyncio,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'docs/case-study'


async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=os.environ.get('CHECKPOINT_BROWSER','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
  await page.goto(os.environ.get('REGEN_CASE_URL','http://127.0.0.1:8123/'),wait_until='networkidle');await page.evaluate('document.fonts.ready')
  # PDF links must remain useful away from the temporary preview server.
  await page.evaluate('''() => {const base='https://github.com/AnujR17/Chatgpt-Environment/blob/topic/regen-case-study-site/topics/checkpoint/app/docs/case-study/';for(const a of document.querySelectorAll('a')){const value=a.getAttribute('href');if(value&&!value.startsWith('#')&&!value.startsWith('http'))a.href=base+value}document.querySelector('.evidence').open=true;dispatchEvent(new Event('beforeprint'))}''')
  await page.emulate_media(media='print')
  await page.pdf(path=str(CASE/'Regen-case-study.pdf'),print_background=True,prefer_css_page_size=True,display_header_footer=False)
  (CASE/'Checkpoint-case-study.pdf').write_bytes((CASE/'Regen-case-study.pdf').read_bytes())
  await browser.close()


if __name__=='__main__':asyncio.run(main())
