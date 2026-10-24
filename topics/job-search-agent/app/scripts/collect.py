"""Read public career pages. Never submit applications or solve access challenges.

Known pages are monitored for changes; supported JobPosting JSON-LD and Lever
feeds supply new candidates. Unverified candidates are kept in a review queue.
"""
import argparse
import hashlib
import ipaddress
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ROOT = Path(__file__).resolve().parents[1]
UA = 'DesignInternshipTracker/1.0 (personal internship discovery; read-only)'
MAX_BYTES = 4_000_000

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.text=[]; self.links=[]; self.scripts=[]; self.ignored=0; self.json_script=False; self.buf=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('script','style','noscript'):
            self.ignored+=1
            if tag=='script' and d.get('type','').split(';')[0]=='application/ld+json': self.json_script=True;self.buf=[]
        if tag=='a' and d.get('href'): self.links.append(d['href'])
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript'):
            if self.json_script and tag=='script':
                try:self.scripts.append(json.loads(''.join(self.buf)))
                except (ValueError,TypeError):pass
                self.json_script=False;self.buf=[]
            self.ignored=max(0,self.ignored-1)
    def handle_data(self,data):
        if self.json_script:self.buf.append(data)
        elif not self.ignored:self.text.append(data)
    def visible(self):return re.sub(r'\s+',' ',' '.join(self.text)).strip()

def safe_remote(url):
    parsed=urlparse(url)
    if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password: return False
    host=parsed.hostname.lower()
    if host=='localhost' or host.endswith(('.local','.internal','.localhost')):return False
    try:return ipaddress.ip_address(host).is_global
    except ValueError:return True

def fetch(url):
    if not safe_remote(url):raise ValueError('Only public HTTPS sources are supported.')
    with urlopen(Request(url,headers={'User-Agent':UA,'Accept':'text/html, application/json;q=0.9'}),timeout=18) as response:
        if not safe_remote(response.url): raise ValueError('Unsupported redirect destination.')
        data=response.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES:raise ValueError('Source exceeded size limit.')
        return data.decode('utf-8',errors='replace'),response.url

def job_objects(value):
    if isinstance(value,list):
        for item in value:yield from job_objects(item)
    elif isinstance(value,dict):
        types=value.get('@type',[])
        if 'JobPosting' in ([types] if isinstance(types,str) else types):yield value
        if '@graph' in value:yield from job_objects(value['@graph'])

def relevant(title):
    return bool(re.search(r'\bintern(?:ship)?\b',title,re.I) and re.search(r'\b(?:ux|ui|product|interaction|experience)\b',title,re.I) and re.search(r'design',title,re.I))

def location_supported(location,remote=False):
    text=location.lower()
    if remote:
        return any(v in text for v in ['india','worldwide','anywhere','global'])
    return any(v in text for v in ['gujarat','ahmedabad','surat','vadodara','rajkot','gandhinagar','pune','mumbai','bengaluru','bangalore','hyderabad','chennai','trivandrum','thiruvananthapuram','goa','mysore','mysuru','puducherry','pondicherry','ooty','visakhapatnam','vishakapatnam','kochi','coimbatore','mangalore','mangaluru','kerala'])

def extract_schema(item,url,company,day):
    title=item.get('title','')
    if not relevant(title):return None
    locations=item.get('jobLocation',[])
    if isinstance(locations,dict):locations=[locations]
    parts=[]
    for location in locations:
        address=location.get('address',{}) if isinstance(location,dict) else {}
        if isinstance(address,str):parts.append(address)
        elif isinstance(address,dict):parts.extend(str(address[k]) for k in ['addressLocality','addressRegion','addressCountry'] if address.get(k))
    remote=item.get('jobLocationType','').upper()=='TELECOMMUTE'
    eligibility=item.get('applicantLocationRequirements',[])
    if isinstance(eligibility,dict):eligibility=[eligibility]
    parts.extend(e.get('name','') for e in eligibility if isinstance(e,dict))
    location=', '.join(dict.fromkeys(parts)) or 'Location unconfirmed'
    if not location_supported(location,remote):return None
    role_url=urljoin(url,item.get('url') or url)
    if not safe_remote(role_url):return None
    description=Page();description.feed(item.get('description',''))
    return dict(id='auto-'+hashlib.sha256(role_url.encode()).hexdigest()[:14],company=company,title=title,
        sourceUrl=role_url,applicationUrl=role_url,location=location,workMode='Remote' if remote else 'Unconfirmed',
        region='Gujarat' if any(x in location.lower() for x in ['gujarat','ahmedabad','surat','rajkot','vadodara','gandhinagar']) else 'India',
        sourceType='Company careers',payMin=None,payMax=None,payVerified=False,status='on_hold',roleType='Internship',
        firstSeen=day,checkedAt=day,postedAt=item.get('datePosted'),postedLabel=item.get('datePosted') or 'Not stated',
        evidence='Automatically discovered in a public employer JobPosting feed. Confirm role, remote eligibility, pay and current availability before applying.',
        requirements=description.visible()[:1800],applicationMethod='Employer application; review required',
        automationNotes='Only discovery is automated. Application fields and any access challenges have not been checked.',tags=[],reviewRequired=True)

