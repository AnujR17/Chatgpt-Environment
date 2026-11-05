// Browser captures are untrusted, private intake. Never accept applicant or stage fields from them.
import { canonicalUrl, companyMatches, isCompanyBlocked } from './model.js';

export const isCaptureFile = value => value?.format === 'design-job-captures';
const text = (value, max) => typeof value === 'string' ? value.trim().slice(0, max) : '';
function sourceUrl(value) {
  if (typeof value !== 'string' || value.length > 4000) throw Error('A capture has an invalid source URL.');
  let url; try { url = new URL(value); } catch { throw Error('A capture has an invalid source URL.'); }
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) throw Error('Capture sources must be HTTP or HTTPS pages without credentials.');
  return canonicalUrl(url.href);
}
function sourceIdentity(value) {
  const url = new URL(value);
  const host = url.hostname.toLowerCase().replace(/^www\./, '');
  if (host === 'linkedin.com' || host.endsWith('.linkedin.com')) {
    const id = url.pathname.match(/\/jobs\/view\/(?:.*-)?(\d+)\/?$/)?.[1] || url.searchParams.get('currentJobId');
    if (id && /^\d+$/.test(id)) return `linkedin:${id}`;
  }
  if (host === 'naukri.com' || host.endsWith('.naukri.com')) {
    const id = url.pathname.match(/-(\d{6,})\/?$/)?.[1];
    if (id) return `naukri:${id}`;
  }
  if (host === 'indeed.com' || host.endsWith('.indeed.com')) {
    const id = url.searchParams.get('jk') || url.searchParams.get('vjk');
    if (id) return `indeed:${id}`;
  }
  return value.replace(/\/$/, '');
}
export async function prepareCapturedJobs(payload, { jobs = [], companies = [], now = new Date() } = {}) {
  if (!isCaptureFile(payload) || payload.version !== 1 || !Array.isArray(payload.candidates) || payload.candidates.length > 100) throw Error('Choose a version 1 job-capture file with at most 100 captures.');
  // Validate every item before producing any state update.
  const captures = payload.candidates.map(item => {
    if (!item || typeof item !== 'object') throw Error('A capture is invalid.');
    const title = text(item.title, 250), company = text(item.company, 200), description = text(item.description, 20000);
    if (!title || !company || !description) throw Error('Every capture needs a role, company and job description.');
    return { title, company, description, sourceUrl: sourceUrl(item.sourceUrl), location: text(item.location, 500), rawCompensation: text(item.rawCompensation, 1500), postedLabel: text(item.postedLabel, 100), capturedAt: text(item.capturedAt, 100) };
  });
  const known = new Set();
  for (const job of jobs) for (const value of [job.sourceUrl, job.applicationUrl, ...(job.additionalSources || []).map(item => item.url)]) {
    try { known.add(sourceIdentity(sourceUrl(value))); } catch { /* Non-web application routes do not identify a page. */ }
  }
  const result = { jobs: [], duplicates: 0, blocked: 0, unpaid: 0 };
  const day = now.toISOString().slice(0, 10);
  for (const capture of captures) {
    const employer = companies.find(item => companyMatches(item, capture.company));
    const base = { company: capture.company, ...(employer ? { companyId: employer.id } : {}) };
    if (isCompanyBlocked(base, companies)) { result.blocked++; continue; }
    if (/\bunpaid\b/i.test(capture.rawCompensation)) { result.unpaid++; continue; }
    const identity = sourceIdentity(capture.sourceUrl);
    if (known.has(identity)) { result.duplicates++; continue; }
    known.add(identity);
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(identity));
    const id = 'capture-' + [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('').slice(0, 24);
    const host = new URL(capture.sourceUrl).hostname.toLowerCase();
    const platform = /(^|\.)naukri\.com$/.test(host) ? 'Naukri' : /(^|\.)linkedin\.com$/.test(host) ? 'LinkedIn job' : /(^|\.)indeed\.com$/.test(host) ? 'Indeed' : 'Browser capture';
    result.jobs.push({
      ...base, id, title: capture.title, sourceUrl: capture.sourceUrl, applicationUrl: capture.sourceUrl,
      sourceType: platform, location: capture.location || 'Location unconfirmed', workMode: 'Unconfirmed', region: 'Unconfirmed', roleType: 'Unclassified capture',
      status: 'on_hold', payMin: null, payMax: null, payVerified: false, firstSeen: day, checkedAt: null, postedAt: null,
      postedLabel: capture.postedLabel ? `Captured date label (unverified): ${capture.postedLabel}` : 'Original posting date not established',
      requirements: capture.description, summary: 'Browser capture; role type, pay, location and current intake need review.',
      evidence: `Captured from the page you viewed; not independently verified.${capture.rawCompensation ? ` Pay text as captured: ${capture.rawCompensation}` : ' No pay captured.'}`,
      nextAction: 'Verify the original employer, digital-design scope, seniority, India/location eligibility, current intake, joining dates and stipend units before shortlisting. Saving is not applying.',
      tags: ['Browser capture', 'Unverified terms'], listingVerification: 'browser-capture-unverified',
      browserCapture: { capturedAt: capture.capturedAt || null, importedAt: now.toISOString(), rawCompensation: capture.rawCompensation },
    });
  }
  return result;
}
