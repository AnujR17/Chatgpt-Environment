import React from 'react';
import {safeUrl,dateLabel,localDate} from './model';
import {establishedEmployer,screeningStatus,personalLalaFlag,SCREEN_LABELS,LALA_DEFINITION_URL} from './employerScreening';

function Sources({items=[]}) {
  return <div className="employer-evidence-links">{items.map((item,i)=>{
    const url=safeUrl(typeof item==='string'?item:item.url);
    return url?<a key={i} href={url} target="_blank" rel="noopener noreferrer">{item.label||'Source'}{item.access==='indexed'?' (indexed evidence)':''}</a>:null;
  })}</div>;
}
export function EmployerBadges({company}) {
  const status=screeningStatus(company);
  return <div className="employer-badges">
    {establishedEmployer(company)&&<span className="pill employer-established">Established employer</span>}
    <span className={`pill employer-screen-${status}`}>{SCREEN_LABELS[status]}</span>
    {personalLalaFlag(company)!=='unknown'&&<span className="pill">Your private Lala flag: {personalLalaFlag(company)==='yes'?'Yes':'No'}</span>}
  </div>;
}
export function ScreeningExplanation() {
  return <details className="employer-screen-explanation"><summary>What does the Lala-style flag mean?</summary>
    <p>Informal workplace slang for owner-controlled, arbitrary management: weak HR rules, favouritism, unclear pay or roles, and poor accountability. Size, family ownership, low pay or an unknown brand alone do not establish that culture.</p>
    <p><strong>Processes documented</strong> means published procedures were found. <strong>Check terms</strong> means the cited hiring terms contain a specific issue. Neither is a Yes/No culture verdict. <strong>Unassessed</strong> means there is not enough reviewed evidence. A recognised brand can still have a poor team or manager.</p>
    <a href={LALA_DEFINITION_URL} target="_blank" rel="noopener noreferrer">Business Standard: meaning and context, 18 August 2022</a>
  </details>;
}
export default function EmployerScreening({company,onUpdate}) {
  const review=company?.workplaceReview,profile=company?.employerProfile;
  function update(changes) {onUpdate(company.id,{...(company.id.startsWith('fit-')?{name:company.name}:{}),lalaAssessment:{...company.lalaAssessment,...changes,checkedAt:localDate()}});}
  return <section className="employer-screening" aria-label={`Employer checks for ${company.name||company.company}`}>
    <h4>Employer reputation & workplace checks</h4><EmployerBadges company={company}/>
    {profile&&<><p>{profile.basis}</p><Sources items={profile.sources}/><p className="muted">{profile.limits} Checked {dateLabel(profile.checkedAt)}.</p></>}
    <p>{review?.summary||'No workplace assessment has been researched for this company. Missing information does not make it a Lala company.'}</p>
    {review?.signals?.length>0&&<ul>{review.signals.map(signal=><li key={signal.id}>{signal.text}</li>)}</ul>}
    <Sources items={review?.sources}/>
    {review&&<p className="muted">{review.limits} Checked {dateLabel(review.checkedAt)}. Confidence: {review.confidence}.</p>}
    <p><strong>Before accepting:</strong> {review?.nextAction||'Confirm the legal employer, written fixed pay, hours, leave, reporting manager, design mentorship and whether any fee or bond applies. Ask recent team members about actual practice.'}</p>
    {onUpdate&&<div className="private-lala-assessment">
      <label className="field"><span>Your Lala-style assessment (private)</span><select aria-label={`Your Lala assessment for ${company.name||company.company}`} value={personalLalaFlag(company)} onChange={e=>update({value:e.target.value})}><option value="unknown">Unknown / not assessed</option><option value="yes">Yes, in my assessment</option><option value="no">No, in my assessment</option></select></label>
      <label className="field"><span>Your reasons or evidence (private)</span><textarea aria-label={`Private workplace notes for ${company.name||company.company}`} value={company.lalaAssessment?.note||''} onChange={e=>update({note:e.target.value})} maxLength={20000} rows={2}/></label>
      <p className="muted">Your assessment stays in this browser and your JSON backup. It does not alter public research, blacklist a company or change application stages.</p>
    </div>}
  </section>;
}
