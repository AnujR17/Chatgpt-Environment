"""Browser-to-native export verification with explicitly synthetic UI cues, not accuracy evidence."""
import asyncio
import json
import time
from pathlib import Path
from playwright.async_api import async_playwright
from checkpoint.app import create_application,MainWindow
from checkpoint.phone import PhoneServer
from checkpoint.runtime import Cue

ROOT=Path(__file__).resolve().parents[1]


async def main():
    app=create_application([]);window=MainWindow(no_setup=True,data_dir=ROOT/'build/browser-history');window.show();window.reduced_motion=True
    window.session.experimental_analysis=True;generation=window.session.start_capture('video');window.live_view=True
    flat={'smile':0.,'brow':0.,'eyes':1.,'jaw':0.,'tension':0.}
    window.session.receive_cue(Cue('accepted','neutral',movement=flat,mapping_label='Neutral appearance'),generation)
    window.overlay_enabled=True;window.refresh();window.phone_server=PhoneServer(window.phone_bridge,host='127.0.0.1',port=0).start()
    running=True
    async def pulse():
        while running:
            if window.session.cue is not None:window.session.cue_received_at=time.monotonic()
            app.processEvents();await asyncio.sleep(.02)
    task=asyncio.create_task(pulse());errors=[]
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(headless=True,args=['--no-sandbox'])
            page=await browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
            page.on('pageerror',lambda error:errors.append(str(error)))
            await page.goto(window.phone_server.url('127.0.0.1'));await page.get_by_role('heading',name='Neutral appearance',exact=True).wait_for()
            await page.screenshot(path=str(ROOT/'artifacts/pip-phone-neutral.png'),full_page=True)
            assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Phone content overflows horizontally'
            window.grab().save(str(ROOT/'artifacts/pip-desktop-neutral.png'));window.overlay.grab().save(str(ROOT/'artifacts/pip-overlay-neutral.png'))
            window.reduced_motion=False
            happy={'smile':.6,'brow':0.,'eyes':.8,'jaw':0.,'tension':0.,'laugh':0.}
            window.session.receive_cue(Cue('accepted','happiness',movement=happy,mapping_label='Smile movement'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='Smile movement',exact=True).wait_for()
            laughing={**happy,'smile':.85,'jaw':.65,'laugh':.8}
            window.session.receive_cue(Cue('accepted','happiness',movement=laughing,mapping_label='Open smile'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='Open smile',exact=True).wait_for();await asyncio.sleep(.5)
            assert await page.evaluate('current.laugh>.65 && current.smile>.7'), 'Open smile did not reach the phone animation'
            await page.screenshot(path=str(ROOT/'artifacts/pip-phone-open-smile.png'),full_page=True)
            # App reduced-motion preference is also honoured by the paired phone.
            window.reduced_motion=True;window.next_export=0.;window.refresh()
            for _ in range(30):
                if await page.evaluate('latest.animate===false'):break
                await asyncio.sleep(.1)
            assert await page.evaluate('latest.animate===false')
            await asyncio.sleep(.1)
            assert await page.evaluate('current.laugh===to.laugh'), 'Reduced motion must show the current expression without easing/bounce'
            brow={'smile':-.15,'brow':.65,'eyes':.7,'jaw':0.,'tension':.35}
            window.session.receive_cue(Cue('accepted','anger',movement=brow,mapping_label='Brows drawn'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='Brows drawn',exact=True).wait_for();await asyncio.sleep(1.3)
            await page.screenshot(path=str(ROOT/'artifacts/pip-phone-brows.png'),full_page=True)
            async with page.expect_download() as download_info:await page.get_by_role('button',name='Download session report').click()
            download=await download_info.value;report=json.loads(Path(await download.path()).read_text())
            assert report['schema']==2 and 'moments' in report and 'input_activity' in report
            assert not any(key in report for key in ['frame','pixels','typed_text','face_landmarks'])
            window.session.receive_cue(Cue('unavailable',reason='No face detected'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='No face detected',exact=True).wait_for()
            # Unknown face renders a flat neutral appearance without asserting a neutral emotion.
            assert window.latest_companion['unknown'] and window.latest_companion['blob']['smile']==0
            window.phone_server.stop();window.phone_server=None
            await page.get_by_text('Disconnected',exact=True).wait_for(timeout=8000)
            assert not errors,errors
            await browser.close()
        result={'browser':'Chromium, 390x844 phone viewport','fixture':'Synthetic physical-face cues, not live recognition',
                'native_to_phone_updates':'passed','open_smile_animation':'passed','paired_reduced_motion':'passed','neutral_fallback':'passed','report_download':'passed','disconnection':'passed','horizontal_overflow':'none','javascript_errors':errors,
                'physical_phone_network':'not tested'}
        (ROOT/'artifacts/pip-phone-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
    finally:
        running=False;await task;window.close();app.processEvents()


if __name__=='__main__':asyncio.run(main())
