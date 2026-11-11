export const SCREEN_LABELS = {
  unassessed: 'Lala-style screen: unassessed',
  'processes-documented': 'Lala-style screen: processes documented',
  'terms-concerns': 'Lala-style screen: check terms',
};
export const LALA_DEFINITION_URL = 'https://www.business-standard.com/article/beyond-business/surviving-in-india-s-family-owned-company-122081801424_1.html';
export function establishedEmployer(company) {
  return company?.employerProfile?.status === 'established' && !!company.employerProfile.sources?.length;
}
export function screeningStatus(company) {
  const review = company?.workplaceReview;
  return review?.sources?.length && Object.hasOwn(SCREEN_LABELS, review.status) ? review.status : 'unassessed';
}
export function personalLalaFlag(company) {
  return ['yes','no','unknown'].includes(company?.lalaAssessment?.value) ? company.lalaAssessment.value : 'unknown';
}
export function matchesEmployerScreen(company, filter) {
  if (filter === 'all') return true;
  if (filter === 'my-yes' || filter === 'my-no') return personalLalaFlag(company) === filter.slice(3);
  return screeningStatus(company) === filter;
}
