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
    window.session.experimental_analysis=True;generation=window.session.start_capture('video');window.select_card_source(1)
    flat={'smile':0.,'brow':0.,'eyes':1.,'jaw':0.,'tension':0.}
    window.session.receive_cue(Cue('accepted','neutral',movement=flat,mapping_label='Neutral appearance'),generation)
    window.overlay_enabled=True;window.refresh();window.phone_server=PhoneServer(window.phone_bridge,host='127.0.0.1',port=0).start()
    running=True;keep_fresh=True
    async def pulse():
        while running:
            if keep_fresh and window.session.cue is not None:window.session.cue_received_at=time.monotonic()
            app.processEvents();await asyncio.sleep(.02)
    task=asyncio.create_task(pulse());errors=[]
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(headless=True,args=['--no-sandbox'])
            page=await browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
            page.on('pageerror',lambda error:errors.append(str(error)))
            await page.goto(window.phone_server.url('127.0.0.1'));await page.get_by_role('heading',name='Neutral appearance',exact=True).wait_for()
            await page.screenshot(path=str(ROOT/'artifacts/nori-phone-neutral.png'),full_page=True)
            assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Phone content overflows horizontally'
            window.grab().save(str(ROOT/'artifacts/nori-desktop-neutral.png'));window.overlay.grab().save(str(ROOT/'artifacts/nori-overlay-neutral.png'))
            window.reduced_motion=False
            happy={'smile':.6,'brow':0.,'eyes':.8,'jaw':0.,'tension':0.,'laugh':0.}
            window.session.receive_cue(Cue('accepted','happiness',movement=happy,mapping_label='Smile movement'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='Smile movement',exact=True).wait_for()
            laughing={**happy,'smile':.85,'jaw':.65,'laugh':.8}
            window.session.receive_cue(Cue('accepted','happiness',movement=laughing,mapping_label='Open smile'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='Open smile',exact=True).wait_for();await asyncio.sleep(.5)
            assert await page.evaluate('current.laugh>.65 && current.smile>.7'), 'Open smile did not reach the phone animation'
            await page.screenshot(path=str(ROOT/'artifacts/nori-phone-open-smile.png'),full_page=True)
            # App reduced-motion preference is also honoured by the paired phone.
            window.reduced_motion=True;window.next_export=0.;window.refresh()
            for _ in range(30):
                if await page.evaluate('latest.animate===false'):break
                await asyncio.sleep(.1)
            assert await page.evaluate('latest.animate===false')
            await asyncio.sleep(.1)
            assert await page.evaluate('current.laugh===to.laugh'), 'Reduced motion must show the current expression without easing/bounce'
            teeth={**laughing,'teeth':.8,'mouth_wide':.3}
            window.session.receive_cue(Cue('accepted','happiness',movement=teeth,mapping_label='Open smile'),generation);window.next_export=0.;window.refresh()
            await asyncio.sleep(.35);assert await page.evaluate('to.teeth>.7')
            await page.screenshot(path=str(ROOT/'artifacts/nori-phone-teeth.png'),full_page=True)
            covered={**flat,'hand':1.,'mouth_visible':0.,'teeth':0.}
            window.session.receive_cue(Cue('unavailable',reason='Mouth partly hidden',movement=covered,gesture={'near':True,'occluded':True}),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='Hand near mouth',exact=True).wait_for();await asyncio.sleep(.35)
            assert await page.evaluate('to.hand===1 && current.teeth===0')
            await page.screenshot(path=str(ROOT/'artifacts/nori-phone-hand.png'),full_page=True)
            brow={'smile':-.15,'brow':.65,'eyes':.7,'jaw':0.,'tension':.35}
            window.session.receive_cue(Cue('accepted','anger',movement=brow,mapping_label='Brows drawn'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='Brows drawn',exact=True).wait_for();await asyncio.sleep(1.3)
            await page.screenshot(path=str(ROOT/'artifacts/nori-phone-brows.png'),full_page=True)
            # Exercise the default reflection at a real 8Hz signal cadence, not only Movement test.
            keep_fresh=False;window.select_card_source(0)
            for _ in range(12):
                window.session.receive_cue(Cue('accepted','happiness',movement={**happy,'cheek':.5},mapping_label='Smile movement'),generation)
                window.next_export=0.;window.refresh();await asyncio.sleep(.125)
            await page.get_by_role('heading',name='Smile-like expression',exact=True).wait_for()
            assert await page.evaluate('latest.source==="visual_pattern" && latest.blob.smile>0.5')
            await page.screenshot(path=str(ROOT/'artifacts/nori-phone-reflection.png'),full_page=True)
            assert window.latest_report['cma']['count']==0, 'Face cues must not invent CMA check-ins'
            window.session.check_in('angry',-.7,.8);window.session.check_in('calm',.6,-.6);window.next_export=0.;window.refresh()
            await page.get_by_text('2 CMA check-ins',exact=True).wait_for()
            async with page.expect_download() as download_info:await page.get_by_role('button',name='Download CMA report (PDF)').click()
            download=await download_info.value;pdf=Path(await download.path()).read_bytes()
            assert pdf.startswith(b'%PDF-') and len(pdf)>5000
            assert window.latest_report['schema']==3 and 'moments' not in window.latest_report
            assert window.latest_companion['source']=='visual_pattern' and window.latest_companion['artwork']=='happy', 'Check-in pinned the live character'
            window.select_card_source(1);keep_fresh=True
            window.session.receive_cue(Cue('unavailable',reason='No face detected'),generation);window.next_export=0.;window.refresh()
            await page.get_by_role('heading',name='No face detected',exact=True).wait_for()
            # Unknown face renders a flat neutral appearance without asserting a neutral emotion.
            assert window.latest_companion['unknown'] and window.latest_companion['blob']['smile']==0
            window.phone_server.stop();window.phone_server=None
            await page.get_by_text('Disconnected',exact=True).wait_for(timeout=8000)
            assert not errors,errors
            await browser.close()
        result={'browser':'Chromium, 390x844 phone viewport','fixture':'Synthetic physical-face cues, not live recognition',
                'default_reflection_and_manual_separation':'passed','native_to_phone_updates':'passed','open_smile_animation':'passed','paired_reduced_motion':'passed','neutral_fallback':'passed','report_download':'PDF passed','hand_mouth_mask':'passed','visible_teeth_presentation':'passed','cma_uses_checkins_only':'passed','disconnection':'passed','horizontal_overflow':'none','javascript_errors':errors,
                'physical_phone_network':'not tested'}
        (ROOT/'artifacts/nori-phone-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
    finally:
        running=False;await task;window.close();app.processEvents()


if __name__=='__main__':asyncio.run(main())
