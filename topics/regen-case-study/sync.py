"""Build a standalone static website from the reviewed case study. No dependencies."""
import html
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'checkpoint/app/docs/case-study'
SITE=ROOT/'site'
SOURCE_REF='topic/checkpoint-case-study-20261118'
REPO='https://github.com/AnujR17/Chatgpt-Environment/blob/'+SOURCE_REF+'/'
PAGES={'PROJECT-CONTEXT.md':'project.html','CASE-STUDY.md':'research.html','FEASIBILITY.md':'feasibility.html'}


def target(value):
 if value in PAGES:return PAGES[value]
 if value.startswith('../../../research/'):return REPO+'topics/checkpoint/research/'+value.rsplit('/',1)[-1]
 if value.startswith('../'):return REPO+'topics/checkpoint/app/docs/'+value[3:]
 return value


def inline(value):
 value=html.escape(value)
 value=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:'<a href="'+html.escape(target(html.unescape(m[2])),quote=True)+'">'+m[1]+'</a>',value)
 value=re.sub(r'`([^`]+)`',r'<code>\1</code>',value)
 value=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',value)
 return value


def markdown(text):
 out=[];paragraph=[];listing=False
 def flush():
  if paragraph:out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
 for line in text.splitlines():
  if line.startswith('#'):
   flush()
   if listing:out.append('</ul>');listing=False
   mark,title=line.split(' ',1);level=min(len(mark),3);out.append(f'<h{level}>'+inline(title)+f'</h{level}>')
  elif line.startswith('- '):
   flush()
   if not listing:out.append('<ul>');listing=True
   out.append('<li>'+inline(line[2:])+'</li>')
  elif not line.strip():
   flush()
   if listing:out.append('</ul>');listing=False
  else:paragraph.append(line.strip())
 flush()
 if listing:out.append('</ul>')
 return '\n'.join(out)


def build():
 SITE.mkdir(parents=True,exist_ok=True)
 for name in ('index.html','case-study.css','case-study.js','case-data.js','Regen-case-study.pdf','sample-session-report.pdf','verification.json','phone-verification.json','visual-case-verification.json','windows-verification.json'):
  shutil.copy2(SOURCE/name,SITE/name)
 shutil.copytree(SOURCE/'assets',SITE/'assets',dirs_exist_ok=True)
 index=(SITE/'index.html').read_text()
 for original,url in PAGES.items():index=index.replace('href="'+original+'"','href="'+url+'"')
 (SITE/'index.html').write_text(index)
 for name,url in PAGES.items():
  content=markdown((SOURCE/name).read_text());title=(SOURCE/name).read_text().splitlines()[0].lstrip('# ')
  document='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+''' / Regen</title><link rel="icon" href="assets/regen.svg"><link rel="stylesheet" href="case-study.css"><style>.notes{max-width:920px;margin:0 auto;padding:60px 32px 90px}.notes h1{font-size:48px;margin-bottom:30px}.notes h2{font-size:27px;letter-spacing:-1px;line-height:1.2;margin:40px 0 15px}.notes p,.notes li{font-size:16px;line-height:1.75}.notes li{margin:8px 0}.notes a{overflow-wrap:anywhere}.notes code{font-size:13px;overflow-wrap:anywhere}.notes ul{padding-left:22px}@media(max-width:600px){.notes{padding:35px 23px}.notes h1{font-size:37px}.notes h2{font-size:24px}.notes p,.notes li{font-size:14px}}</style></head><body><header class="sitebar"><a class="wordmark" href="/"><img src="assets/regen.svg" alt="" width="30" height="30">regen</a><a href="/">Back to the case study</a></header><main class="notes">'''+content+'''</main></body></html>'''
  (SITE/url).write_text(document)
 (SITE/'vercel.json').write_text('''{\n  "$schema": "https://openapi.vercel.sh/vercel.json",\n  "version": 2,\n  "framework": null,\n  "buildCommand": "",\n  "installCommand": "",\n  "outputDirectory": "."\n}\n''')
 (SITE/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
 print('Static website ready:',SITE)


if __name__=='__main__':build()
