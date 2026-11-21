"""Generate auditable public hiring-post query links; never fetch or authenticate."""
import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode, urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def search_term(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Search identities must be nonempty strings.')
    return ' '.join(value.replace('"', ' ').split())


DISCOVERY_QUERIES = [
    ('discovery-product-intern-simple', 'Employer discovery', '"product design intern" hiring'),
    ('discovery-ux-research-simple', 'Employer discovery', '"UX research intern" hiring India'),
    ('discovery-design-trainee-simple', 'Employer discovery', '"UI UX" (trainee OR apprentice) India hiring'),
    ('discovery-referral-roundups', 'Employer discovery', '("product design" OR "UX research") (intern OR internship) (referral OR PPO)'),
    ('discovery-form-destinations', 'Employer discovery', '("product design intern" OR "UX research intern") ("forms.gle" OR "docs.google.com/forms")'),
    ('discovery-linkedin-simple', 'LinkedIn posts', 'site:linkedin.com/posts/ "product design intern"'),
    ('discovery-employer-product', 'Employer discovery', '("product design intern" OR "UI/UX intern" OR "UX design intern") (careers OR hiring) (India OR remote) -site:linkedin.com -site:myinternships.in'),
    ('discovery-employer-studio', 'Employer discovery', '("design intern" OR "junior UX designer") (studio OR SaaS OR startup) (careers OR "join us") (India OR remote)'),
    ('discovery-gujarat', 'Employer discovery', '("UI/UX" OR "product design") (intern OR fresher OR "0–2") (Gandhinagar OR Ahmedabad OR Vadodara OR Surat) (careers OR hiring)'),
    ('discovery-south-west', 'Employer discovery', '("UX intern" OR "product design intern") (Pune OR Mumbai OR Hyderabad OR Bengaluru OR Chennai OR Goa OR Kerala) careers'),
    ('discovery-linkedin-posts', 'LinkedIn posts', 'site:linkedin.com/posts/ ("UI/UX" OR UIUX OR "product design") (intern OR fresher OR "0–2 years") (hiring OR portfolio)'),
    ('discovery-linkedin-authors', 'LinkedIn posts', 'site:linkedin.com/posts/ ("design intern" OR "UX intern") (founder OR recruiter OR "design lead" OR "send me")'),
    ('discovery-x-posts', 'X', 'site:x.com ("UI/UX" OR UIUX OR "product designer") (intern OR junior OR fresher) (hiring OR portfolio)'),
    ('discovery-employer-ats', 'Employer discovery', '(site:jobs.lever.co OR site:jobs.ashbyhq.com OR site:boards.greenhouse.io) ("design intern" OR "UX intern") (India OR remote)'),
    ('discovery-board-employers', 'Employer discovery', '(site:wellfound.com/jobs OR site:cutshort.io/job OR site:in.indeed.com/viewjob) ("design intern" OR "junior UX") (India OR remote)'),
    ('discovery-parent-alias', 'Employer discovery', '("UI/UX" OR "product design") (intern OR junior) ("parent company" OR "formerly" OR "part of") hiring'),
]

# The existing task switches to two independent research tracks on this date.
# Today's plan/layout is not changed into a junior search retrospectively.
TRACKS_START = date(2026, 11, 22)
JUNIOR_QUERIES = [
    ('junior-product-simple', 'Employer discovery', '"junior product designer" (India OR remote) hiring'),
    ('junior-ux-simple', 'Employer discovery', '"junior UX designer" India careers'),
    ('junior-uiux-fresher', 'Employer discovery', '"UI/UX designer" (fresher OR trainee) (India OR remote)'),
    ('junior-employer-ats', 'Employer discovery', '(site:jobs.lever.co OR site:jobs.ashbyhq.com OR site:boards.greenhouse.io) ("junior designer" OR "associate designer") India'),
    ('junior-boards', 'Employer discovery', '(site:wellfound.com/jobs OR site:cutshort.io/job OR site:in.indeed.com/viewjob) (junior OR fresher) (UX OR "product design") India'),
    ('junior-naukri', 'Naukri', 'site:naukri.com/job-listings (junior OR fresher) (UX OR "product designer")'),
    ('junior-linkedin-posts', 'LinkedIn posts', 'site:linkedin.com/posts/ ("junior product designer" OR "junior UX designer" OR "UIUX fresher") hiring'),
    ('junior-x-posts', 'X', 'site:x.com ("junior product designer" OR "junior UX designer" OR "UIUX fresher") hiring'),
]


def build_plan(config, day):
    if config.get('version') != 1 or not isinstance(config.get('targets'), list):
        raise ValueError('Expected version1 social watchlist with targets.')
    as_of = date.fromisoformat(day)
    cutoff = as_of - timedelta(days=14)
    queries = list(DISCOVERY_QUERIES) + (list(JUNIOR_QUERIES) if as_of >= TRACKS_START else []) + [
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
        term = search_term(name)
        queries.extend([
            (tid+'-linkedin-posts', 'LinkedIn posts', f'site:linkedin.com/posts/ "{term}" (intern OR internship OR hiring)'),
            (tid+'-linkedin-updates', 'LinkedIn company updates', f'site:linkedin.com/company/ "{term}" ("intern" OR "internship")'),
            (tid+'-x-posts', 'X', f'site:x.com "{term}" (intern OR internship OR hiring)'),
            (tid+'-linkedin-authors', 'LinkedIn posts', f'site:linkedin.com/posts/ "{term}" ("UI/UX" OR "product design" OR UIUX) (hiring OR portfolio OR intern)'),
        ])
        aliases = target.get('aliases', [])
        people = target.get('publicHiringPeople', [])
        if not isinstance(aliases, list) or not isinstance(people, list):
            raise ValueError('Aliases and public hiring people must be lists.')
        for i, alias in enumerate(aliases):
            alias = search_term(alias)
            queries.extend([
                (f'{tid}-alias-{i}-posts', 'LinkedIn posts', f'site:linkedin.com/posts/ "{alias}" ("UI/UX" OR design) (intern OR junior OR hiring)'),
                (f'{tid}-alias-{i}-careers', 'Employer discovery', f'"{alias}" ("UI/UX" OR "product design") (intern OR junior OR careers)'),
                (f'{tid}-alias-{i}-x', 'X', f'site:x.com "{alias}" (design OR UX) (intern OR hiring)'),
            ])
        for i, person in enumerate(people):
            person = search_term(person)
            queries.append((f'{tid}-person-{i}-posts', 'LinkedIn posts',
                            f'site:linkedin.com/posts/ "{person}" ("UI/UX" OR design) (hiring OR intern OR portfolio)'))
    rows = []
    for qid, platform, query in queries:
        social = platform.startswith('LinkedIn') or platform == 'X'
        if social:
            # Search filters narrow discovery; they never verify a post's date.
            query += f' after:{(cutoff-timedelta(days=1)).isoformat()} before:{(as_of+timedelta(days=1)).isoformat()}'
        row = dict(id=qid, platform=platform, query=query,
                   searchUrl='https://www.google.com/search?'+urlencode({'q':query}),
                   status='not_searched', generatedFor=day)
        row['phase'] = 'discovery' if qid.startswith('discovery-') or platform == 'Employer discovery' else ('boards' if not social else 'targets')
        if as_of >= TRACKS_START:
            row['roleTrack'] = 'Junior / fresher' if qid.startswith('junior-') else ('Cross-track discovery' if qid in {'discovery-design-trainee-simple','discovery-parent-alias','discovery-board-employers','discovery-linkedin-posts','discovery-x-posts'} else 'Internships')
        if social:
            row['publicationWindow'] = {'from':cutoff.isoformat(), 'through':day}
        rows.append(row)
    return dict(version=1, workflowVersion=3, generatedFor=day, timezone='Asia/Kolkata',
                kind='Research query plan — not search results',
                maxSocialPostAgeDays=14,
                socialPublicationCutoff=cutoff.isoformat(),
                roleTracksEffectiveFrom=TRACKS_START.isoformat(),
                roleTracks=['Junior / fresher','Internships'] if as_of >= TRACKS_START else ['Internships with clearly marked junior alternatives'],
                discoveryPolicy='Run discovery before watchlist rechecks. Follow new employer names to exact role pages, public hiring people and source-backed aliases/parents. Location-free social searches are discovery only; apply geography, age, level, pay and eligibility rules before recommending. Log actual queries, candidates, duplicates, exclusions and access gaps; never use query counts as a no-missed-jobs claim.',
                reviewPolicy='Reconcile plausible leads from supplied search receipts with discovery_audit.py. Account for profile hiring snippets, referral roundups and form destinations; preserve unresolved and outside-geography awareness separately from active recommendations. A recorded disposition is not vacancy verification. Read the discovery ledger and retry due unresolved leads before fixed-target rechecks.',
                limits='Generation performs no search or login. Social-only recommendations require a verified original publication within 14 days; crawl/repost/firstSeen dates and search date filters are not publication evidence. Older or undated posts remain historical research unless an independently current employer vacancy supports a separate recommendation. Record actual searches and limits in sources.coverage.',
                queries=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--watchlist', type=Path, default=ROOT/'public/data/social-watchlist.json')
    parser.add_argument('--output', type=Path, default=ROOT/'public/data/social-search-plan.json')
    parser.add_argument('--date', default=datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat())
    parser.add_argument('--phase', choices=['all', 'discovery', 'targets', 'boards'], default='all')
    args = parser.parse_args()
    plan = build_plan(json.loads(args.watchlist.read_text()), args.date)
    if args.phase != 'all':
        plan['queries'] = [q for q in plan['queries'] if q['phase'] == args.phase]
        plan['selectedPhase'] = args.phase
    args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n')
    print(f'Generated {len(plan["queries"])} query links; none marked searched.')


if __name__ == '__main__':
    main()
