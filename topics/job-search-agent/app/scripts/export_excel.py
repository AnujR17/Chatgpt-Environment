"""Export the researched feed, source evidence and blank application tracking fields."""
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'public/data/jobs.json').read_text())
sources=json.loads((ROOT/'public/data/sources.json').read_text())
wb=Workbook();ws=wb.active;ws.title='Internships'
columns={'company':'Company','title':'Role','roleType':'Role type','location':'Location','workMode':'Work mode','payMin':'Minimum INR/month','payMax':'Maximum INR/month','payVerified':'Pay confirmed in original','status':'Status','nextAction':'Next action','dueDate':'Due date','interviewAt':'Interview time','appliedAt':'Applied date','sourceType':'Platform','sourceUrl':'Original source','applicationUrl':'Application link','email':'Application email','applicationMethod':'Application route','evidence':'Evidence / caveats','requirements':'Requirements','applicationInstructions':'Application instructions','postedLabel':'Posted','firstSeen':'First discovered','checkedAt':'Last checked','notes':'Personal notes'}
ws.append(list(columns.values()))
for job in data['jobs']:
 row=[]
 for key in columns:
  value=job.get(key,'')
  if isinstance(value,str) and value.lstrip().startswith(('=','+','-','@')):value="'"+value
  row.append(value)
 ws.append(row)
 for column in (15,16):
  cell=ws.cell(ws.max_row,column)
  if isinstance(cell.value,str) and cell.value.startswith(('https://','mailto:')):cell.hyperlink=cell.value;cell.style='Hyperlink'
status=DataValidation(type='list',formula1='"discovered,shortlisted,on_hold,applied,assessment,interview,offer,closed"');ws.add_data_validation(status);status.add('I2:I10000')
ws.freeze_panes='C2';ws.auto_filter.ref=ws.dimensions
for col in ws.columns:
 letter=col[0].column_letter
 ws.column_dimensions[letter].width=55 if letter in ['M','N','Q','R','S'] else 27
for row in ws.iter_rows(min_row=2):
 for cell in row:cell.alignment=Alignment(vertical='top',wrap_text=True)
 ws.row_dimensions[row[0].row].height=95
ss=wb.create_sheet('Sources');ss.append(['Company','URL','Type','Fetch result','Last fetch','Notes'])
for s in sources['sources']:ss.append([s['company'],s['url'],s['kind'],s.get('lastStatus',''),s.get('lastChecked',''),s.get('message','')])
ss.freeze_panes='A2';ss.auto_filter.ref=ss.dimensions
company_path=ROOT/'public/data/companies.json'
if company_path.exists():
 cs=wb.create_sheet('Company watchlist')
 cs.append(['Company','Suggested category','Why this target','Pay evidence type','Reported role','Range minimum','Range maximum','Original period','Confidence','Limitations','Careers URL','Pay source','Observed date'])
 for company in json.loads(company_path.read_text()).get('companies',[]):
  benchmark=company.get('payBenchmark') or {}
  cs.append([company['name'],company['tier'],company['rationale'],benchmark.get('kind','Not established'),benchmark.get('role',''),benchmark.get('min'),benchmark.get('max'),benchmark.get('period',''),benchmark.get('confidence','Unconfirmed'),company.get('payNote',''),company.get('careersUrl',''),benchmark.get('sourceUrl',''),company.get('researchedAt','')])
  for column in (11,12):
   cell=cs.cell(cs.max_row,column)
   if isinstance(cell.value,str) and cell.value.startswith('https://'):cell.hyperlink=cell.value;cell.style='Hyperlink'
 cs.freeze_panes='C2';cs.auto_filter.ref=cs.dimensions
 tiers=DataValidation(type='list',formula1='"Dream,Workable,Possible"');cs.add_data_validation(tiers);tiers.add('B2:B10000')
notes=wb.create_sheet('Read me')
for row in [
 ['Design internship search','Research snapshot: '+data['meta']['researchedAt']],
 ['Priority','Remote India, then Gujarat/Maharashtra/Goa/southern India.'],
 ['Stipend','Gujarat minimum INR20,000/month; elsewhere INR30,000+, INR25,000 conditional. Remote floor provisionally INR30,000.'],
 ['Evidence','Only employer-stated minimums count as confirmed. Undisclosed-pay roles stay on hold. Glassdoor and other company reports are historical context, never a current offer. Annual figures stay annual.'],
 ['Company groups','Dream / Workable / Possible are editable suggestions, not hiring probabilities. The company watchlist does not assert current vacancies or offers.'],
 ['Freshness','Discovery date is not posting date. An accessible listing does not guarantee current hiring.'],
 ['Applications','No applications have been submitted. Status and application fields are for you to update.'],
 ['Board vs Excel','This workbook contains the research snapshot. Browser board changes are exported separately using CSV or JSON backup.'],
 ['Privacy','Initial workbook contains no résumé or personal contact data. Employer application contacts are public listing details.'],
 ['Excluded roles','See the exclusion list below.'],
 *[[x['company'],x['reason']] for x in data['meta']['excluded']]
]:notes.append(row)
for sheet in wb:
 for cell in sheet[1]:cell.font=Font(bold=True,color='FFFFFF');cell.fill=PatternFill('solid',fgColor='343D2B');cell.alignment=Alignment(wrap_text=True)
 sheet.row_dimensions[1].height=29
 if sheet!=ws:
  for col in sheet.columns:sheet.column_dimensions[col[0].column_letter].width=35 if col[0].column==1 else 75
  for row in sheet.iter_rows(min_row=2):
   for cell in row:cell.alignment=Alignment(wrap_text=True,vertical='top')
   sheet.row_dimensions[row[0].row].height=42
wb.save(ROOT/'public/data/internships.xlsx')
print('Exported internships.xlsx')
