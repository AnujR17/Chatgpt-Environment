import test from 'node:test';
import assert from 'node:assert/strict';
import { payMatch, mergeJobs, isDue, toCsv, safeUrl, canonicalUrl, validateBackup, benchmarkText, mergeCompanies, isCompanyBlocked, fitSummary, mergeCompanyPreferences,platformName,platforms,stipend,compensationText } from '../src/model.js';
test('stipend thresholds use the lower bound and original evidence',()=>{
 assert.equal(payMatch({region:'Gujarat',payMin:20000,payVerified:true}),'meets');
 assert.equal(payMatch({region:'India',payMin:30000,payVerified:true}),'meets');
 assert.equal(payMatch({region:'India',payMin:25000,payMax:40000,payVerified:true}),'consider');
 assert.equal(payMatch({region:'India',payMin:1000,payMax:30000,payVerified:true}),'below');
 assert.equal(payMatch({region:'India',payMin:40000,payVerified:false}),'unconfirmed');
 assert.equal(payMatch({region:'India',payMin:null}),'unconfirmed');
});
test('updated feed preserves personal progress and newly added roles',()=>{
 const result=mergeJobs([{id:'a',company:'A',title:'Intern',payMin:30000},{id:'b',company:'B',title:'UX Intern'}],[{id:'c',company:'C',title:'Product Intern'}],{a:{status:'interview',notes:'Call tomorrow'},b:{status:'invalid'}});
 assert.equal(result.length,3);assert.equal(result.find(j=>j.id==='a').status,'interview');
 assert.equal(result.find(j=>j.id==='a').payMin,30000);assert.equal(result.find(j=>j.id==='b').status,'discovered');
});
test('due actions exclude closed and offer roles',()=>{
 assert.equal(isDue({dueDate:'2026-10-22',status:'applied'},'2026-10-23'),true);
 assert.equal(isDue({dueDate:'2026-10-23',status:'assessment'},'2026-10-23'),true);
 assert.equal(isDue({dueDate:'2026-10-24',status:'assessment'},'2026-10-23'),false);
 assert.equal(isDue({dueDate:'2026-10-22',status:'closed'},'2026-10-23'),false);
});
test('CSV escapes formulas, quotes and multiline notes',()=>{
 const csv=toCsv([{company:'=HYPERLINK("bad")',notes:'First line\n"quoted"'}]);
 assert.ok(csv.includes('"\'=HYPERLINK(""bad"")"'));assert.ok(csv.includes('First line\n""quoted""'));
});
test('unsafe URL schemes rejected and tracking URLs deduplicate',()=>{
 assert.equal(safeUrl('javascript:alert(1)'), '');assert.equal(safeUrl('data:text/html,bad'), '');
 assert.equal(safeUrl('https://example.com/jobs'), 'https://example.com/jobs');
 assert.equal(canonicalUrl('https://example.com/jobs/?utm_source=feed#apply'),'https://example.com/jobs');
});
test('backup validation rejects malformed imports',()=>{
 assert.throws(()=>validateBackup({version:1,custom:[],overrides:[]}));
 assert.throws(()=>validateBackup({version:1,custom:[{id:'a'}],overrides:{}}));
 assert.equal(validateBackup({version:1,custom:[],overrides:{}}).version,1);
});
test('company reports never become confirmed listing pay and annual units stay annual',()=>{
 const benchmark={min:300000,max:300000,period:'year',sourceUrl:'https://example.com/report'};
 assert.equal(payMatch({payMin:null,payVerified:false,payBenchmark:benchmark}),'estimated');
 assert.equal(benchmarkText(benchmark),'₹3,00,000/year reported');
 assert.equal(payMatch({payMin:40000,payVerified:false}),'unconfirmed');
});
test('on-hold feed updates preserve an existing application and its notes',()=>{
 const feed=[{id:'same-role',company:'Employer',title:'UX Intern',status:'on_hold'}];
 assert.equal(mergeJobs(feed,[],{})[0].status,'on_hold');
 const merged=mergeJobs(feed,[],{'same-role':{status:'applied',notes:'Already submitted'}})[0];
 assert.equal(merged.status,'applied');assert.equal(merged.notes,'Already submitted');
});

