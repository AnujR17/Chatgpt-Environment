export const STAGES = [
  { id: 'discovered', label: 'Discovered', help: 'Review the role and requirements' },
  { id: 'shortlisted', label: 'Shortlisted', help: 'Prepare your application' },
  { id: 'on_hold', label: 'On hold', help: 'Confirm pay, eligibility or timing' },
  { id: 'applied', label: 'Applied', help: 'Track replies and follow-ups' },
  { id: 'assessment', label: 'Assessment', help: 'Complete the next task' },
  { id: 'interview', label: 'Interview', help: 'Prepare and confirm the time' },
  { id: 'offer', label: 'Offer', help: 'Review the details' },
  { id: 'closed', label: 'Closed', help: 'Archived, rejected or withdrawn' },
];
export const KEYS = { overrides: 'design-jobs.overrides.v1', custom: 'design-jobs.custom.v1', profile: 'design-jobs.profile.v1', companies: 'design-jobs.companies.v1' };
export const PLATFORM_FILTERS = ['Company careers','Indeed','Naukri','Cutshort','YC / Work at a Startup','Wellfound','Remote boards','Hacker News','LinkedIn','X','Job board'];
export function platformName(value) {
  const source = String(value || '').toLowerCase();
  if (/hacker news|who is hiring|news\.ycombinator|hnhiring/.test(source)) return 'Hacker News';
  if (/ycombinator|work.?at.?a.?startup|workatastartup|^yc\b/.test(source)) return 'YC / Work at a Startup';
  if (/wellfound|angel\.co/.test(source)) return 'Wellfound';
  if (/remote boards|remoteok|remote ok|weworkremotely|we work remotely|remotive|himalayas|workingnomads|working nomads|remote\.co/.test(source)) return 'Remote boards';
  if (source.includes('linkedin')) return 'LinkedIn';
  if (source.includes('indeed')) return 'Indeed';
  if (source.includes('naukri')) return 'Naukri';
  if (source.includes('cutshort')) return 'Cutshort';
  if (source === 'x' || source.includes('twitter') || source.includes('x.com/')) return 'X';
  if (source.includes('company')) return 'Company careers';
  return source.includes('manual') ? 'Manual' : 'Job board';
}
export function platforms(job) {
  return [...new Set([platformName(job.sourceType), ...(job.additionalSources || []).map(source => platformName(source.platform || source.url))])];
}
export const money = value => value == null ? 'Undisclosed' : `₹${Number(value).toLocaleString('en-IN')}`;
export function compensationText(compensation) {
  if (!compensation || compensation.min == null || !['INR','USD'].includes(compensation.currency) || !['year','month'].includes(compensation.period)) return '';
  const format = value => `${compensation.currency === 'INR' ? '₹' : 'USD '}${Number(value).toLocaleString(compensation.currency === 'INR' ? 'en-IN' : 'en-US')}`;
  return `${format(compensation.min)}${compensation.max && compensation.max !== compensation.min ? `–${format(compensation.max)}` : ''}/${compensation.period}`;
}
export function stipend(job) {
  if (job.payMin == null) return compensationText(job.advertisedCompensation) || 'Pay not disclosed';
  return `${money(job.payMin)}${job.payMax && job.payMax !== job.payMin ? `–${money(job.payMax)}` : ''}/mo`;
}
export function payMatch(job) {
  if (job.advertisedCompensation?.period === 'year' && job.advertisedCompensation.verified === true) return 'annual';
  if (job.payMin == null || job.payVerified !== true) return job.payBenchmark?.sourceUrl ? 'estimated' : 'unconfirmed';
  const floor = job.region === 'Gujarat' ? 20000 : 30000;
  if (job.payMin >= floor) return 'meets';
  if (job.payMin >= 25000 || (job.payMax >= 25000 && job.payMin >= 20000)) return 'consider';
  return 'below';
}
export function benchmarkText(benchmark) {
  if (!benchmark || benchmark.min == null) return 'No reliable design-intern pay range found';
  const range = `${money(benchmark.min)}${benchmark.max && benchmark.max !== benchmark.min ? `–${money(benchmark.max)}` : ''}`;
  return `${range}/${benchmark.period === 'year' ? 'year' : 'month'} ${benchmark.kind === 'Employer-listed stipend' ? 'in employer listing' : 'reported'}`;
}
export function roleType(job) { return job.roleType || 'Internship'; }
export function isPipeline(job) { return ['shortlisted','applied','assessment','interview','offer'].includes(job.status); }
export const companyKey = name => String(name || '').toLowerCase().replace(/[^a-z0-9]/g, '');
export function companyMatches(company, name) {
  const key = companyKey(name);
  return !!key && [company.name, company.company, ...(company.aliases || [])].some(value => companyKey(value) === key);
}
export function mergeCompanies(feed, overrides) {
  const known = new Set(feed.map(c => c.id));
  return [...feed.map(c => ({...c, ...overrides[c.id]})), ...Object.entries(overrides).filter(([id,c]) => !known.has(id) && c?.name).map(([id,c]) => ({id,tier:'Possible',companyType:'Unclassified',...c}))];
}
export function mergeCompanyPreferences(existing, incoming) {
  const merged = {...existing};
  for (const [id, update] of Object.entries(incoming)) {
    const previous = existing[id] || {};
    const assessments = {...previous.assessments};
    for (const [role, criteria] of Object.entries(update.assessments || {})) assessments[role] = {...assessments[role], ...criteria};
    merged[id] = {...previous, ...update, ...(Object.keys(assessments).length ? {assessments} : {})};
  }
  return merged;
}
export function isCompanyBlocked(job, companies) {
  return companies.some(c => c.blacklisted === true && (job.companyId === c.id || companyMatches(c, job.company)));
}
export function fitSummary(requirements = [], assessment = {}) {
  const result = {total:requirements.length, met:0, partial:0, gap:0, unknown:0};
  requirements.forEach((requirement, i) => {
    const state = assessment[requirement.id || String(i)]?.state;
    result[['met','partial','gap'].includes(state) ? state : 'unknown']++;
  });
  return {...result, percent:result.total ? Math.round(result.met / result.total * 100) : null, assessed:result.total - result.unknown};
}
export function safeUrl(value) {
  try { const url = new URL(value); return ['https:', 'http:', 'mailto:'].includes(url.protocol) ? url.href : ''; } catch { return ''; }
}
export function canonicalUrl(value) {
  try { const url = new URL(value); url.hash = ''; for (const k of [...url.searchParams.keys()]) if (/^(utm_|ref$|trk$|tracking)/i.test(k)) url.searchParams.delete(k); return url.href.replace(/\/$/, ''); } catch { return ''; }
}
export function mergeJobs(feed, custom, overrides) {
  const seen = new Set();
  return [...custom, ...feed].filter(job => {
    if (!job || !job.id || !job.company || !job.title || seen.has(job.id)) return false;
    seen.add(job.id); return true;
  }).map(job => ({ status: 'discovered', notes: '', nextAction: '', dueDate: '', appliedAt: '', events: [], ...job, ...overrides[job.id], id: job.id, status: STAGES.some(s => s.id === overrides[job.id]?.status) ? overrides[job.id].status : (STAGES.some(s => s.id === job.status) ? job.status : 'discovered') }));
}
export function dateLabel(value) {
  if (!value) return 'Not set';
  const date = new Date(value.length === 10 ? `${value}T12:00:00` : value);
  return Number.isNaN(date.valueOf()) ? 'Not set' : date.toLocaleDateString('en-IN', {day: 'numeric', month: 'short', year: 'numeric'});
}
export function localDate(date = new Date()) {
  return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
}
export function isDue(job, today = localDate()) {
  return !!job.dueDate && job.dueDate.slice(0,10) <= today && !['closed','offer'].includes(job.status);
}
export function csvCell(value) {
  const text = String(value ?? '');
  // Avoid spreadsheet formula evaluation of imported or user-provided text.
  return `"${(/^[\s]*[=+@-]/.test(text) ? "'" : '') + text.replaceAll('"', '""')}"`;
}
export function toCsv(jobs) {
  const columns = { company: 'Company', title: 'Role', roleType: 'Role type', location: 'Location', workMode: 'Work mode', payMin: 'Minimum INR/month', payMax: 'Maximum INR/month', payVerified: 'Pay confirmed in original listing', listedCompensation: 'Listed salary / original units', benchmarkSummary: 'Reported pay (not current offer)', status: 'Status', nextAction: 'Next action', dueDate: 'Due date', interviewAt: 'Interview time', appliedAt: 'Applied date', sourceType: 'Platform', sourceUrl: 'Source', applicationUrl: 'Apply link', email: 'Application email', evidence: 'Evidence', firstSeen: 'First discovered', checkedAt: 'Last checked', notes: 'Notes' };
  return '\ufeff' + [Object.values(columns).map(csvCell).join(','), ...jobs.map(job => Object.keys(columns).map(k => csvCell(k === 'listedCompensation' ? compensationText(job.advertisedCompensation) || job.advertisedCompensation?.label || '' : job[k])).join(','))].join('\r\n');
}
export function validateBackup(value) {
  if (!value || value.version !== 1 || !Array.isArray(value.custom) || !value.overrides || typeof value.overrides !== 'object' || Array.isArray(value.overrides)) throw new Error('Choose a valid tracker JSON backup.');
  if (value.custom.length > 5000 || JSON.stringify(value).length > 5_000_000) throw new Error('Backup is too large.');
  for (const job of value.custom) if (!job.id || typeof job.id !== 'string' || !job.company || !job.title) throw new Error('Backup contains an invalid job.');
  for (const update of Object.values(value.overrides)) if (!update || typeof update !== 'object' || Array.isArray(update)) throw new Error('Backup contains invalid updates.');
  if (value.companyOverrides !== undefined) {
    if (!value.companyOverrides || typeof value.companyOverrides !== 'object' || Array.isArray(value.companyOverrides)) throw new Error('Backup contains invalid company preferences.');
    for (const update of Object.values(value.companyOverrides)) {
      if (!update || typeof update !== 'object' || Array.isArray(update) || (update.blacklisted !== undefined && typeof update.blacklisted !== 'boolean')) throw new Error('Backup contains invalid company preferences.');
    }
  }
  return value;
}
