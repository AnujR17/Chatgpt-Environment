import React, {useRef,useState} from 'react';
import {createRequest,importResult,requestPrompt,requestSnapshot,sourceHash,editDocument,submissionSnapshot,DOCUMENT_LABELS} from './applicationKit';
import {jobFitRecord} from './CompanyDirectory';

function download(name,value,type='application/json') {
  const url=URL.createObjectURL(new Blob([value],{type}));
  const link=document.createElement('a');link.href=url;link.download=name;link.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}

export default function ApplicationWorkspace({job,company,profile,onUpdate,onProfile,onNotify}) {
  const kit=job.applicationKit || {};
  const [posting,setPosting]=useState(kit.posting ?? kit.request?.snapshot.posting ?? job.capturedDescription ?? '');
  const [confirmed,setConfirmed]=useState(false),[sent,setSent]=useState(false);
  const [busy,setBusy]=useState(false),[error,setError]=useState(''),[document,setDocument]=useState('evaluation');
  const input=useRef(null);
  const requirements=jobFitRecord(job,company).requirements || [];
  const result=kit.result;
  const resultIsCurrent=result?.requestId===kit.request?.requestId;

  async function run(action) {
    setError('');setBusy(true);
    try {await action();} catch(err) {setError(err.message || 'Could not complete this action. Your existing drafts were kept.');}
    finally {setBusy(false);}
  }
  async function exportRequest() {
    await run(async()=>{
      const request=await createRequest({job,profile,posting,requirements,confirmed});
      onUpdate({applicationKit:{...kit,request}});
      download(`application-request-${job.id}.json`,JSON.stringify(request,null,2));
      onNotify('Request saved. Attach the JSON in Codex and ask it to prepare the application.');
    });
  }
  async function copyRequest() {
    await run(async()=>{
      if (!kit.request) throw Error('Prepare a request first.');
      await navigator.clipboard.writeText(requestPrompt(kit.request));
      onNotify('Request copied. Paste it in Codex to prepare the application.');
    });
  }
  async function receive(event) {
    const file=event.target.files[0];event.target.value='';if(!file)return;
    await run(async()=>{
      if(file.size>1_000_000)throw Error('Application result is too large.');
      if(!kit.request)throw Error('Prepare a request for this role first.');
      const current=await sourceHash(requestSnapshot(job,profile,posting,requirements));
      if(current!==kit.request.sourceHash)throw Error('The role, profile or posting changed. Prepare a new request before importing.');
      const next=await importResult(JSON.parse(await file.text()),kit.request);
      onUpdate({applicationKit:{...kit,result:next}});
      onNotify('Application documents imported. Review them before sending. Your application stage is unchanged.');
    });
  }
  function edit(value) {
    onUpdate({applicationKit:{...kit,result:editDocument(result,document,value)}});
  }
  function recordSubmission() {
    run(async()=>{
      const submitted=submissionSnapshot(kit,sent);
      onUpdate({applicationKit:{...kit,submitted}});
      setSent(false);onNotify('Submitted copy saved in this browser. Update the application stage separately.');
    });
  }

  return <section className="application-workspace" aria-label="Application workspace">
    <div className="info-panel compact"><div><h3>Prepare this application with Codex</h3><p>Export this role and your confirmed profile, attach the request in Codex, then import the returned documents here. Nothing is sent to a model or employer by this page.</p></div></div>
    {error&&<p className="error-banner" role="alert">{error}</p>}
    <p>Your saved profile: <strong>{profile.name || 'Name missing'}</strong>. {profile.background ? 'Experience is available.' : 'Add your confirmed experience before exporting.'} <button className="text-button" onClick={onProfile}>Edit profile</button></p>
    <label className="field"><span>Full job description</span><textarea aria-label="Full job description" rows={7} maxLength={80000} value={posting} onChange={e=>{setPosting(e.target.value);setConfirmed(false);onUpdate({applicationKit:{...kit,posting:e.target.value}});}} placeholder="Paste the complete description from the job page. The board summary alone may omit requirements."/></label>
    <label className="check-field"><input type="checkbox" checked={confirmed} onChange={e=>setConfirmed(e.target.checked)}/>I reviewed this posting and confirm that the saved profile facts are accurate.</label>
    <div className="workspace-actions"><button className="button primary" disabled={busy||!confirmed} onClick={exportRequest}>Download Codex request</button><button className="button secondary" disabled={busy||!kit.request} onClick={copyRequest}>Copy request for Codex</button><button className="button secondary" disabled={busy||!kit.request} onClick={()=>input.current.click()}>Import application result</button></div>
    <input hidden type="file" accept=".json,application/json" ref={input} onChange={receive}/>
    <p className="muted">The request includes this role, the pasted posting, and your profile facts and contact links. It excludes private notes, other applications, blacklists and assessments. Share it only in the chat you choose. {kit.request&&`Last request: ${new Date(kit.request.createdAt).toLocaleString('en-IN')}.`}</p>
    {result&&<>
      <h3>Your application documents</h3>
      <p role="status">{!resultIsCurrent?'These drafts belong to an earlier request.':result.review?'Factual review recorded. Check the drafts before sending.':'Edited since review. Ask Codex to review the revised text before sending.'} References are checked on import; this does not prove every claim is true.</p>
      <div className="workspace-actions" aria-label="Application documents">{Object.entries(DOCUMENT_LABELS).map(([key,label])=><button key={key} className={`button ${document===key?'primary':'secondary'}`} aria-pressed={document===key} onClick={()=>setDocument(key)}>{label}</button>)}</div>
      <label className="field"><span>{DOCUMENT_LABELS[document]}</span><textarea className="application-document" aria-label={DOCUMENT_LABELS[document]} rows={15} value={result.documents[document]} maxLength={80000} onChange={e=>edit(e.target.value)}/></label>
      <div className="workspace-actions"><button className="button secondary" onClick={()=>download(`${job.id}-${document}.md`,result.documents[document],'text/markdown')}>Download this document</button><button className="button secondary" onClick={()=>download(`application-kit-${job.id}.json`,JSON.stringify({request:result.sourceRequest,result},null,2))}>Download application kit</button></div>
      {result.review?.notes&&<p className="readable">Review notes: {result.review.notes}</p>}
      <p className="muted">Documents are editable Markdown. PDF layout and ATS text extraction have not been checked. Draft edits save in this browser and remove the previous review.</p>
      {!kit.submitted?<div className="submission-copy"><h3>Preserve what you sent</h3><label className="check-field"><input type="checkbox" checked={sent} onChange={e=>setSent(e.target.checked)}/>These are the exact documents I submitted.</label><button className="button secondary" disabled={!sent||busy} onClick={recordSubmission}>Save submitted copy</button><p className="muted">This saves a separate copy. It does not send anything or change your application stage.</p></div>:<div className="submission-copy"><h3>Submitted copy saved</h3><p>{new Date(kit.submitted.at).toLocaleString('en-IN')}. Later draft edits leave this copy unchanged.</p><button className="button secondary" onClick={()=>download(`submitted-application-${job.id}.json`,JSON.stringify(kit.submitted,null,2))}>Download submitted copy</button></div>}
    </>}
    <p className="muted">This workspace is included in Export → Back up saved progress. Keep a backup before switching browsers or clearing browser storage.</p>
  </section>;
}
