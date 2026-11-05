from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]/'figma-design';APP=ROOT.parent/'checkpoint'
s=json.loads((ROOT/'cards-app-state.json').read_text());s={k:s[k] for k in ['pageId','variables','metrics','palettes','styles','colorCollection','primitiveCollection','modes','artComponents','unreportedComponent','cardComponent','cardProperties']}
data=json.loads((APP/'design/native-app-geometry.json').read_text());keys=list(data)
positions={'session':[0,0],'dark':[1540,0],'empty':[3080,0],'common':[0,1100],'all':[1220,1100],'search':[2440,1100],'settings':[3000,2200],'break':[3800,2200],'summary':[3800,3240]}
for i,key in enumerate(k for k in keys if k.startswith('checkin_')):positions[key]=[i%3*920,2200+i//3*690]
for i,key in enumerate(k for k in keys if k.startswith('session_')):positions[key]=[9500+i%3*1540,i//3*1040]
helper=(ROOT/'emotion-motion-helpers.js').read_text();builder=(ROOT/'cards-app-view-helpers.js').read_text()
batches=[];batch={}
for key in keys:
    test={**s,'screenBatch':{**batch,key:data[key]},'positions':positions}
    code=helper.replace('__STATE__',json.dumps(test,separators=(',',':')))+builder
    if len(code)>47000 and batch:batches.append(batch);batch={key:data[key]}
    else:batch[key]=data[key]
if batch:batches.append(batch)
index=int(sys.argv[1]) if len(sys.argv)>1 else 0
s['screenBatch']=batches[index];s['positions']=positions
code=helper.replace('__STATE__',json.dumps(s,separators=(',',':')))+builder
Path('/tmp/cards-app-views.js').write_text(code)
print(json.dumps({'batch':index,'total':len(batches),'screens':list(batches[index]),'characters':len(code)}))
