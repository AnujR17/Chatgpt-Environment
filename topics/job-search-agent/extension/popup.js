import { captureJobPage } from './capture.js';

const fields = ['title', 'company', 'location', 'rawCompensation', 'description'];
const $ = id => document.getElementById(id);
const key = 'design-search.captures.v1';
let current = null;
const message = text => { $('message').textContent = text; };
const readQueue = async () => { const data = await chrome.storage.local.get(key); return Array.isArray(data[key]) ? data[key] : []; };
const validUrl = value => { try { return ['https:', 'http:'].includes(new URL(value).protocol); } catch { return false; } };
const identity = value => {
  const url = new URL(value); url.hash = '';
  for (const name of [...url.searchParams.keys()]) if (/^(utm_|trk|tracking|ref$)/i.test(name)) url.searchParams.delete(name);
  return url.href;
};
async function readPage() {
  $('save').disabled = true; current = null;
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!validUrl(tab?.url)) throw Error('Open a job detail page in a regular browser tab.');
    const [result] = await chrome.scripting.executeScript({ target: { tabId: tab.id }, func: captureJobPage });
    current = result?.result;
    if (!current || !validUrl(current.sourceUrl)) throw Error('Could not read this page. Open the job detail and try again.');
    fields.forEach(name => { $(name).value = current[name] || ''; });
    $('save').disabled = false;
    message(current.description ? 'Check the captured details before saving.' : 'The description was not readable. Paste the job description below.');
  } catch (error) { message(error.message || 'The browser did not allow reading this page.'); }
}
$('capture-form').addEventListener('submit', async event => {
  event.preventDefault();
  if (!current || $('save').disabled) return;
  $('save').disabled = true;
  try {
    const capture = { ...current, ...Object.fromEntries(fields.map(name => [name, $(name).value.trim()])), capturedAt: new Date().toISOString() };
    if (!capture.title || !capture.company || !capture.description) throw Error('Role, company and job description are required.');
    const queue = await readQueue();
    const index = queue.findIndex(item => identity(item.sourceUrl) === identity(capture.sourceUrl));
    if (index < 0 && queue.length >= 100) throw Error('Export or clear the 100 saved captures before adding more.');
    if (index < 0) queue.push(capture); else queue[index] = capture;
    await chrome.storage.local.set({ [key]: queue });
    message(`${index < 0 ? 'Saved for review.' : 'Updated the existing capture.'} ${queue.length} capture${queue.length === 1 ? '' : 's'} ready to export.`);
  } catch (error) { message(error.message || 'Could not save. Your earlier captures are retained.'); }
  finally { $('save').disabled = false; }
});
$('reread').addEventListener('click', readPage);
$('export').addEventListener('click', async () => {
  try {
    const candidates = await readQueue();
    if (!candidates.length) { message('No captures to export.'); return; }
    const payload = { format: 'design-job-captures', version: 1, exportedAt: new Date().toISOString(), candidates };
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a'); link.href = url; link.download = 'design-job-captures.json'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    message(`Exported ${candidates.length} captures. Import the file in your board. The local copies are retained.`);
  } catch { message('Could not export the captures. Try again.'); }
});
$('clear').addEventListener('click', async () => {
  if (!confirm('Clear captured jobs from this extension? Export a copy first if needed. Your board is unaffected.')) return;
  try { await chrome.storage.local.set({ [key]: [] }); message('Extension captures cleared.'); } catch { message('Could not clear the captures.'); }
});
readPage();
