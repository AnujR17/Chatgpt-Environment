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
PAGES={'PROJECT-CONTEXT.md':'project.html','CASE-STUDY.md':'research.html','FEASIBILITY.md':'feasibility.html','RESEARCH-EVIDENCE.md':'evidence.html','INTERVIEW-GUIDE.md':'interview-guide.html'}


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
 lines=text.splitlines();out=[];paragraph=[];listing=False;table=False
 def flush():
  if paragraph:out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
 def cells(line):return [part.strip() for part in line.strip().strip('|').split('|')]
 for i,line in enumerate(lines):
  if line.startswith('|'):
   flush()
   if listing:out.append('</ul>');listing=False
   parts=cells(line)
   if all(re.fullmatch(r':?-+:?',part) for part in parts):continue
   if not table:
    out.append('<div class="table-wrap" role="region" tabindex="0" aria-label="Research table"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in parts)+'</tr></thead><tbody>');table=True
   else:out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in parts)+'</tr>')
   continue
  if table:out.append('</tbody></table></div>');table=False
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
 if table:out.append('</tbody></table></div>')
 return '\n'.join(out)


def build():
 SITE.mkdir(parents=True,exist_ok=True)
 for stale in ('scenarios.html','verification.json','phone-verification.json','visual-case-verification.json','windows-verification.json','recovery-verification.json','play-support-verification.json','Regen-case-study.pdf'):
  (SITE/stale).unlink(missing_ok=True)
 for name in ('index.html','case-study.css','case-study.js','case-data.js','sample-session-report.pdf'):
  shutil.copy2(SOURCE/name,SITE/name)
 shutil.copytree(SOURCE/'assets',SITE/'assets',dirs_exist_ok=True)
 index=(SITE/'index.html').read_text()
 for original,url in PAGES.items():index=index.replace('href="'+original+'"','href="'+url+'"')
 (SITE/'index.html').write_text(index)
 for name,url in PAGES.items():
  content=markdown((SOURCE/name).read_text());title=(SOURCE/name).read_text().splitlines()[0].lstrip('# ')
  document='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+''' / Regen</title><link rel="icon" href="assets/regen.svg"><link rel="stylesheet" href="case-study.css"><style>.back-link{max-width:920px;margin:25px auto 0;padding:0 32px;font-size:14px}.notes{max-width:920px;margin:0 auto;padding:60px 32px 90px}.notes h1{font-size:48px;margin-bottom:30px}.notes h2{font-size:27px;letter-spacing:-1px;line-height:1.2;margin:40px 0 15px}.notes p,.notes li{font-size:16px;line-height:1.75}.notes li{margin:8px 0}.notes a{overflow-wrap:anywhere}.notes code{font-size:13px;overflow-wrap:anywhere}.notes ul{padding-left:22px}.table-wrap{max-width:100%;overflow:auto;margin:20px 0 30px}.notes table{border-collapse:collapse;width:100%;font-size:13px;line-height:1.6}.notes th,.notes td{min-width:170px;padding:14px 12px;text-align:left;vertical-align:top;border-bottom:1px solid #cbd4c5}.notes th{background:#e5eadc;font-weight:600}.table-wrap:focus-visible{outline:2px solid #315d45;outline-offset:3px}@media(max-width:600px){.notes{padding:35px 23px}.notes h1{font-size:37px}.notes h2{font-size:24px}.notes p,.notes li{font-size:14px}}</style></head><body><p class="back-link"><a href="/">Back to the case study</a></p><main class="notes">'''+content+'''</main></body></html>'''
  (SITE/url).write_text(document)
 (SITE/'vercel.json').write_text('''{\n  "$schema": "https://openapi.vercel.sh/vercel.json",\n  "version": 2,\n  "framework": null,\n  "buildCommand": "",\n  "installCommand": "",\n  "outputDirectory": "."\n}\n''')
 (SITE/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
 print('Static website ready:',SITE)


if __name__=='__main__':build()
