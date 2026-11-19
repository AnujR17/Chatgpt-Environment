"""Build the visual PDF in release CI; publish large documents as release assets."""
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/case-study'
REVIEW = ROOT / 'artifacts/design-review'


def run():
    for name in ('session.png', 'play-reminder.png', 'recovery-frustrated.png',
                 'recovery-later.png', 'widget-break.png', 'reminder-overlay.png', 'recap.png', 'session-recap.png'):
        assert (REVIEW / name).is_file(), name
        shutil.copy2(REVIEW / name, SOURCE / 'assets' / name)
    candidates = [shutil.which('chromium'), shutil.which('google-chrome')]
    for variable in ('PROGRAMFILES', 'PROGRAMFILES(X86)', 'LOCALAPPDATA'):
        root = Path(os.environ.get(variable, '/not-installed'))
        candidates.extend([str(root / 'Google/Chrome/Application/chrome.exe'),
                           str(root / 'Microsoft/Edge/Application/msedge.exe')])
    browser = next((p for p in candidates if p and Path(p).is_file()), None)
    if not browser:
        raise RuntimeError('Chrome or Edge is required to print the visual case study')
    output = ROOT.parent / 'Regen-case-study.pdf'
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(SOURCE)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            chromium = p.chromium.launch(executable_path=browser, headless=True, args=['--no-sandbox'])
            page = chromium.new_page(viewport={'width':1440, 'height':1000}, reduced_motion='reduce')
            page.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            assert page.locator('#character-family .look').count() == 5
            assert page.locator('nav,button,input,select,details').count() == 0
            assert page.locator('img').evaluate_all('nodes => nodes.every(e => e.complete && e.naturalWidth > 0)')
            page.evaluate("""() => {for (const a of document.querySelectorAll('a')) {
                const v=a.getAttribute('href');
                if(v && !v.startsWith('#') && !v.startsWith('http'))
                  a.href='https://github.com/AnujR17/Chatgpt-Environment/blob/topic/regen-case-study-site/topics/checkpoint/app/docs/case-study/'+v;
            }}""")
            page.pdf(path=str(output), print_background=True, prefer_css_page_size=True, display_header_footer=False)
            chromium.close()
    finally:
        server.shutdown(); server.server_close()
    assert output.stat().st_size > 100_000 and output.read_bytes().startswith(b'%PDF-')
    print('Visual case study PDF ready:', output.stat().st_size, 'bytes')


if __name__ == '__main__':
    run()
