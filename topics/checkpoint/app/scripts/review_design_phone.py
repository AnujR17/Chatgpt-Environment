"""Native-to-browser practice cue test. Scripted choices, not gameplay evidence."""
import asyncio
import json
import os
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright
from checkpoint.app import create_application, MainWindow
from checkpoint.attempts import start_attempt, finish_attempt
from checkpoint.phone import PhoneServer

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/design-review';OUT.mkdir(parents=True,exist_ok=True)


async def main():
    app=create_application([])
    with tempfile.TemporaryDirectory() as directory:
        w=MainWindow(no_setup=True,data_dir=directory);w.reduced_motion=True;w.timer.stop();w.show()
        w.session.check_in('frustrated',-.7,.8);w.select_card_source(2)
        start_attempt(w.session,'grip');w.practice_changed()
        w.phone_server=PhoneServer(w.phone_bridge,host='127.0.0.1',port=0).start()
        running=True
        async def pulse():
            while running:
                app.processEvents();await asyncio.sleep(.02)
        task=asyncio.create_task(pulse());errors=[]
        try:
            async with async_playwright() as p:
                options={'headless':True,'args':['--no-sandbox']}
                if os.environ.get('CHECKPOINT_BROWSER'):options['executable_path']=os.environ['CHECKPOINT_BROWSER']
                browser=await p.chromium.launch(**options)
                page=await browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
                page.on('pageerror',lambda e:errors.append(str(e)))
                await page.goto(w.phone_server.url('127.0.0.1'))
                await page.locator('#practiceCue').get_by_text('Try a shorter reach and a slower pull.',exact=True).wait_for()
                assert await page.locator('#practice').is_visible()
                assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                finish_attempt(w.session,'helped');w.practice_changed()
                await page.locator('#practice').wait_for(state='hidden')
                w.mark_setback()
                await page.locator('#nudge').wait_for(state='visible')
                assert 'breath before the next try' in await page.locator('#nudge').inner_text()
                await page.screenshot(path=str(OUT/'phone.png'),full_page=True)
                w.set_support_enabled(False)
                await page.locator('#nudge').wait_for(state='hidden')
                async with page.expect_download() as download_info:await page.locator('#report').click()
                download=await download_info.value
                assert Path(await download.path()).read_bytes().startswith(b'%PDF-')
                start_attempt(w.session,'orange');w.practice_changed()
                await page.locator('#practice').wait_for(state='visible')
                w.phone_server.stop();w.phone_server=None
                await page.get_by_text('Disconnected',exact=True).wait_for(timeout=8000)
                assert not await page.locator('#practice').is_visible()
                assert await page.locator('#report').is_disabled()
                assert not errors,errors
                await browser.close()
            result={'fixture':'Scripted player choices, real native HTTP bridge and Chromium 390x844',
                    'selected_cue_above_character':'passed','resolved_cue_hidden':'passed','disconnected_cue_hidden':'passed',
                    'native_pdf_download':'passed','setback_tip_and_mute':'passed','horizontal_overflow':'none','javascript_errors':errors,
                    'physical_phone_wifi':'not tested'}
            (OUT/'phone-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
        finally:
            running=False;await task;w.close();app.processEvents()


if __name__=='__main__':asyncio.run(main())
