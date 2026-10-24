import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const companies=JSON.parse(fs.readFileSync(new URL('../public/data/companies.json',import.meta.url))).companies;
const jobs=JSON.parse(fs.readFileSync(new URL('../public/data/jobs.json',import.meta.url))).jobs;
test('company records keep sources, inferred families and personal assessment separate',()=>{
 assert.equal(new Set(companies.map(c=>c.id)).size,companies.length);
 for(const c of companies){
  assert.ok(c.careersUrl||c.contact?.url,c.name);assert.ok(['Dream','Workable','Possible'].includes(c.tier));
  assert.ok(c.sources?.length,c.name);assert.ok(Array.isArray(c.likelyRoles));assert.equal(c.blacklisted,undefined,'Private blacklist must not be seeded publicly');assert.equal(c.assessments,undefined,'Private evidence must not be committed');
  for(const role of c.roles||[]){assert.ok(role.id&&role.url&&role.evidenceStatus);for(const req of role.requirements){assert.ok(req.id&&req.text&&req.sourceUrl);}}
 }
 const project=companies.find(c=>c.id==='project44');assert.equal(project.contact.kind,'Hiring accommodations only');
});
test('new employer roles preserve unknown pay and honest role types',()=>{
 assert.equal(new Set(jobs.map(j=>j.id)).size,jobs.length);
 const newJobs=jobs.filter(j=>j.companyId);assert.equal(newJobs.length,8);
 for(const j of newJobs){assert.equal(j.payMin,null);assert.equal(j.payMax,null);assert.equal(j.payVerified,false);assert.equal(j.status,'on_hold');assert.equal(j.postedAt,null);assert.ok(j.requirementItems.length);}
 assert.equal(newJobs.find(j=>j.companyId==='gravity').workMode,'Remote');assert.equal(newJobs.find(j=>j.companyId==='frappe').roleType,'Junior / fresher');
});