test('blacklist survives feed refresh, matches aliases, and keeps application history',()=>{
 const overrides={a:{blacklisted:true},custom:{name:'Other Studio',blacklisted:true}};
 const companies=mergeCompanies([{id:'a',name:'Product Co',aliases:['ProductCo India']}],overrides);
 assert.equal(companies.length,2);
 assert.equal(isCompanyBlocked({company:'ProductCo India'},companies),true);
 assert.equal(isCompanyBlocked({company:'Other Studio'},companies),true);
 assert.equal(isCompanyBlocked({company:'Other'},companies),false);
 const job=mergeJobs([{id:'j',company:'Product Co',title:'UX Intern'}],[],{j:{status:'applied',notes:'Preserve'}})[0];
 assert.equal(job.status,'applied');assert.equal(job.notes,'Preserve');
 assert.equal(isCompanyBlocked(job,mergeCompanies([{id:'a',name:'Product Co'}],{a:{blacklisted:false}})),false);
});
test('fit counts unknowns separately and cannot manufacture a match',()=>{
 const reqs=[{id:'portfolio'},{id:'figma'},{id:'degree'},{id:'duration'}];
 assert.deepEqual(fitSummary(reqs),{total:4,met:0,partial:0,gap:0,unknown:4,percent:0,assessed:0});
 const result=fitSummary(reqs,{portfolio:{state:'met',evidence:'Case study'},figma:{state:'partial'},degree:{state:'gap'},duration:{state:'invalid'}});
 assert.equal(result.met,1);assert.equal(result.percent,25);assert.equal(result.unknown,1);assert.equal(result.partial,1);assert.equal(result.gap,1);
 assert.equal(fitSummary([]).percent,null);
});

test('importing reviewed criteria preserves blacklist, category and other role evidence',()=>{
 const old={a:{blacklisted:true,blacklistReason:'Private',tier:'Dream',following:true,assessments:{r:{one:{state:'met',evidence:'Existing'},two:{state:'unknown'}},other:{criterion:{state:'gap'}}}}};
 const result=mergeCompanyPreferences(old,{a:{assessments:{r:{two:{state:'partial',evidence:'Reviewed portfolio'}}}}});
 assert.equal(result.a.blacklisted,true);assert.equal(result.a.blacklistReason,'Private');assert.equal(result.a.tier,'Dream');assert.equal(result.a.following,true);
 assert.equal(result.a.assessments.r.one.evidence,'Existing');assert.equal(result.a.assessments.r.two.state,'partial');assert.equal(result.a.assessments.other.criterion.state,'gap');assert.equal(old.a.assessments.r.two.state,'unknown');
});

test('source families distinguish startup boards, HN and remote cross-posts',()=>{
 assert.equal(platformName('https://news.ycombinator.com/item?id=49922569'),'Hacker News');
 assert.equal(platformName('https://www.ycombinator.com/companies/example/jobs/123'),'YC / Work at a Startup');
 assert.equal(platformName('Work at a Startup'),'YC / Work at a Startup');
 assert.equal(platformName('Himalayas'),'Remote boards');assert.equal(platformName('Wellfound'),'Wellfound');
 assert.deepEqual(platforms({sourceType:'Company careers',additionalSources:[{platform:'Wellfound'},{platform:'Wellfound'},{platform:'Remote OK'}]}),['Company careers','Wellfound','Remote boards']);
});
test('annual and foreign compensation are displayed without implying a monthly stipend match',()=>{
 const salary={min:8000,max:12000,currency:'USD',period:'year',verified:true};
 assert.equal(compensationText(salary),'USD 8,000–USD 12,000/year');
 assert.equal(stipend({payMin:null,advertisedCompensation:salary}),'USD 8,000–USD 12,000/year');
 assert.equal(payMatch({payMin:null,advertisedCompensation:salary}),'annual');
 assert.equal(compensationText({min:400000,max:600000,currency:'INR',period:'year'}),'₹4,00,000–₹6,00,000/year');
 assert.equal(payMatch({payMin:null,advertisedCompensation:{...salary,verified:false}}),'unconfirmed');
});
