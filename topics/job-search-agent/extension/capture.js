// Adapted from Praful Aggarwal's MIT-licensed scrapeJobPage(). See LICENSE and README.
// This self-contained function runs only in the tab the user explicitly opens the popup on.
export function captureJobPage() {
  const clean = value => typeof value === 'string' ? value.replace(/\s+/g, ' ').trim() : '';
  const pick = selectors => {
    for (const selector of selectors) {
      const element = document.querySelector(selector);
      const text = clean(element?.innerText || element?.textContent);
      if (text) return text;
    }
    return '';
  };
  const plain = html => {
    if (!html) return '';
    const doc = new DOMParser().parseFromString(String(html), 'text/html');
    doc.querySelectorAll('script,style,noscript').forEach(node => node.remove());
    return clean(doc.body.textContent);
  };
  const host = location.hostname.replace(/^www\./, '');
  let title = '', company = '', description = '', rawCompensation = '', jobLocation = '', platform = 'Browser capture';
  if (host === 'naukri.com' || host.endsWith('.naukri.com')) {
    platform = 'Naukri';
    title = pick(['[class*="jd-header-title"]', 'h1']);
    company = pick(['[class*="jd-header-comp-name"] a', '[class*="jd-header-comp-name"]', '.comp-name']);
    description = pick(['[class*="JDC__dang-inner-html"]', '[class*="styles_JDC__job-desc"]', '[class*="job-desc-container"]', '.job-description', '[itemprop="description"]']);
    rawCompensation = pick(['[class*="jd-header-salary"]', '[class*="salary-wrap"]', '[itemprop="baseSalary"]']);
    jobLocation = pick(['[class*="jd-header-location"]', '[class*="loc-wrap"]']);
  } else if (host === 'linkedin.com' || host.endsWith('.linkedin.com')) {
    platform = 'LinkedIn';
    title = pick(['.job-details-jobs-unified-top-card__job-title', '.jobs-unified-top-card__job-title', '.topcard__title', 'h1']);
    company = pick(['.job-details-jobs-unified-top-card__company-name a', '.job-details-jobs-unified-top-card__company-name', '.jobs-unified-top-card__company-name', '.topcard__org-name-link']);
    description = pick(['.jobs-description__content', '.jobs-description-content__text', '.show-more-less-html__markup']);
    rawCompensation = pick(['.salary-main-rail__compensation-value', '.compensation__salary']);
    jobLocation = pick(['.job-details-jobs-unified-top-card__primary-description-container', '.topcard__flavor--bullet']);
  } else if (host === 'indeed.com' || host.endsWith('.indeed.com')) {
    platform = 'Indeed';
    title = pick(['[data-testid="jobsearch-JobInfoHeader-title"]', '.jobsearch-JobInfoHeader-title', 'h1']);
    company = pick(['[data-testid="inlineHeader-companyName"]', '[data-company-name="true"]', '.jobsearch-CompanyInfoContainer a']);
    description = pick(['#jobDescriptionText']);
    rawCompensation = pick(['#salaryInfoAndJobType', '[data-testid="attribute_snippet_testid"]']);
    jobLocation = pick(['[data-testid="inlineHeader-companyLocation"]', '#jobLocationText']);
  }
  let posting = null;
  const walk = value => {
    if (Array.isArray(value)) { value.forEach(walk); return; }
    if (!value || typeof value !== 'object') return;
    const types = [].concat(value['@type'] || []);
    if (!posting && types.includes('JobPosting')) posting = value;
    if (value['@graph']) walk(value['@graph']);
  };
  for (const node of document.querySelectorAll('script[type="application/ld+json"]')) {
    try { walk(JSON.parse(node.textContent)); } catch { /* Malformed metadata is not evidence. */ }
  }
  if (posting) {
    title ||= clean(posting.title);
    company ||= clean(typeof posting.hiringOrganization === 'string' ? posting.hiringOrganization : posting.hiringOrganization?.name);
    description ||= plain(posting.description);
    if (!jobLocation) jobLocation = [].concat(posting.jobLocation || []).map(item => {
      const address = item?.address;
      return typeof address === 'string' ? address : [address?.addressLocality, address?.addressRegion, typeof address?.addressCountry === 'object' ? address.addressCountry.name : address?.addressCountry].filter(Boolean).join(', ');
    }).filter(Boolean).join('; ');
    if (!rawCompensation && posting.baseSalary) rawCompensation = JSON.stringify(posting.baseSalary);
  }
  return {
    title: (title || pick(['h1'])).slice(0, 250), company: company.slice(0, 200),
    sourceUrl: location.href, platform, location: jobLocation.slice(0, 500),
    description: description.slice(0, 20000), rawCompensation: rawCompensation.slice(0, 1500),
    postedLabel: clean(posting?.datePosted).slice(0, 100), capturedAt: new Date().toISOString(),
  };
}