def lever_candidates(data,source,day):
    if not isinstance(data,list):return
    for post in data:
        title=post.get('text','')
        if not relevant(title):continue
        cats=post.get('categories',{})
        loc=cats.get('location','')
        if not location_supported(loc):continue
        url=post.get('hostedUrl','')
        if not safe_remote(url):continue
        item=dict(title=title,url=url,description=post.get('description',''),jobLocation={'address':loc})
        candidate=extract_schema(item,url,source.get('company',''),day)
        if candidate:
            candidate['applicationUrl']=post.get('applyUrl',url)
            candidate['workMode']={'remote':'Remote','hybrid':'Hybrid','on-site':'On-site'}.get(post.get('workplaceType'),'Unconfirmed')
            yield candidate

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--data-dir',type=Path,default=ROOT/'public/data');args=parser.parse_args()
    directory=args.data_dir
    source_data=json.loads((directory/'sources.json').read_text())
    data=json.loads((directory/'jobs.json').read_text())
    queue_path=directory/'review-queue.json'
    queue=json.loads(queue_path.read_text()) if queue_path.exists() else {'candidates':[]}
    queued={j['sourceUrl']:j for j in queue['candidates']}
    known_urls={j['sourceUrl'].rstrip('/') for j in data['jobs']}
    known_signatures={(j['company'].casefold(),j['title'].casefold()) for j in data['jobs']}
    robots={};now=datetime.now(timezone.utc).isoformat(timespec='seconds');day=now[:10];counts={}
    by_id={j['id']:j for j in data['jobs']}
    for source in source_data['sources']:
        url=source['url'];source['lastChecked']=now
        try:
            if not safe_remote(url):raise ValueError('Unsupported source URL.')
            parsed=urlparse(url);origin=f'{parsed.scheme}://{parsed.netloc}'
            if origin not in robots:
                try:
                    raw,_=fetch(origin+'/robots.txt');rp=RobotFileParser();rp.parse(raw.splitlines());robots[origin]=rp
                except HTTPError as error:
                    if error.code==404:robots[origin]=True
                    else:robots[origin]=False
                except (URLError,TimeoutError,OSError,ValueError):robots[origin]=False
            allowed=robots[origin]
            if not allowed or (isinstance(allowed,RobotFileParser) and not allowed.can_fetch(UA,url)):
                source.update(lastStatus='blocked',message='Manual check required: robots policy unavailable or disallows automated fetch.');counts['blocked']=counts.get('blocked',0)+1;continue
            raw,final_url=fetch(url)
            candidates=[]
            if source['kind']=='lever':
                candidates=list(lever_candidates(json.loads(raw),source,day));text=raw
            else:
                page=Page();page.feed(raw);text=page.visible()
                if any(s in text.lower() for s in ['verify you are human','unusual traffic','access denied','complete the captcha']):
                    source.update(lastStatus='blocked',message='Access challenge detected; manual check required.');counts['blocked']=counts.get('blocked',0)+1;continue
                for obj in page.scripts:
                    for item in job_objects(obj):
                        candidate=extract_schema(item,final_url,source.get('company',''),day)
                        if candidate:candidates.append(candidate)
            digest=hashlib.sha256(text.encode()).hexdigest()
            changed=bool(source.get('contentHash') and source['contentHash']!=digest)
            source.update(lastStatus='changed' if changed else 'ok',message='Content changed; review the employer listing.' if changed else 'Public page fetched; hiring availability still needs employer confirmation.',contentHash=digest)
            existing=by_id.get(source.get('jobId'))
            # A successful HTTP response alone must not count as verification.
            if existing and existing['title'].lower() in text.lower():existing['lastPageFetched']=day
            elif existing:source.update(lastStatus='changed',message='Role title not found in visible page text; check for removed or dynamically loaded content.')
            for candidate in candidates:
                signature=(candidate['company'].casefold(),candidate['title'].casefold())
                if candidate['sourceUrl'].rstrip('/') not in known_urls and signature not in known_signatures:
                    if candidate['sourceUrl'] not in queued:queued[candidate['sourceUrl']]=candidate
                    else:queued[candidate['sourceUrl']]['checkedAt']=day
            counts[source['lastStatus']]=counts.get(source['lastStatus'],0)+1
        except HTTPError as error:
            state='missing' if error.code in (404,410) else 'blocked' if error.code in (401,403,429) else 'error'
            source.update(lastStatus=state,message=f'HTTP {error.code}; no application attempted.');counts[state]=counts.get(state,0)+1
        except (URLError,TimeoutError,OSError,ValueError,TypeError) as error:
            source.update(lastStatus='error',message=f'{type(error).__name__}; manual review required.');counts['error']=counts.get('error',0)+1
        print(f"{source['id']}: {source['lastStatus']}",flush=True)
    data['meta']['collectorLastRun']=now
    data['meta']['scheduleStatus']='Collector result recorded. Daily search is managed by the connected task; the optional repository cron requires default-branch setup.'
    data['meta']['collectorSummary']=counts
    queue={'updatedAt':now,'candidates':list(queued.values())}
    for path,value in [(directory/'sources.json',source_data),(directory/'jobs.json',data),(queue_path,queue)]:
        path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    report=[f'# Collection report — {day}', '',f'Checked {len(source_data["sources"])} sources. Review queue: {len(queued)} candidates.','',
        'This collector never submits applications, bypasses CAPTCHA or confirms that a vacancy remains open.','',
        '| Company | Result | Notes |','| --- | --- | --- |']
    for s in source_data['sources']:report.append(f"| {s['company']} | {s['lastStatus']} | {s.get('message','')} |")
    (directory/'collection-report.md').write_text('\n'.join(report)+'\n')
    print(json.dumps(dict(sources=len(source_data['sources']),results=counts,reviewCandidates=len(queued))))

if __name__=='__main__':main()
