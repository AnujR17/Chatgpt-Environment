"""Generate auditable public hiring-post query links; never fetch or authenticate."""
import argparse
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def build_plan(config, day):
    if config.get('version') != 1 or not isinstance(config.get('targets'), list):
        raise ValueError('Expected version1 social watchlist with targets.')
    queries = [
        ('linkedin-posts-broad', 'LinkedIn posts', 'site:linkedin.com/posts/ ("product design intern" OR "UX intern" OR "interaction design intern") (hiring OR internship) (India OR Ahmedabad OR Bengaluru OR Mumbai OR remote)'),
        ('linkedin-updates-broad', 'LinkedIn updates', 'site:linkedin.com/feed/update/ ("design intern" OR "UX internship") (India OR remote)'),
        ('x-posts-broad', 'X', 'site:x.com ("product design intern" OR "UX intern" OR "design internship") (hiring OR portfolio) (India OR remote)'),
        ('naukri-design-broad', 'Naukri', 'site:naukri.com/job-listings ("UX" OR "product design") (intern OR internship) (Ahmedabad OR Gandhinagar OR remote)'),
    ]
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
    rows = [dict(id=qid, platform=platform, query=q,
                 searchUrl='https://www.google.com/search?'+urlencode({'q':q}),
                 status='not_searched', generatedFor=day)
            for qid, platform, q in queries]
    return dict(version=1, generatedFor=day, timezone='Asia/Kolkata',
                kind='Research query plan — not search results',
                limits='Generation performs no search or login. Actual queries, findings, access limits and dates must be recorded in sources.coverage.',
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
