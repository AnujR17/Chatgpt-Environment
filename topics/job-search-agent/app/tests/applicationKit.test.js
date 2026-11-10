import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequest,sourceHash,validateRequest,importResult,editDocument,submissionSnapshot,requestPrompt,RESULT_FORMAT} from '../src/applicationKit.js';
import {validateBackup} from '../src/model.js';

const job={id:'stable-public-id',company:'Example Co',title:'Design intern',sourceUrl:'https://example.com/jobs/42',requirements:'Research and prototype.',payMin:null,payVerified:false,status:'interview',notes:'Never share this note',applicationKit:{secret:'Never recursively export kits'}};
const profile={name:'Fictional Candidate',email:'example@example.com',portfolio:'https://example.com',background:'Built a prototype.\nInterviewed five users.',availability:'December, three months',secret:'Never export extra fields'};
const make=()=>createRequest({job,profile,posting:'Full posting: research and prototype. Stipend undisclosed.',requirements:[{id:'req-1',text:'Research',sourceUrl:job.sourceUrl}],confirmed:true});
function response(request){return {format:RESULT_FORMAT,version:1,jobId:request.jobId,requestId:request.requestId,sourceHash:request.sourceHash,documents:{evaluation:'Research: direct evidence F002. Pay remains unknown.',cv:'Built a prototype.',coverLetter:'I interviewed five users.',interview:'Discuss prototype tradeoffs.'},review:{factualAccuracy:true,requirementsCoverage:true,claims:[{document:'cv',quote:'Built a prototype.',factIds:['F001']},{document:'coverLetter',quote:'interviewed five users',factIds:['F002']}],notes:'Checked only fictional source facts.'},status:'applied',notes:'Injected note',companyOverrides:{example:{blacklisted:false}}};}

test('request requires explicit confirmation, real profile and posting',async()=>{
 await assert.rejects(createRequest({job,profile,posting:'JD',confirmed:false}),/Confirm/);
 await assert.rejects(createRequest({job,profile:{},posting:'JD',confirmed:true}),/profile/);
 await assert.rejects(createRequest({job,profile,posting:' ',confirmed:true}),/full job description/);
});
test('handoff preserves IDs, unknown pay and confirmed fact provenance while excluding private board state',async()=>{
 const request=await make();assert.equal(request.jobId,job.id);assert.equal(request.snapshot.job.payMin,null);
 assert.equal(request.snapshot.candidate.facts[1].id,'F002');assert.equal(request.snapshot.candidate.facts[2].claim,'Availability: December, three months');
 const json=JSON.stringify(request);assert.ok(!json.includes('Never'));assert.ok(!json.includes('blacklisted'));
 assert.equal(await sourceHash(request.snapshot),request.sourceHash);assert.ok(requestPrompt(request).includes(request.sourceHash));
 const reordered=Object.fromEntries(Object.entries(request.snapshot).reverse());assert.equal(await sourceHash(reordered),request.sourceHash);
});
test('reviewed result imports documents without importing application status, notes or company state',async()=>{
 const request=await make(),result=await importResult(response(request),request);
 assert.equal(result.documents.cv,'Built a prototype.');assert.equal(result.status,undefined);assert.equal(result.notes,undefined);assert.equal(result.companyOverrides,undefined);
 assert.equal(job.status,'interview');assert.equal(job.notes,'Never share this note');
});
test('wrong role, old request and changed source snapshots cannot replace current drafts',async()=>{
 const request=await make();for(const key of ['jobId','requestId','sourceHash'])await assert.rejects(importResult({...response(request),[key]:'wrong'},request),/different role or an older request/);
 const changed=structuredClone(request);changed.snapshot.posting+=' Changed';await assert.rejects(validateRequest(changed),/hash/);
});
test('unreviewed, placeholder, unknown-fact and nonexistent quotes are rejected',async()=>{
 const request=await make();
 for(const change of [p=>p.review.factualAccuracy=false,p=>p.review.claims=[],p=>p.documents.cv='[[TODO]]',p=>p.review.claims[0].factIds=['F999'],p=>p.review.claims[0].quote='Made up quote',p=>p.review.claims=[null]]){
  const payload=response(request);change(payload);await assert.rejects(importResult(payload,request));
 }
});
test('editing invalidates the review and leaves the submitted source and documents unchanged',async()=>{
 const request=await make(),result=await importResult(response(request),request);const kit={request,result};
 assert.throws(()=>submissionSnapshot(kit,false),/Confirm/);
 const submitted=submissionSnapshot(kit,true);const edited=editDocument(result,'cv','Revised factual wording');
 assert.equal(edited.review,null);assert.equal(submitted.result.documents.cv,'Built a prototype.');
 assert.throws(()=>submissionSnapshot({...kit,submitted},true),/already saved/);
 const newRequest=await make();const olderSnapshot=submissionSnapshot({request:newRequest,result},true);
 assert.equal(olderSnapshot.request.requestId,request.requestId,'Archive must retain the request that actually produced these drafts');
});
test('backups preserve complete workspaces and reject malformed document state atomically',async()=>{
 const request=await make(),result=await importResult(response(request),request);
 const applicationKit={request,result,submitted:submissionSnapshot({request,result},true)};
 const backup={version:1,custom:[],overrides:{[job.id]:{applicationKit,status:'interview',notes:'Keep note'}}};
 assert.deepEqual(validateBackup(JSON.parse(JSON.stringify(backup))),backup);
 for(const broken of [null,{result:{documents:true}},{request:{snapshot:{candidate:{}}}},{submitted:{at:12}}]){
  assert.throws(()=>validateBackup({...backup,overrides:{[job.id]:{applicationKit:broken}}}),/invalid/);
 }
 assert.equal(backup.overrides[job.id].notes,'Keep note');
});
