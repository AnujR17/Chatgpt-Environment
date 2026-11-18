"""Export authored examples for the visual case study. No user data or camera inference."""
import json
from pathlib import Path
from checkpoint.blob import parameters
from checkpoint.session import Session
from checkpoint.attempts import guidance_mode, BY_KEY

ROOT=Path(__file__).resolve().parents[1]
rows=[]
for key,title,v,a in [('frustrated','Frustrated',-.7,.8),('exhausted','Drained',-.7,-.8),('calm','Calm',.6,-.6),('excited','Excited',.7,.8),('mixed','Not sure',None,None)]:
 s=Session();s.check_in(key,v,a)
 rows.append({'key':key,'label':title,'pleasantness':v,'activation':a,'mode':guidance_mode(s)[0],'art':parameters(None if key=='mixed' else key)})
family=[{'key':key,'label':title,'art':parameters(key)} for key,title in [('composed','Neutral'),('happy','Happy'),('amused','Laughing'),('frustrated','Frustrated'),('confused','Confused'),('determined','Determined'),('sad','Sad'),('surprised','Surprised')]]
data={'presets':rows,'family':family,'cue':BY_KEY['grip'].__dict__,'responses':{'pause':'Take a pause','continue':'Keep playing','smaller_goal':'Smaller goal'},'thresholds':{'pleasantness':-.18,'activation':.4,'freshness_seconds':300},'basis':'Authored interactive example. Not participant data or camera inference.'}
(ROOT/'docs/case-study/case-data.js').write_text('window.REGEN_CASE='+json.dumps(data,separators=(',',':'))+';\n')
