"""Generate auditable public hiring-post query links; never fetch or authenticate."""
import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode, urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def build_plan(config, day):
    if config.get('version') != 1 or not isinstance(config.get('targets'), list):
        raise ValueError('Expected version1 social watchlist with targets.')
    as_of = date.fromisoformat(day)
    cutoff = as_of - timedelta(days=14)
    queries = [
        ('linkedin-posts-broad', 'LinkedIn posts', 'site:linkedin.com/posts/ ("product design intern" OR "UX intern" OR "interaction design intern") (hiring OR internship) (India OR Ahmedabad OR Bengaluru OR Mumbai OR remote)'),
        ('linkedin-updates-broad', 'LinkedIn updates', 'site:linkedin.com/feed/update/ ("design intern" OR "UX internship") (India OR remote)'),
        ('x-posts-broad', 'X', 'site:x.com ("product design intern" OR "UX intern" OR "design internship") (hiring OR portfolio) (India OR remote)'),
        ('naukri-design-broad', 'Naukri', 'site:naukri.com/job-listings ("UX" OR "product design") (intern OR internship) (Ahmedabad OR Gandhinagar OR remote)'),
    ]
    for qid, domain in [('indeed','in.indeed.com/viewjob'), ('wellfound','wellfound.com/jobs'),
                        ('cutshort','cutshort.io/job'), ('unstop','unstop.com/internships'),
                        ('internshala','internshala.com/internship/detail'), ('instahyre','instahyre.com'),
                        ('prosple','in.prosple.com'), ('hirist','hirist.tech'), ('foundit','foundit.in'),
                        ('apna','apna.co/job'), ('shine','shine.com/jobs'),
                        ('peerlist','peerlist.io/company'), ('freshersworld','freshersworld.com')]:
        queries.append((qid+'-design-broad', qid.title(),
                        f'site:{domain} ("UX" OR "product design") (intern OR internship) (India OR Ahmedabad OR Gandhinagar OR Bengaluru OR remote)'))
    seen = set()
    for target in config['targets']:
        tid, name = target.get('id'), target.get('name')
        if not tid or tid in seen or not isinstance(name, str) or not name.strip():
            raise ValueError('Targets require unique IDs and nonempty names.')
        seen.add(tid)
        for field in ['careersUrl', 'linkedinUrl']:
            if not target.get(field):
                continue
            url = urlparse(target[field])
            if url.scheme != 'https' or not url.hostname or url.username or url.password:
                raise ValueError('Watchlist links must be public HTTPS URLs without credentials.')
        # Quote source data as search text, not executable commands or guessed handles.
        term = name.replace('"', ' ').replace('\n', ' ').strip()
        queries.extend([
            (tid+'-linkedin-posts', 'LinkedIn posts', f'site:linkedin.com/posts/ "{term}" (intern OR internship OR hiring)'),
            (tid+'-linkedin-updates', 'LinkedIn company updates', f'site:linkedin.com/company/ "{term}" ("intern" OR "internship")'),
            (tid+'-x-posts', 'X', f'site:x.com "{term}" (intern OR internship OR hiring)'),
        ])
    rows = []
    for qid, platform, query in queries:
        social = platform.startswith('LinkedIn') or platform == 'X'
        if social:
            # Search filters narrow discovery; they never verify a post's date.
            query += f' after:{(cutoff-timedelta(days=1)).isoformat()} before:{(as_of+timedelta(days=1)).isoformat()}'
        row = dict(id=qid, platform=platform, query=query,
                   searchUrl='https://www.google.com/search?'+urlencode({'q':query}),
                   status='not_searched', generatedFor=day)
        if social:
            row['publicationWindow'] = {'from':cutoff.isoformat(), 'through':day}
        rows.append(row)
    return dict(version=1, generatedFor=day, timezone='Asia/Kolkata',
                kind='Research query plan — not search results',
                maxSocialPostAgeDays=14,
                socialPublicationCutoff=cutoff.isoformat(),
                limits='Generation performs no search or login. Social-only recommendations require a verified original publication within 14 days; crawl/repost/firstSeen dates and search date filters are not publication evidence. Older or undated posts remain historical research unless an independently current employer vacancy supports a separate recommendation. Record actual searches and limits in sources.coverage.',
                queries=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--watchlist', type=Path, default=ROOT/'public/data/social-watchlist.json')
    parser.add_argument('--output', type=Path, default=ROOT/'public/data/social-search-plan.json')
    parser.add_argument('--date', default=datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat())
    args = parser.parse_args()
    plan = build_plan(json.loads(args.watchlist.read_text()), args.date)
    args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n')
    print(f'Generated {len(plan["queries"])} query links; none marked searched.')


if __name__ == '__main__':
    main()
