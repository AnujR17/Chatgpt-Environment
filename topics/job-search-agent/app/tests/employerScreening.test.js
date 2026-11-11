import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {establishedEmployer,screeningStatus,personalLalaFlag,matchesEmployerScreen} from '../src/employerScreening.js';
import {mergeCompanies,mergeCompanyPreferences,validateBackup} from '../src/model.js';

test('visibility, evidence and a private opinion cannot manufacture one another',()=>{
 const established={id:'brand',name:'Brand',employerProfile:{status:'established',sources:[{url:'https://example.com/careers'}]}};
 assert.equal(establishedEmployer(established),true);
 assert.equal(screeningStatus(established),'unassessed');assert.equal(personalLalaFlag(established),'unknown');
 assert.equal(establishedEmployer({employerProfile:{status:'established'}}),false);
 assert.equal(screeningStatus({workplaceReview:{status:'processes-documented',sources:[]}}),'unassessed');
 assert.equal(screeningStatus({workplaceReview:{status:'safe',sources:[{}]}}),'unassessed');
 assert.equal(screeningStatus({...established,lalaAssessment:{value:'no'}}),'unassessed');
 assert.equal(matchesEmployerScreen({...established,lalaAssessment:{value:'no'}},'my-no'),true);
 assert.equal(matchesEmployerScreen(undefined,'terms-concerns'),false);
});
test('feed refresh and partial backup imports retain private reasons, blacklist and criteria',()=>{
 const previous={brand:{blacklisted:true,blacklistReason:'Synthetic preference',lalaAssessment:{value:'yes',note:'Synthetic interview evidence'},assessments:{role:{one:{state:'met'}}}}};
 const merged=mergeCompanyPreferences(previous,{brand:{assessments:{role:{two:{state:'partial'}}}}});
 const company=mergeCompanies([{id:'brand',name:'Brand',workplaceReview:{status:'processes-documented',sources:[{url:'https://example.com'}]}}],merged)[0];
 assert.equal(personalLalaFlag(company),'yes');assert.equal(company.lalaAssessment.note,'Synthetic interview evidence');assert.equal(company.blacklisted,true);
 const partial=mergeCompanyPreferences(merged,{brand:{lalaAssessment:{value:'no'}}});assert.equal(partial.brand.lalaAssessment.note,'Synthetic interview evidence');assert.equal(partial.brand.assessments.role.one.state,'met');assert.equal(previous.brand.lalaAssessment.value,'yes');
 assert.equal(validateBackup({version:1,custom:[],overrides:{},companyOverrides:partial}).companyOverrides.brand.lalaAssessment.value,'no');
});
test('malformed imported workplace opinions are rejected before rendering',()=>{
 for(const lalaAssessment of [null,[],{value:'safe'},{note:{}},{note:'a'.repeat(20001)},{checkedAt:12}]) assert.throws(()=>validateBackup({version:1,custom:[],overrides:{},companyOverrides:{x:{lalaAssessment}}}),/workplace assessment/);
});
test('published employer screens carry sources and limits without private flags or invented vacancies',()=>{
 const companies=JSON.parse(fs.readFileSync(new URL('../public/data/companies.json',import.meta.url))).companies;
 const jobs=JSON.parse(fs.readFileSync(new URL('../public/data/jobs.json',import.meta.url))).jobs;
 for(const c of companies){
  assert.equal(c.lalaAssessment,undefined,'Personal company opinions must never enter public research');
  if(c.workplaceReview){assert.ok(c.workplaceReview.sources.length&&c.workplaceReview.checkedAt&&c.workplaceReview.limits&&c.workplaceReview.confidence);assert.ok(['unassessed','processes-documented','terms-concerns'].includes(c.workplaceReview.status));}
 }
 for(const id of ['intuit','sap','servicenow']){
  const c=companies.find(c=>c.id===id);assert.equal(establishedEmployer(c),true);assert.equal(c.currentOpeningVerified,false);assert.equal(jobs.some(j=>j.companyId===id),false);
 }
});
