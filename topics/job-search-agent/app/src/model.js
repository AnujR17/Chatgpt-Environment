export const STAGES = [
  { id: 'discovered', label: 'Discovered', help: 'Review the role and requirements' },
  { id: 'shortlisted', label: 'Shortlisted', help: 'Prepare your application' },
  { id: 'applied', label: 'Applied', help: 'Track replies and follow-ups' },
  { id: 'assessment', label: 'Assessment', help: 'Complete the next task' },
  { id: 'interview', label: 'Interview', help: 'Prepare and confirm the time' },
  { id: 'offer', label: 'Offer', help: 'Review the details' },
  { id: 'closed', label: 'Closed', help: 'Archived, rejected or withdrawn' },
];
export const KEYS = { overrides: 'design-jobs.overrides.v1', custom: 'design-jobs.custom.v1', profile: 'design-jobs.profile.v1' };
export const money = value => value == null ? 'Undisclosed' : `₹${Number(value).toLocaleString('en-IN')}`;
export function stipend(job) {
  if (job.payMin == null) return 'Stipend undisclosed';
  return `${money(job.payMin)}${job.payMax && job.payMax !== job.payMin ? `–${money(job.payMax)}` : ''}/mo`;
}
export function payMatch(job) {
  if (job.payMin == null || job.payVerified === false) return 'unconfirmed';
  const floor = job.region === 'Gujarat' ? 20000 : 30000;
  if (job.payMin >= floor) return 'meets';
  if (job.payMin >= 25000 || (job.payMax >= 25000 && job.payMin >= 20000)) return 'consider';
  return 'below';
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
  const columns = { company: 'Company', title: 'Role', location: 'Location', workMode: 'Work mode', payMin: 'Minimum INR/month', payMax: 'Maximum INR/month', payVerified: 'Pay confirmed in original listing', status: 'Status', nextAction: 'Next action', dueDate: 'Due date', interviewAt: 'Interview time', appliedAt: 'Applied date', sourceUrl: 'Source', applicationUrl: 'Apply link', email: 'Application email', evidence: 'Evidence', firstSeen: 'First discovered', checkedAt: 'Last checked', notes: 'Notes' };
  return '\ufeff' + [Object.values(columns).map(csvCell).join(','), ...jobs.map(job => Object.keys(columns).map(k => csvCell(job[k])).join(','))].join('\r\n');
}
export function validateBackup(value) {
  if (!value || value.version !== 1 || !Array.isArray(value.custom) || !value.overrides || typeof value.overrides !== 'object' || Array.isArray(value.overrides)) throw new Error('Choose a valid tracker JSON backup.');
  if (value.custom.length > 5000 || JSON.stringify(value).length > 5_000_000) throw new Error('Backup is too large.');
  for (const job of value.custom) if (!job.id || typeof job.id !== 'string' || !job.company || !job.title) throw new Error('Backup contains an invalid job.');
  for (const update of Object.values(value.overrides)) if (!update || typeof update !== 'object' || Array.isArray(update)) throw new Error('Backup contains invalid updates.');
  return value;
}
