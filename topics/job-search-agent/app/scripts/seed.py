"""Curated research snapshot, 23 October 2026. Run only to recreate the initial feed."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = '2026-10-23'
jobs = []

def add(id, company, title, location, workMode, region, sourceUrl, **kw):
    jobs.append(dict(id=id, company=company, title=title, location=location, workMode=workMode,
        region=region, sourceUrl=sourceUrl, applicationUrl=sourceUrl, payMin=None, payMax=None,
        payVerified=False, sourceType='Company careers', firstSeen=DAY, checkedAt=DAY,
        postedAt=None, postedLabel='Not stated', status='discovered', tags=[], **kw))

add('shramiksathi-4469701295','ShramikSathi','UI/UX Design Intern','Remote, India','Remote','India',
    'https://in.linkedin.com/jobs/view/ui-ux-design-intern-at-shramiksathi-4469701295')
jobs[-1].update(payMin=30000,payMax=30000,payVerified=True,sourceType='LinkedIn job',postedLabel='3 weeks ago when checked',
    email='info@shramiksathi.com',subject='UI/UX Design Intern',applicationUrl='mailto:info@shramiksathi.com',
    requirements='Figma, reusable components, design tokens, responsive and accessible interfaces, research and Hindi/English communication. Work includes worker-facing mobile flows and administrative dashboards. Internship: 3–6 months.',
    evidence='Employer-authored LinkedIn description explicitly states Remote (India) and ₹30,000/month. The job header says Bengaluru; the description confirms remote work. One opening listed.',
    applicationMethod='Email application; draft can be prepared',automationNotes='Prepare portfolio links and the requested design response, then review and send by email. No email has been sent.',
    applicationInstructions='Email a portfolio with 2–3 case studies and a response of up to 150 words: how should a worker confirm yesterday’s attendance on a small Android phone with an intermittent connection? No cover letter requested. Selection mentions a portfolio discussion, then a paid exercise.',
    tags=['UX','Product','Accessibility','Research'])
add('menstrupedia-ux-intern','Menstrupedia','UX Design Intern','Ahmedabad, Gujarat','On-site','Gujarat',
    'https://www.menstrupedia.com/careers/ux-intern')
jobs[-1].update(payMin=25000,payMax=30000,payVerified=True,
    requirements='Design web/mobile interfaces, test with users, collaborate with developers and measure outcomes. Visual design, typography, colour and English communication required. Past UX experience is desirable.',
    evidence='Company career page states internship, Ahmedabad office and ₹25,000–₹30,000/month. Meets the Gujarat minimum. Original posting date is not stated; confirm the opening is still available.',
    applicationUrl='https://forms.gle/fWuuGCFJwACS7uVa9',applicationMethod='Company application form',automationNotes='Form link is present on the employer page. Final fields, sign-in requirements and CAPTCHA have not been verified; use the original page to apply.',
    applicationInstructions='Use the company’s Apply link. The page also asks for a résumé and a paragraph explaining suitability, with subject Application for UX Design Intern.',tags=['UX','Research','Gujarat'])
add('more-retail-4477072502','More Retail','Product Design Intern','Bengaluru, Karnataka','On-site','Southern India',
    'https://in.linkedin.com/jobs/view/product-design-intern-at-more-retail-private-limited-4477072502')
jobs[-1].update(payMin=35000,payMax=35000,payVerified=True,sourceType='LinkedIn job',postedLabel='1 week ago when checked',
    requirements='Portfolio showing design decisions and process, Figma, user research and design systems. Pursuing or recently completed a relevant design/HCI degree. Internship duration: 3–6 months.',
    evidence='Employer-authored LinkedIn description states ₹35,000/month and Bengaluru. Remote work is not confirmed. Third-party ₹40,000 claims were not used.',
    applicationMethod='LinkedIn application',automationNotes='Requires your signed-in LinkedIn session. Treat as manual until the actual application flow is inspected.',tags=['Product','Figma','Research'])
add('bthree-4473077505','BThree Design Agency','Product Design Intern','Remote / hybrid, India','Unconfirmed','India',
    'https://in.linkedin.com/jobs/view/product-design-intern-at-bthree-design-agency-4473077505')
jobs[-1].update(payMin=20000,payMax=25000,payVerified=True,sourceType='LinkedIn job',postedLabel='3 weeks ago when checked',
    email='contact@bthreedesigns.com',applicationUrl='mailto:contact@bthreedesigns.com',
    requirements='Strong Framer implementation, Figma auto-layout/components, design systems and motion tools such as Jitter or Lottie. Three-month internship, immediate start, eight hours/day.',
    evidence='Original listing gives ₹20,000–₹25,000/month and Remote / Hybrid. Conditional only if ₹25,000 is agreed and fully remote work is confirmed; the advertised minimum falls below your general threshold.',
    applicationMethod='Email application; draft can be prepared',automationNotes='Prepare a personalised email and links. Confirm ₹25k and fully remote terms before committing. No message has been sent.',
    applicationInstructions='Send portfolio/work samples, 2–3 lines on work you enjoy and 2–3 lines on what you want to learn. Framer/motion examples are useful.',tags=['Product','Framer','Motion'])
add('wint-7515659430051426304','Wint Wealth','Product Design Intern','Bengaluru, Karnataka','On-site','Southern India',
    'https://www.linkedin.com/posts/sruthisivakumar_product-design-intern-wint-wealth-activity-7515659430051426304-tqUQ')
jobs[-1].update(sourceType='LinkedIn post',postedLabel='1 week ago when checked',applicationUrl='https://binary.so/P01RayN',
    requirements='Figma, product thinking, collaboration with product and engineering. Portfolio work on design systems is specifically encouraged.',
    evidence='A current post by the company’s co-founder/design leader confirms the internship and Bangalore office attendance. ₹30k–₹35k appears only in third-party listings; employer pay is unconfirmed.',
    applicationMethod='Recruiter-linked application form',automationNotes='The original post links to a Binary form. Inspect form requirements in your browser; submission and CAPTCHA behaviour are unverified.',tags=['Product','Design systems'])
add('hevo-433ffdef','Hevo Data','UX Design Intern','Bengaluru, Karnataka','On-site','Southern India',
    'https://jobs.lever.co/hevodata/433ffdef-3125-48ed-a131-52c697c321ee')
jobs[-1].update(applicationUrl='https://jobs.lever.co/hevodata/433ffdef-3125-48ed-a131-52c697c321ee/apply',
    requirements='Figma components and tokens, SaaS/dashboard interfaces, prototyping and developer handoff. AI-assisted design workflows are relevant.',
    evidence='Official employer Lever role and application page are accessible. On-site Bangalore; stipend and original publication date are not disclosed.',
    applicationMethod='Lever application form',automationNotes='Assisted form filling appears feasible after a résumé and accurate profile are supplied. Fields include résumé, name, email, phone and current company. Final validation/CAPTCHA unverified.',tags=['UX','SaaS','Design systems'])
add('revrag-product-design','RevRag AI','Product Design Intern','Bengaluru, Karnataka','On-site','Southern India',
    'https://www.revrag.ai/careers/product-design-intern')
jobs[-1].update(requirements='Strong portfolio, Figma variables/components, AI prototyping, interaction states and fintech workflows. Six-month internship.',
    evidence='Original company role is accessible and lists Bengaluru on-site. Third-party ₹40k claims are not confirmed by this page.',
    applicationMethod='Employer-linked Google Form',automationNotes='Open the company’s application form and select Product Design Intern. Required fields, authentication and CAPTCHA have not been verified.',tags=['Product','AI','Fintech'])
add('chiblu-design-intern','Chiblu','Product Design Intern (UX & UI)','Remote, India; Bengaluru preferred','Remote','India',
    'https://chiblu.com/careers/product-design-intern-ux-ui')
jobs[-1].update(postedAt='2026-05-05',postedLabel='5 May 2026 · older posting',email='apply@chiblu.com',applicationUrl='mailto:apply@chiblu.com',
    requirements='At least three portfolio projects, including end-to-end thinking and a mobile flow; Figma, visual craft, research and communication. Two months with possible extension.',
    evidence='Company still exposes the role page and links it from careers. It is an older May posting; current hiring and stipend require confirmation.',
    applicationMethod='Email or Wellfound',automationNotes='Email draft can be prepared. First confirm this older role remains open and meets the stipend requirement.',
    applicationInstructions='Share portfolio, a short reason for your interest, one project you would discuss and earliest start date.',tags=['Product','Marketplace','UX'])
add('neuralpath-design-intern','NeuralPath Technologies','Product Design Intern','Remote, India','Remote','India',
    'https://www.neuralpath.app/careers/')
jobs[-1].update(requirements='Figma, UI, prototypes and a portfolio. Students/recent graduates welcome; internships can fit around classes.',
    evidence='Company careers page explicitly lists a remote Product Design Intern opportunity and year-round applications. Duration and stipend are discussed individually.',
    applicationMethod='Email application via company page',automationNotes='Use the company’s email link to prepare an application with work samples and availability. Confirm the stipend first.',tags=['Product','Mobile','UI'])
add('krmr-design-intern','KRMR Solutions','UI/UX Product Design Intern','Remote, India','Remote','India',
    'https://krmrsolutions.com/careers/design-intern')
jobs[-1].update(requirements='Portfolio showing layout, typography and colour; Figma auto-layout and prototypes; component documentation and development handoff.',
    evidence='Original company career page confirms Remote (India) and internship. No stipend or publication date stated.',
    applicationMethod='LinkedIn link from employer page',automationNotes='Application link leads toward LinkedIn; signed-in flow and exact fields are unverified.',tags=['UX','Product','Design systems'])
add('zavio-design-intern','Zavio','Product Design Intern','Remote, India','Remote','India',
    'https://www.gozavio.com/careers')
jobs[-1].update(requirements='Research, wireframes, user flows and high-fidelity interfaces for financial education products.',
    evidence='Company careers page lists this as an open internship, remote anywhere in India. Stipend and posting date are not stated.',
    applicationMethod='Company application link',automationNotes='Open the original company Apply link. The final destination and form requirements need manual verification.',tags=['Product','Fintech','Research'])
add('gnixar-design-intern','Gnixar Academy','Product Design Intern','Remote, India (reported)','Remote','India',
    'https://www.jobleads.com/in/job/product-design-intern--india--e24abd61a6654a91f9a3af3bab3db8da5')
jobs[-1].update(sourceType='Job board',postedLabel='13 days ago on job board when checked',
    requirements='Visual and interaction design portfolio, Figma, prototyping and design-system contributions.',
    evidence='Job-board description reports remote India and ₹25k–₹40k/month, but its header conflicts on location and compensation. The company careers page dynamically loads roles; this role/pay remains unverified.',
    applicationMethod='Confirm on employer careers first',applicationUrl='https://www.gnixar.in/careers',automationNotes='Verify the opening, remote eligibility and stipend with the employer before sharing personal information. Third-party pay is not treated as confirmed.',tags=['Product','Education'])
add('glance-ux-intern','Glance','UX Design Intern','Bengaluru, Karnataka','Unconfirmed','Southern India',
    'https://www.studentsmart.co.in/student/internships/glance-ux-design-intern')
jobs[-1].update(sourceType='Job board',postedAt='2026-10-15',postedLabel='15 October 2026 on job board',
    requirements='UX/visual design for TV shopping interfaces, design systems, interaction states, engineering handoff and interest in AI/ambient computing.',
    evidence='StudentSmart reports ₹30k–₹40k/month and Bengaluru; original employer confirmation and work arrangement are still needed.',
    applicationMethod='Job-board sign-in; find original employer listing',automationNotes='StudentSmart requires login/identity details before redirecting. Prefer verifying the original Glance opportunity first.',tags=['UX','Interaction','AI'])

excluded = [
 dict(company='Appbrew',reason='Previously indexed Wellfound role returned HTTP 410 Gone; excluded as an active opening.',url='https://wellfound.com/jobs/3340685-product-design-intern'),
 dict(company='Parallel',reason='Third-party role returned HTTP 410 Gone. General careers page alone does not confirm an internship or stipend.',url='https://www.parallelhq.com/careers'),
 dict(company='CrossBo',reason='Remote recruiter post is approximately seven months old; stipend and current hiring not confirmed.',url='https://www.linkedin.com/posts/hiring-uidesign-uxdesign-share-7442792683330449409-yy0E'),
 dict(company='Ourora',reason='Remote internship is explicitly unpaid and falls below your stipend requirements.',url='https://wellfound.com/jobs/4748674-product-design-intern'),
 dict(company='Trinance',reason='Hyderabad on-site internship lists ₹20,000/month, below your non-Gujarat minimum.',url='https://in.linkedin.com/jobs/view/product-design-intern-at-trinance-4461895853'),
 dict(company='hussh Pune',reason='Stale snippet advertises ₹40k, but the current page gives no stipend and describes a campus challenge/probation process; keep outside confirmed matches.',url='https://careers.hussh.ai/open-roles/ui-ux-product-design-intern-pune'),
 dict(company='X',reason='Searched public indexed hiring posts; no independently verified qualifying original post found in this pass.',url=None),
]
meta = dict(researchedAt=DAY,collectorLastRun=None,scheduleStatus='Daily collection configured; first scheduled run pending.',
    coverage='Research snapshot across company careers, LinkedIn jobs/posts and public job boards; X searched without a qualifying verified result.',excluded=excluded)
out=ROOT/'public/data'
out.mkdir(parents=True,exist_ok=True)
(out/'jobs.json').write_text(json.dumps(dict(meta=meta,jobs=jobs),ensure_ascii=False,indent=2)+'\n')
sources=[]
for j in jobs:
    sources.append(dict(id=j['id'],company=j['company'],url=j['sourceUrl'],kind='social' if j['sourceType']=='LinkedIn post' else 'role', jobId=j['id'],titlePattern=j['title'],lastStatus='pending'))
sources += [dict(id='gnixar-careers',company='Gnixar Academy',url='https://www.gnixar.in/careers',kind='careers',lastStatus='pending'),dict(id='hevo-careers',company='Hevo Data',url='https://api.lever.co/v0/postings/hevodata?mode=json',kind='lever',lastStatus='pending')]
(out/'sources.json').write_text(json.dumps(dict(sources=sources),ensure_ascii=False,indent=2)+'\n')
(out/'review-queue.json').write_text(json.dumps(dict(updatedAt=None,candidates=[]),indent=2)+'\n')
print(f'Wrote {len(jobs)} curated opportunities and {len(sources)} sources.')
