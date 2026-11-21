"""Account for a bounded search-result sample before publishing research.

This does not search, authenticate, verify vacancies or submit applications.
It detects unreviewed plausible leads in supplied public-search receipts.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

OUTCOMES = {'feed', 'duplicate', 'watchlist', 'historical', 'excluded', 'unresolved', 'not_role'}
ROLE = re.compile(r'(?:\b(?:ux|ui|uiux|hci)\b|product\s+design|interaction\s+design|design\s+intern)', re.I)
LEVEL = re.compile(r'\b(?:intern(?:ship)?s?|junior|fresher|trainee|apprentice)\b', re.I)


def candidates(receipts, max_per_batch=None):
    found = {}; errors = []; omitted = 0
    batches = receipts.get('batches', [])
    if not isinstance(batches, list) or not batches:
        raise ValueError('Provide nonempty search receipt batches.')
    for index, batch in enumerate(batches):
        result = batch.get('result', {})
        if result.get('status') == 'fulfilled':
            result = result.get('value', {})
        texts = [c.get('text', '') for c in result.get('content', []) if c.get('type') == 'text']
        if result.get('isError') or not texts or any('ClientResponseError' in t for t in texts):
            errors.append(str(batch.get('id', index)))
            continue
        selected = 0
        for text in texts:
            for block in re.split(r'\n-{20,}\n', text):
                match = re.search(r'^([^\n]+)\((https?://[^\n]+)\)\s*\n', block.strip())
                if not match:
                    continue
                title, url = match.group(1).strip(), match.group(2)
                sample = title + ' ' + block[:1600]
                if not ROLE.search(sample) or not LEVEL.search(sample):
                    continue
                if url in found:
                    found[url]['receiptBatches'].append(str(batch.get('id', index)))
                    continue
                if max_per_batch is not None and selected >= max_per_batch:
                    omitted += 1
                    continue
                parsed = urlparse(url)
                if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
                    continue
                selected += 1
                found[url] = dict(id='discovery-'+hashlib.sha256(url.encode()).hexdigest()[:14],
                                  sourceUrl=url, title=title,
                                  receiptBatches=[str(batch.get('id', index))])
    return dict(candidates=list(found.values()), receiptErrors=errors,
                omittedCandidates=omitted, sampleOnly=max_per_batch is not None,
                limits='Only supplied receipt text and the declared sample are audited. A pass is accounting, not vacancy verification, full source coverage or a no-missed-jobs guarantee.')


def audit(inventory, decisions, jobs=None, companies=None):
    entries = decisions.get('entries', [])
    by_url = {}; invalid = []
    for entry in entries:
        url = entry.get('sourceUrl')
        if url in by_url:
            invalid.append(dict(sourceUrl=url, error='Duplicate decision source URL'))
        by_url[url] = entry
    missing = []
    for candidate in inventory['candidates']:
        entry = by_url.get(candidate['sourceUrl'])
        if entry is None:
            missing.append(candidate)
            continue
        problems = []
        if entry.get('id') != candidate['id']:
            problems.append('Stable candidate ID differs')
        if entry.get('disposition') not in OUTCOMES:
            problems.append('Unknown disposition')
        for key in ['checkedAt', 'reason', 'nextAction']:
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                problems.append('Missing '+key)
        if entry.get('disposition') == 'unresolved' and not entry.get('recheckAfter'):
            problems.append('Unresolved lead needs recheckAfter')
        if entry.get('disposition') in {'feed', 'duplicate'}:
            if not entry.get('jobId') or (jobs is not None and entry['jobId'] not in jobs):
                problems.append('Feed/duplicate requires an existing stable job ID')
        if entry.get('disposition') == 'watchlist':
            if not entry.get('companyId') or (companies is not None and entry['companyId'] not in companies):
                problems.append('Watchlist requires an existing company ID')
        if problems:
            invalid.append(dict(sourceUrl=candidate['sourceUrl'], error='; '.join(problems)))
    return dict(passed=not missing and not invalid and not inventory['receiptErrors'] and not inventory['omittedCandidates'],
                candidateCount=len(inventory['candidates']), accountedCount=len(inventory['candidates'])-len(missing),
                unresolvedCount=sum(by_url.get(c['sourceUrl'],{}).get('disposition')=='unresolved' for c in inventory['candidates']),
                missing=missing, invalid=invalid, receiptErrors=inventory['receiptErrors'],
                omittedCandidates=inventory['omittedCandidates'], sampleOnly=inventory['sampleOnly'],
                limits=inventory['limits'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--receipts', type=Path, required=True)
    p.add_argument('--decisions', type=Path)
    p.add_argument('--inventory', type=Path, help='Optional explicit output for candidate inventory; never modifies feeds.')
    p.add_argument('--max-per-batch', type=int)
    p.add_argument('--jobs', type=Path)
    p.add_argument('--companies', type=Path)
    args = p.parse_args()
    if args.max_per_batch is not None and args.max_per_batch < 1:
        p.error('max-per-batch must be positive')
    inventory = candidates(json.loads(args.receipts.read_text()), args.max_per_batch)
    if args.inventory:
        args.inventory.write_text(json.dumps(inventory, ensure_ascii=False, indent=2)+'\n')
    if not args.decisions:
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
        return
    jobs = {j['id'] for j in json.loads(args.jobs.read_text())['jobs']} if args.jobs else None
    companies = {c['id'] for c in json.loads(args.companies.read_text())['companies']} if args.companies else None
    result = audit(inventory, json.loads(args.decisions.read_text()), jobs, companies)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
