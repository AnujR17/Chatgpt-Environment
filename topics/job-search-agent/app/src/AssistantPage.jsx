import React, {useMemo,useState} from 'react';
import {ArrowUpRight,FileText,Search,UserRound} from 'lucide-react';
import ApplicationWorkspace from './ApplicationWorkspace';
import {companyMatches,isPipeline,safeUrl,STAGES} from './model';

export default function AssistantPage({jobs,companies,profile,selectedId,onSelect,onUpdate,onProfile,onReview,onNotify,loading}) {
  const [query,setQuery]=useState(''),[savedOnly,setSavedOnly]=useState(false);
  const job=jobs.find(role=>role.id===selectedId);
  const company=job?companies.find(value=>companyMatches(value,job.company)):null;
  const roles=useMemo(()=>jobs.filter(role=>{
    const eligible=role.status!=='closed'||isPipeline(role)||role.applicationKit;
    return eligible&&(!savedOnly||isPipeline(role)||role.applicationKit)&&
      `${role.company} ${role.title}`.toLowerCase().includes(query.trim().toLowerCase());
  }).sort((a,b)=>Number(!!b.applicationKit)-Number(!!a.applicationKit)||Number(isPipeline(b))-Number(isPipeline(a))||a.company.localeCompare(b.company)),[jobs,query,savedOnly]);
  const source=safeUrl(job?.sourceUrl);

  return <section className="assistant-page" aria-label="Application assistant">
    <div className="assistant-intro">
      <div><span className="assistant-eyebrow">YOUR APPLICATION WORKSPACE</span><h2>Turn a role into a prepared application</h2><p>Evaluate the requirements, tailor your documents and prepare for the interview. Your existing profile and saved applications stay connected here.</p></div>
      <button className="button secondary" onClick={onProfile}><UserRound size={16}/>{profile.name?'Review your profile':'Set up your profile'}</button>
    </div>
    <div className="assistant-layout">
      <aside className="assistant-role-panel" aria-label="Choose an assistant role">
        <h3>Choose a role</h3>
        <label className="search-field"><Search size={17}/><input aria-label="Search assistant roles" value={query} onChange={event=>setQuery(event.target.value)} placeholder="Company or role"/></label>
        <label className="check-field"><input type="checkbox" checked={savedOnly} onChange={event=>setSavedOnly(event.target.checked)}/>Saved applications only</label>
        <p className="muted">{roles.length} {roles.length===1?'role':'roles'}{loading?' · Updating…':''}</p>
        <div className="assistant-role-list" aria-label="Assistant roles">
          {roles.map(role=><button key={role.id} className={`assistant-role ${role.id===selectedId?'selected':''}`} aria-pressed={role.id===selectedId} onClick={()=>onSelect(role.id)}><strong>{role.company}</strong><span>{role.title}</span><small>{role.applicationKit?.result?'Documents saved':role.applicationKit?.request?'Request prepared':STAGES.find(stage=>stage.id===role.status)?.label||'To review'}</small></button>)}
          {!roles.length&&<p className="assistant-list-empty">{loading?'Loading your roles…':'No matching roles. Try another company or clear the saved-only filter.'}</p>}
        </div>
      </aside>
      <div className="assistant-main">
        {job?<>
          <div className="assistant-role-heading"><div><p>{job.company}</p><h2>{job.title}</h2><span>{job.location||'Location to confirm'}</span></div><div className="workspace-actions"><button className="button secondary" onClick={()=>onReview(job.id)}>View role details</button>{source&&<a className="button secondary" href={source} target="_blank" rel="noopener noreferrer">Original posting<ArrowUpRight size={15}/></a>}</div></div>
          <ApplicationWorkspace key={job.id} job={job} company={company} profile={profile} onUpdate={changes=>onUpdate(job.id,changes)} onProfile={onProfile} onNotify={onNotify}/>
        </>:<div className="assistant-start"><FileText size={30}/><h2>{selectedId?'This role is unavailable':'Start with a role'}</h2><p>{selectedId?'Choose another role from your list. Saved application records remain in the job board.':'Choose a role on the left to open its dedicated application workspace.'}</p><ol><li>Review the full posting and your profile facts.</li><li>Generate a tailored application with a separate factual review.</li><li>Review and download the documents, then keep the version you send.</li></ol><p className="muted">AI generation runs directly on this site. The selected posting and confirmed profile are sent to the model only when you choose Generate.</p></div>}
      </div>
    </div>
  </section>;
}
