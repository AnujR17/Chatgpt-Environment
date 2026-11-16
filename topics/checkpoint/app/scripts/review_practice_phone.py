"""Actual native-to-HTTP-to-browser practice cue check; no physical phone claim."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from checkpoint.app import MainWindow, create_application
from checkpoint.attempts import start_attempt, finish_attempt
from checkpoint.phone import PhoneServer

OUT = Path(__file__).resolve().parents[1] / 'artifacts/session-review'


async def main():
    app = create_application([])
    window = MainWindow(no_setup=True, data_dir=OUT / 'phone-fixture')
    window.timer.stop()
    window.session.check_in('frustrated', -.7, .8)
    start_attempt(window.session, 'grip')
    window.next_export = 0.
    window.refresh()
    server = PhoneServer(window.phone_bridge, host='127.0.0.1', port=0).start()
    errors = []
    running = True

    async def pulse():
        while running:
            app.processEvents()
            await asyncio.sleep(.02)

    pump = asyncio.create_task(pulse())
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, executable_path=os.environ.get('CHECKPOINT_CHROMIUM'), args=['--no-sandbox'])
            page = await browser.new_page(viewport={'width':390, 'height':844})
            page.on('pageerror', lambda error: errors.append(str(error)))
            await page.goto(server.url('127.0.0.1'))
            await page.get_by_text('Try a shorter reach and a slower pull.', exact=True).wait_for()
            assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            OUT.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(OUT / 'next-attempt-phone.png'), full_page=True)
            finish_attempt(window.session, 'helped', 'Shorter reach')
            window.next_export = 0.
            window.refresh()
            await page.locator('#practice').wait_for(state='hidden')
            # The same PDF endpoint used by the phone includes the player's verdict.
            response = await page.request.get(f'http://127.0.0.1:{server.port}/api/report.pdf', headers={'Authorization':'Bearer '+server.token})
            assert response.ok and (await response.body()).startswith(b'%PDF-')
            start_attempt(window.session, 'orange', mode='small')
            window.next_export = 0.
            window.refresh()
            await page.get_by_text('Reach the first hold once, without chasing the next jump.', exact=True).first.wait_for()
            server.stop()
            await page.get_by_text('Disconnected', exact=True).wait_for(timeout=8000)
            assert await page.locator('#practice').is_hidden(), 'Disconnected cue must not look live'
            assert not errors, errors
            await browser.close()
        result = {'native_to_browser_cue': 'passed', 'outcome_clears_cue': 'passed',
                  'small_target': 'passed', 'pdf_endpoint': 'passed', 'disconnect_hides_cue': 'passed',
                  'viewport': '390x844, no horizontal overflow', 'javascript_errors': errors,
                  'physical_phone_network': 'not tested'}
        (OUT / 'practice-phone-verification.json').write_text(json.dumps(result, indent=2))
        print(json.dumps(result))
    finally:
        running = False
        await pump
        server.stop()
        window.close()
        app.processEvents()


if __name__ == '__main__':
    asyncio.run(main())
