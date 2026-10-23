import test from 'node:test';
import assert from 'node:assert/strict';
import { payMatch, mergeJobs, isDue, toCsv, safeUrl, canonicalUrl, validateBackup } from '../src/model.js';
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
