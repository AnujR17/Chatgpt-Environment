"""Package reviewed extension files only. Never include browser state or credentials."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'extension'
FILES = ['manifest.json', 'capture.js', 'popup.html', 'popup.js', 'README.md', 'LICENSE']
output = ROOT / 'public/downloads/design-search-clipper.zip'
output.parent.mkdir(exist_ok=True)
with ZipFile(output, 'w') as archive:
    for name in FILES:
        info = ZipInfo(name, date_time=(2026, 11, 5, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, (SOURCE / name).read_bytes())
print(f'Packaged {output.name}: {len(FILES)} files, {output.stat().st_size} bytes')
