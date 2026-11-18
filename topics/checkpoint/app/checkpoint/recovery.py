"""Player choices and reported changes. Association is not a cause of recovery."""
from collections import Counter

CHOICES={'pause':'Take a pause','continue':'Keep playing','smaller_goal':'Choose a smaller goal'}


def recovery_summary(session,points):
    choices=[]
    for i,row in enumerate(session.responses):
        stamp=row['elapsed_seconds']
        before=next((p for p in reversed(points) if p['elapsed_seconds']<=stamp),None)
        limit=session.responses[i+1]['elapsed_seconds'] if i+1<len(session.responses) else float('inf')
        after=next((p for p in points if stamp<p['elapsed_seconds']<limit),None)
        changes=None
        if before and after:
            changes={'pleasantness':round(after['pleasantness']-before['pleasantness'],3),
                     'activation':round(after['activation']-before['activation'],3)}
        choices.append({**row,'title':CHOICES[row['kind']],'before':before,'after':after,'change':changes})
    contexts=Counter(p.get('context','') for p in points if p['pleasantness']<-.18 and p['activation']>.4 and p.get('context'))
    helpful=Counter(CHOICES[r['kind']] for r in session.responses if r.get('helpful')=='yes')
    return {'choices':choices,'contexts':dict(contexts),'helpful':dict(helpful),
            'basis':'Player-reported moments and feedback. Changes between check-ins do not establish why they happened.'}
