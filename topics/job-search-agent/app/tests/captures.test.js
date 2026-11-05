import test from 'node:test';
import assert from 'node:assert/strict';
import { prepareCapturedJobs } from '../src/captures.js';
import { mergeJobs } from '../src/model.js';

const capture = changes => ({title:'UX Design Intern',company:'Example Studio',description:'Research, wireframes and prototypes.',sourceUrl:'https://www.naukri.com/job-listings-design-example-123456789',rawCompensation:'INR 2,40,000 per year',location:'Ahmedabad',...changes});
const file = candidates => ({format:'design-job-captures',version:1,candidates});
const now = new Date('2026-11-05T10:00:00Z');

test('captures keep salary/date/location/classification unverified and reject forged application state',async()=>{
 const {jobs}=await prepareCapturedJobs(file([capture({status:'applied',payMin:20000,payVerified:true,postedAt:'2026-11-05',profile:{name:'Never import'},notes:'Never overwrite'})]),{now});
 const job=jobs[0];
 assert.equal(job.status,'on_hold');assert.equal(job.payMin,null);assert.equal(job.payMax,null);assert.equal(job.payVerified,false);assert.equal(job.postedAt,null);assert.equal(job.checkedAt,null);
 assert.equal(job.workMode,'Unconfirmed');assert.equal(job.roleType,'Unclassified capture');assert.match(job.evidence,/2,40,000 per year/);
 assert.equal(job.profile,undefined);assert.equal(job.notes,undefined);assert.equal(job.browserCapture.importedAt,now.toISOString());
});
test('platform job identity deduplicates tracking URLs, cross-domain LinkedIn links and known crossposts',async()=>{
 const known=[{id:'retained',company:'Example',title:'Design',sourceUrl:'https://in.linkedin.com/jobs/view/ux-at-example-12345',additionalSources:[{url:'https://in.indeed.com/viewjob?jk=abcdef'}]}];
 const a=await prepareCapturedJobs(file([capture({sourceUrl:'https://www.linkedin.com/jobs/view/12345?trk=foo'}),capture({sourceUrl:'https://in.indeed.com/viewjob?jk=abcdef&utm_source=test'})]),{jobs:known,now});
 assert.equal(a.jobs.length,0);assert.equal(a.duplicates,2);
 const b=await prepareCapturedJobs(file([capture(),capture({sourceUrl: capture().sourceUrl+'?utm_source=test'})]),{now});
 assert.equal(b.jobs.length,1);assert.equal(b.duplicates,1);
 const c=await prepareCapturedJobs(file([capture()]),{jobs:b.jobs,now});assert.equal(c.jobs.length,0);
});
test('blacklist aliases and explicit unpaid text are respected without changing existing progress',async()=>{
 const existing={id:'history',company:'Blocked Studio',title:'UX',status:'interview',notes:'Retain'};
 const companies=[{id:'blocked',name:'Blocked Studio',aliases:['Blocked India'],blacklisted:true}];
 const result=await prepareCapturedJobs(file([capture({company:'Blocked India'}),capture({company:'Other',rawCompensation:'Unpaid internship'})]),{jobs:[existing],companies,now});
 assert.equal(result.blocked,1);assert.equal(result.unpaid,1);assert.equal(result.jobs.length,0);
 assert.equal(existing.status,'interview');assert.equal(existing.notes,'Retain');
 assert.equal(mergeJobs([existing],[],{history:{status:'applied',notes:'Existing notes'}})[0].notes,'Existing notes');
});
test('capture validation is atomic and allows no executable/credential-bearing source URLs',async()=>{
 for(const sourceUrl of ['javascript:alert(1)','data:text/html,bad','https://user:secret@example.org/job'])await assert.rejects(prepareCapturedJobs(file([capture({sourceUrl})]),{now}));
 await assert.rejects(prepareCapturedJobs(file([capture(),capture({company:''})]),{now}));
 await assert.rejects(prepareCapturedJobs({...file([]),version:2},{now}));
 await assert.rejects(prepareCapturedJobs(file(Array(101).fill(capture())),{now}));
});
test('crossposts with different identities are not silently merged by employer/title',async()=>{
 const result=await prepareCapturedJobs(file([capture(),capture({sourceUrl:'https://example.org/careers/design-intern'})]),{now});
 assert.equal(result.jobs.length,2);assert.notEqual(result.jobs[0].id,result.jobs[1].id);
});
