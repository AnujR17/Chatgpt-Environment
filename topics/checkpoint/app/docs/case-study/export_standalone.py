"""Pack the visual case into one offline HTML file. Standard-library development tool."""
import base64
import mimetypes
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
BASE='https://github.com/AnujR17/Chatgpt-Environment/blob/topic/checkpoint-case-study-20261118/topics/checkpoint/app/docs/case-study/'


def data(path):
 p=ROOT/path;mime=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()


def build():
 html=(ROOT/'index.html').read_text();css=(ROOT/'case-study.css').read_text()
 css=css.replace("url('assets/DM-Sans.ttf')","url('"+data('assets/DM-Sans.ttf')+"')")
 html=html.replace('<link rel="stylesheet" href="case-study.css">','<style>'+css+'</style>')
 scripts=[]
 for path in re.findall(r'<script defer src="([^"]+)"></script>',html):
  js=(ROOT/path).read_text()
  for asset in ('assets/dark.png','assets/session.png'):js=js.replace("'"+asset+"'","'"+data(asset)+"'")
  scripts.append('<script>'+js.replace('</script','<\\/script')+'</script>')
 html=re.sub(r'<script defer src="[^"]+"></script>','',html)
 html=re.sub(r'src="(assets/[^"]+)"',lambda m:'src="'+data(m[1])+'"',html)
 html=html.replace('href="assets/regen.svg"','href="'+data('assets/regen.svg')+'"')
 html=re.sub(r'href="(?!#|https?:|data:)([^"]+)"',lambda m:'href="'+BASE+m[1]+'"',html)
 html=html.replace('</body>',''.join(scripts)+'</body>')
 target=ROOT/'Regen.html';target.write_text(html);print(target)
 return target


if __name__=='__main__':build()
