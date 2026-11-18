"""Export the five primary Nori states used in the case study."""
import json
from pathlib import Path
from checkpoint.blob import parameters
from checkpoint.primary import PRIMARY_KEYS,PRIMARY_LABELS
from checkpoint.affect import REFERENCES
ROOT=Path(__file__).resolve().parents[1]
family=[{'key':key,'label':PRIMARY_LABELS[key],'art':parameters(key)} for key in PRIMARY_KEYS]
rows=[{'key':key,'label':PRIMARY_LABELS[key],'pleasantness':REFERENCES[key][1],'activation':REFERENCES[key][2],'art':parameters(key)} for key in PRIMARY_KEYS]
(ROOT/'docs/case-study/case-data.js').write_text('window.REGEN_CASE='+json.dumps({'family':family,'presets':rows},separators=(',',':'))+';\n')
