import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ArrowDownToLine, ArrowUpFromLine, ArrowUpRight, CalendarDays, Check, ChevronDown, ChevronRight, ClipboardList, ExternalLink, FileText, Filter, GripVertical, LayoutGrid, List, Mail, Plus, RefreshCw, Search, Settings2, ShieldCheck, SlidersHorizontal, X } from 'lucide-react';
import '@fontsource/dm-sans/400.css';
import '@fontsource/dm-sans/500.css';
import '@fontsource/dm-sans/600.css';
import '@fontsource/dm-sans/700.css';
import { STAGES, KEYS, money, stipend, payMatch, safeUrl, canonicalUrl, mergeJobs, dateLabel, localDate, isDue, toCsv, validateBackup } from './model';
import './styles.css';

const PAY_LABELS = { meets: 'Meets stipend', consider: 'Conditional pay', unconfirmed: 'Confirm stipend', below: 'Below minimum' };
const blankProfile = { name: '', email: '', portfolio: '', resume: '', availability: '', background: '' };
function read(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } }
function download(name, contents, type = 'application/json') {
  const url = URL.createObjectURL(new Blob([contents], { type }));
  const a = document.createElement('a'); a.href = url; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function Link({ href, children, className = '' }) { const url = safeUrl(href); return url ? <a href={url} target="_blank" rel="noopener noreferrer" className={className}>{children}</a> : null; }
function App() {
  const [feed, setFeed] = useState([]), [meta, setMeta] = useState(null), [sources, setSources] = useState([]);
  const [overrides, setOverrides] = useState(() => read(KEYS.overrides, {}));
  const [custom, setCustom] = useState(() => read(KEYS.custom, []));
  const [profile, setProfile] = useState(() => ({ ...blankProfile, ...read(KEYS.profile, {}) }));
  const [page, setPage] = useState('opportunities'), [view, setView] = useState('board');
  const [search, setSearch] = useState(''), [mode, setMode] = useState('all'), [pay, setPay] = useState('all'), [source, setSource] = useState('all');
  const [selected, setSelected] = useState(null), [modal, setModal] = useState(null), [exportOpen, setExportOpen] = useState(false);
  const [loading, setLoading] = useState(true), [error, setError] = useState(''), [toast, setToast] = useState(''), [dragging, setDragging] = useState(''), [dragOver, setDragOver] = useState('');
  const importRef = useRef(null);
  function announce(message) { setToast(message); }
  useEffect(() => { if (!toast) return; const id = setTimeout(() => setToast(''), 5000); return () => clearTimeout(id); }, [toast]);
  useEffect(() => {
    try { localStorage.setItem(KEYS.overrides, JSON.stringify(overrides)); localStorage.setItem(KEYS.custom, JSON.stringify(custom)); localStorage.setItem(KEYS.profile, JSON.stringify(profile)); }
    catch { setError('Your browser could not save changes. Export a JSON backup before leaving this page.'); }
  }, [overrides, custom, profile]);
  async function refresh() {
    setLoading(true); setError('');
    try {
      const response = await fetch(`/data/jobs.json?t=${Date.now()}`, {cache:'no-store'});
      if (!response.ok) throw new Error('Listings could not be loaded. Your saved changes are safe.');
      const data = await response.json();
      if (!Array.isArray(data.jobs)) throw new Error('The listing feed is invalid. Please try again later.');
      setFeed(data.jobs); setMeta(data.meta);
      const [res, queue] = await Promise.all([
        fetch('/data/sources.json', {cache:'no-store'}),
        fetch('/data/review-queue.json', {cache:'no-store'})
      ]);
      if (res.ok) { const s = await res.json(); setSources(s.sources || []); }
      if (queue.ok) { const q = await queue.json(); if (Array.isArray(q.candidates)) setFeed([...data.jobs, ...q.candidates]); }
    } catch (err) { setError(err.message); } finally { setLoading(false); }
  }
  useEffect(() => { refresh(); }, []);
  const jobs = useMemo(() => mergeJobs(feed, custom, overrides), [feed, custom, overrides]);
  const active = jobs.filter(j => j.status !== 'closed');
  const due = active.filter(j => isDue(j)).sort((a,b) => a.dueDate.localeCompare(b.dueDate));
  const interviews = active.filter(j => j.status === 'interview');
  const selectedJob = jobs.find(j => j.id === selected);
  const visible = useMemo(() => jobs.filter(j => {
    const q = search.toLowerCase().trim();
    return (!q || `${j.company} ${j.title} ${j.location} ${(j.tags || []).join(' ')}`.toLowerCase().includes(q)) &&
      (mode === 'all' || (mode === 'remote' ? j.workMode === 'Remote' : j.workMode !== 'Remote')) &&
      (pay === 'all' || payMatch(j) === pay) && (source === 'all' || j.sourceType === source);
  }).sort((a,b) => {
    const scores = {meets:0, consider:1, unconfirmed:2, below:3};
    return scores[payMatch(a)] - scores[payMatch(b)] || (a.workMode === 'Remote' ? 0 : 1) - (b.workMode === 'Remote' ? 0 : 1) || a.company.localeCompare(b.company);
  }), [jobs, search, mode, pay, source]);
  function update(id, changes) {
    setOverrides(previous => {
      const current = jobs.find(j => j.id === id);
      const event = changes.status && changes.status !== current?.status ? { at:new Date().toISOString(), label:`Moved to ${STAGES.find(s => s.id === changes.status)?.label || changes.status}` } : null;
      return {...previous, [id]: {...previous[id], ...changes,
        ...(changes.status === 'applied' && !current?.appliedAt ? {appliedAt: localDate()} : {}),
        ...(event ? {events: [...(current?.events || []), event]} : {})
      }};
    });
  }
  function move(id, status) { update(id, {status}); announce(`Moved to ${STAGES.find(s => s.id === status)?.label}.`); }
  function backup() { download(`design-internships-backup-${localDate()}.json`, JSON.stringify({version:1, exportedAt:new Date().toISOString(), custom, overrides, profile},null,2)); setExportOpen(false); }
  async function restore(event) {
    const file = event.target.files[0]; event.target.value = ''; if (!file) return;
    try {
      if (file.size > 5_000_000) throw new Error('Backup is too large.');
      const data = validateBackup(JSON.parse(await file.text()));
      setCustom(previous => [...new Map([...previous, ...data.custom].map(j => [j.id,j])).values()]);
      setOverrides(previous => ({...previous,...data.overrides}));
      if (data.profile && typeof data.profile === 'object') setProfile({...blankProfile, ...Object.fromEntries(Object.keys(blankProfile).map(k=>[k, typeof data.profile[k] === 'string' ? data.profile[k] : '']))});
      announce('Backup restored.');
    } catch (err) { announce(err.message || 'Could not read this backup.'); }
  }
  function addJob(job) {
    if (jobs.some(j => job.sourceUrl && canonicalUrl(j.sourceUrl) === canonicalUrl(job.sourceUrl))) throw new Error('This source is already on your board.');
    const newJob = { ...job, id:`custom-${crypto.randomUUID()}`, firstSeen:localDate(), checkedAt:null, evidence:'Added manually. Listing details have not been independently verified.', sourceType:'Manual', status:'discovered', tags:[] };
    setCustom(previous => [...previous,newJob]); setModal(null); setSelected(newJob.id); announce('Opportunity added.');
  }
  return <div className="app-shell">
    <aside className="sidebar">
      <a className="brand" href="#" onClick={e=>{e.preventDefault();setPage('opportunities');}}><span className="brand-mark"><LayoutGrid size={19}/></span><span>Design search<span className="brand-sub">ANUJ'S WORKSPACE</span></span></a>
      <div className="side-section-label">WORKSPACE</div>
      <nav aria-label="Main navigation">
        <button className={page==='opportunities'?'nav-item active':'nav-item'} onClick={()=>setPage('opportunities')}><LayoutGrid size={18}/>Opportunities<span className="nav-count">{active.length}</span></button>
        <button className={page==='followups'?'nav-item active':'nav-item'} onClick={()=>setPage('followups')}><CalendarDays size={18}/>Next actions{due.length>0 && <span className="nav-count accent">{due.length}</span>}</button>
        <button className={page==='sources'?'nav-item active':'nav-item'} onClick={()=>setPage('sources')}><ShieldCheck size={18}/>Sources</button>
        <button className={page==='profile'?'nav-item active':'nav-item'} onClick={()=>setPage('profile')}><FileText size={18}/>Application profile</button>
      </nav>
      <div className="side-preferences"><div className="side-section-label">YOUR SEARCH</div><p>UX, interaction & product design</p><span>Internships · India</span><div className="side-rule"><span>01</span> Remote first</div><div className="side-rule"><span>02</span> Gujarat ₹20k+</div><div className="side-rule"><span>03</span> Elsewhere ₹30k+</div><small>₹25k roles considered individually.</small></div>
      <div className="sidebar-bottom"><div className="avatar">AR</div><div><strong>Anuj</strong><span>Personal workspace</span></div><button className="icon-button" aria-label="Open application profile" onClick={()=>setPage('profile')}><Settings2 size={18}/></button></div>
    </aside>
    <main className="main">
      <header className="topbar"><div className="breadcrumb">Workspace<ChevronRight size={14}/><strong>{({opportunities:'Opportunities',followups:'Next actions',sources:'Sources',profile:'Application profile'})[page]}</strong></div><span className="local-label"><ShieldCheck size={14}/>Saved in this browser</span></header>
      <div className="page-content">
        <section className="page-heading"><div><div className="eyebrow">YOUR NEXT OPPORTUNITY</div><h1>{({opportunities:'Design internships',followups:'Next actions',sources:'Search sources',profile:'Application profile'})[page]}</h1><p>{({opportunities:'Good opportunities. Clear next steps. Your search, in one place.',followups:'Keep applications moving, one task at a time.',sources:'See where listings came from and what still needs checking.',profile:'Keep the facts and links you want to use in applications.'})[page]}</p></div>
          <div className="heading-actions"><div className="export-wrap"><button className="button secondary" onClick={()=>setExportOpen(v=>!v)} aria-expanded={exportOpen}><ArrowDownToLine size={16}/>Export<ChevronDown size={14}/></button>{exportOpen && <div className="menu"><button onClick={()=>{download(`design-internships-${localDate()}.csv`,toCsv(jobs),'text/csv;charset=utf-8');setExportOpen(false);}}>Excel-compatible CSV (current board)</button><a href="/data/internships.xlsx" download onClick={()=>setExportOpen(false)}>Excel workbook (researched listings)</a><button onClick={backup}>JSON backup (includes your updates)</button><button onClick={()=>{importRef.current.click();setExportOpen(false);}}>Restore JSON backup</button></div>}</div><button className="button primary" onClick={()=>setModal('add')}><Plus size={17}/>Add opportunity</button></div>
        </section>
        <input type="file" accept=".json,application/json" ref={importRef} onChange={restore} hidden/>
        {error && <div className="error-banner" role="alert">{error}<button onClick={refresh}>Try again</button></div>}
        {page==='opportunities' && <>
          <div className="stats-grid"><Stat label="Opportunities" value={active.length} detail="In your search"/><Stat label="Meet stipend" value={active.filter(j=>payMatch(j)==='meets').length} detail="Pay stated in original listing" highlight/><Stat label="Applied" value={jobs.filter(j=>!!j.appliedAt || ['applied','assessment','interview','offer'].includes(j.status)).length} detail="Recorded by you"/><Stat label="Interviews" value={interviews.length} detail={interviews.length?'Keep dates up to date':'Your next conversation starts here'}/></div>
          <div className="search-context"><div><strong>Remote first, then closer to home.</strong><span>Gujarat, Maharashtra, Goa and southern India. Unknown stipends stay visible for review.</span></div><button onClick={()=>{setMode('remote');setPay('meets');}}>View remote stipend matches<ChevronRight size={16}/></button></div>
          <div className="board-toolbar"><div className="view-switch" aria-label="View"><button className={view==='board'?'selected':''} onClick={()=>setView('board')}><LayoutGrid size={16}/>Board</button><button className={view==='list'?'selected':''} onClick={()=>setView('list')}><List size={16}/>List</button></div><div className="toolbar-right"><span className="checked-label">Researched {dateLabel(meta?.researchedAt)}</span><button className="icon-button" aria-label="Reload published listing feed" onClick={refresh} disabled={loading}><RefreshCw size={16} className={loading?'spin':''}/></button></div></div>
          <div className="filters"><label className="search-field"><Search size={17}/><input aria-label="Search opportunities" placeholder="Search company, role or location" value={search} onChange={e=>setSearch(e.target.value)}/></label><label className="select-filter"><Filter size={15}/><select aria-label="Work mode" value={mode} onChange={e=>setMode(e.target.value)}><option value="all">All locations</option><option value="remote">Remote only</option><option value="onsite">On-site / hybrid</option></select></label><label className="select-filter"><SlidersHorizontal size={15}/><select aria-label="Stipend filter" value={pay} onChange={e=>setPay(e.target.value)}><option value="all">All stipends</option>{Object.entries(PAY_LABELS).map(([id,label])=><option key={id} value={id}>{label}</option>)}</select></label><select className="source-filter" aria-label="Source filter" value={source} onChange={e=>setSource(e.target.value)}><option value="all">All sources</option>{[...new Set(jobs.map(j=>j.sourceType))].map(s=><option key={s}>{s}</option>)}</select>{(search||mode!=='all'||pay!=='all'||source!=='all')&&<button className="text-button" onClick={()=>{setSearch('');setMode('all');setPay('all');setSource('all');}}>Clear</button>}</div>
          {loading && !jobs.length ? <div className="loading">Loading researched opportunities…</div> : !visible.length ? <div className="empty-result"><Search size={24}/><h3>No opportunities match these filters</h3><p>Try another company, location or stipend filter.</p></div> : view==='board' ? <div className="kanban" tabIndex={0} aria-label="Application Kanban board">{STAGES.map(stage=>{
            const cards=visible.filter(j=>j.status===stage.id);
            return <section key={stage.id} className={`kanban-column ${dragOver===stage.id?'drop-target':''}`} aria-label={`${stage.label} column`} onDragOver={e=>{e.preventDefault();setDragOver(stage.id);}} onDragLeave={e=>{if(!e.currentTarget.contains(e.relatedTarget))setDragOver('');}} onDrop={e=>{e.preventDefault();const id=e.dataTransfer.getData('text/plain');if(jobs.some(j=>j.id===id))move(id,stage.id);setDragging('');setDragOver('');}}>
              <div className="column-title"><h2>{stage.label}</h2><span>{cards.length}</span>{stage.id==='discovered'&&<button className="icon-button" aria-label="Add discovered opportunity" onClick={()=>setModal('add')}><Plus size={16}/></button>}</div>
              <div className="column-cards">{cards.map(job=><JobCard key={job.id} job={job} dragging={dragging===job.id} onOpen={()=>setSelected(job.id)} onDragStart={e=>{e.dataTransfer.setData('text/plain',job.id);e.dataTransfer.effectAllowed='move';setDragging(job.id);}} onDragEnd={()=>{setDragging('');setDragOver('');}}/>)}{!cards.length&&<div className="column-empty"><span className="empty-icon">{stage.id==='interview'?<CalendarDays size={20}/>:<ClipboardList size={20}/>}</span><strong>{stage.id==='discovered'?'All caught up':`No ${stage.label.toLowerCase()} roles yet`}</strong><p>{stage.help}. Move a card here or update its status.</p></div>}</div>
            </section>;
          })}</div> : <JobTable jobs={visible} onOpen={setSelected} onMove={move}/>}
          <div className="board-footer"><span>{visible.length} of {jobs.length} opportunities</span><span>Drag cards to move them, or open a card to change its status.</span></div>
        </>}
        {page==='followups' && <div className="followup-page"><div className="section-header"><h2>Due now <span className="count-tag">{due.length}</span></h2><span>{dateLabel(localDate())}</span></div>{!due.length?<div className="large-empty"><CalendarDays size={30}/><h3>No actions due</h3><p>Open any opportunity to add a next step and a due date.</p><button className="button secondary" onClick={()=>setPage('opportunities')}>Open opportunities</button></div>:due.map(j=><ActionRow key={j.id} job={j} onOpen={()=>setSelected(j.id)}/>)}<div className="section-header"><h2>Upcoming actions</h2></div>{active.filter(j=>j.dueDate&&!isDue(j)).sort((a,b)=>a.dueDate.localeCompare(b.dueDate)).map(j=><ActionRow key={j.id} job={j} onOpen={()=>setSelected(j.id)}/>)}{!active.some(j=>j.dueDate&&!isDue(j))&&<p className="muted">No upcoming deadlines recorded.</p>}<div className="section-header"><h2>Interviews</h2></div>{interviews.length?interviews.map(j=><ActionRow key={j.id} job={j} onOpen={()=>setSelected(j.id)} interview/>):<p className="muted">No interviews recorded yet. Add only confirmed invitations.</p>}</div>}
        {page==='sources' && <Sources meta={meta} sources={sources} onRefresh={refresh}/>}
        {page==='profile' && <Profile profile={profile} onSave={value=>{setProfile(value);announce('Profile saved in this browser.');}}/>}
      </div>
    </main>
    {selectedJob&&<JobDrawer job={selectedJob} profile={profile} onClose={()=>setSelected(null)} onUpdate={changes=>update(selectedJob.id,changes)} onProfile={()=>{setSelected(null);setPage('profile');}} onNotify={announce}/>}
    {modal==='add'&&<AddModal onClose={()=>setModal(null)} onAdd={addJob}/>}
    {toast&&<div className="toast" role="status"><Check size={17}/>{toast}<button onClick={()=>setToast('')} aria-label="Dismiss notification"><X size={15}/></button></div>}
  </div>;
}
function Stat({label,value,detail,highlight}) { return <div className={`stat ${highlight?'stat-highlight':''}`}><span>{label}</span><strong>{value}<span className="stat-unit">{highlight?'verified':''}</span></strong><small>{detail}</small></div>; }
function JobCard({job,onOpen,onDragStart,onDragEnd,dragging}) {
  const match=payMatch(job);
  return <article className={`job-card ${dragging?'dragging':''}`} draggable onDragStart={onDragStart} onDragEnd={onDragEnd}>
    <div className="card-top"><span className={`company-initial color-${job.company.length%4}`}>{job.company.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase()}</span><span className="company-name">{job.company}</span><GripVertical size={15} className="grip" aria-hidden="true"/></div>
    <button className="card-open" onClick={onOpen}><h3>{job.title}</h3><span>{job.location}</span></button>
    <div className="card-tags"><span className={job.workMode==='Remote'?'tag remote':'tag'}>{job.workMode}</span><span className="tag">Internship</span></div>
    <div className="card-pay"><strong>{stipend(job)}</strong><span className={`pay-label ${match}`}>{PAY_LABELS[match]}</span></div>
    {job.nextAction&&<div className="card-next"><CalendarDays size={13}/><span>{job.nextAction}</span></div>}
    <div className="card-bottom"><span>{job.sourceType}</span><button onClick={onOpen} aria-label={`View ${job.company} role details`}>View role<ArrowUpRight size={14}/></button></div>
    {isDue(job)&&<div className="due-badge">Action due {dateLabel(job.dueDate)}</div>}
  </article>;
}
function JobTable({jobs,onOpen,onMove}) { return <div className="table-wrap"><table><thead><tr><th>Opportunity</th><th>Location</th><th>Stipend / month</th><th>Status</th><th>Next action</th></tr></thead><tbody>{jobs.map(j=><tr key={j.id}><td><button className="table-role" onClick={()=>onOpen(j.id)}>{j.title}<span>{j.company}</span></button></td><td>{j.location}<span className="table-sub">{j.workMode}</span></td><td>{stipend(j)}<span className={`pay-label ${payMatch(j)}`}>{PAY_LABELS[payMatch(j)]}</span></td><td><select aria-label={`Status for ${j.company}`} value={j.status} onChange={e=>onMove(j.id,e.target.value)}>{STAGES.map(s=><option value={s.id} key={s.id}>{s.label}</option>)}</select></td><td>{j.nextAction||<span className="muted">Add a next step</span>}{j.dueDate&&<span className="table-sub">{dateLabel(j.dueDate)}</span>}</td></tr>)}</tbody></table></div>; }
function ActionRow({job,onOpen,interview}) { return <button className="action-row" onClick={onOpen}><span className="company-initial">{job.company.slice(0,2)}</span><div><strong>{interview ? (job.interviewAt?new Date(job.interviewAt).toLocaleString('en-IN'):'Interview time not set') : job.nextAction || 'Review next step'}</strong><span>{job.company} · {job.title}</span></div><time>{dateLabel(interview?job.interviewAt:job.dueDate)}</time><ChevronRight size={18}/></button>; }
function Sources({meta,sources,onRefresh}) { return <div className="sources-page"><div className="info-panel"><ShieldCheck size={23}/><div><h2>Evidence stays with every role</h2><p>“Meets stipend” requires the minimum to be stated in the employer's listing. Search snippets and third-party salary claims do not count as confirmation.</p><p>Listing availability is a page observation, not a guarantee the employer is still recruiting. Published dates and discovery dates are kept separate.</p></div></div><div className="section-header"><h2>Coverage and refresh</h2><button className="button secondary" onClick={onRefresh}><RefreshCw size={15}/>Reload feed</button></div><div className="coverage-grid"><div><strong>Company career pages</strong><p>Known career pages and supported structured feeds have a read-only collector. New candidates need review; changed, missing or blocked pages are flagged.</p></div><div><strong>Job boards & LinkedIn</strong><p>The enabled daily search task includes public job descriptions and hiring posts. Restricted sources may need manual checks or approved access.</p></div><div><strong>X & other social sources</strong><p>X was searched initially without a qualifying original post. The daily task includes public social search; results depend on platform access.</p></div></div><p className="muted">Research: {dateLabel(meta?.researchedAt)} · Last collector run: {meta?.collectorLastRun ? new Date(meta.collectorLastRun).toLocaleString('en-IN') : 'Not run yet'} · {meta?.scheduleStatus || 'Daily search enabled; automatic updates depend on source and GitHub access.'}</p><div className="source-list">{sources.map(s=><div key={s.id} className="source-row"><div><Link href={s.url}>{s.company || s.name}<ExternalLink size={13}/></Link><span>{s.kind==='role'?'Role page':s.kind==='careers'?'Career page':s.kind==='social'?'Social hiring post':'Job board'}</span></div><span className={`tag ${s.lastStatus==='ok'?'remote':''}`}>{s.lastStatus==='ok'?'Page fetched':s.lastStatus==='blocked'?'Manual check':s.lastStatus==='changed'?'Changed: review':s.lastStatus==='missing'?'Page missing':'Awaiting check'}</span>{s.lastChecked&&<time>{dateLabel(s.lastChecked)}</time>}</div>)}</div><div className="section-header"><h2>Excluded or unresolved</h2></div><ul className="evidence-list">{(meta?.excluded||[]).map((s,i)=><li key={i}><strong>{s.company}:</strong> {s.reason} {s.url&&<Link href={s.url}>Source</Link>}</li>)}</ul></div>; }
function Profile({profile,onSave}) { const [form,setForm]=useState(profile); return <form className="profile-form" onSubmit={e=>{e.preventDefault();onSave(form);}}><div className="info-panel"><FileText size={23}/><div><h2>Your facts, in your words</h2><p>These details stay in this browser. Nothing is sent to an employer from this page. Add links you are comfortable sharing when you apply.</p></div></div><div className="form-grid"><Field label="Name"><input value={form.name} onChange={e=>setForm({...form,name:e.target.value})} autoComplete="name"/></Field><Field label="Email"><input type="email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} autoComplete="email"/></Field><Field label="Portfolio URL"><input type="url" value={form.portfolio} placeholder="https://your-portfolio.com" onChange={e=>setForm({...form,portfolio:e.target.value})}/></Field><Field label="Résumé URL"><input type="url" value={form.resume} placeholder="Public or shareable link" onChange={e=>setForm({...form,resume:e.target.value})}/></Field></div><Field label="Availability"><input value={form.availability} placeholder="Earliest start date and internship duration" onChange={e=>setForm({...form,availability:e.target.value})}/></Field><Field label="Relevant experience or project facts"><textarea rows={6} value={form.background} placeholder="Add only experience and project details you want included in drafts." onChange={e=>setForm({...form,background:e.target.value})}/></Field><button className="button primary" type="submit">Save profile</button><p className="muted">Use Export → JSON backup to move your profile and board to another browser.</p></form>; }
function Field({label,children}) { return <label className="field"><span>{label}</span>{React.cloneElement(children, { "aria-label": label })}</label>; }
function ModalFrame({children,onClose,title,wide=false}) {
  const dialog=useRef(null),previous=useRef(document.activeElement);
  useEffect(()=>{
    const prevOverflow=document.body.style.overflow; document.body.style.overflow='hidden';
    const first=dialog.current?.querySelector('button, input, select, textarea, a[href]');first?.focus();
    function key(e){if(e.key==='Escape')onClose();if(e.key==='Tab') {const els=[...dialog.current.querySelectorAll('button:not([disabled]),input:not([disabled]),select,textarea,a[href]')].filter(el=>el.offsetParent!==null); if(!els.length)return; if(e.shiftKey&&document.activeElement===els[0]){e.preventDefault();els.at(-1).focus();}else if(!e.shiftKey&&document.activeElement===els.at(-1)){e.preventDefault();els[0].focus();}}}
    document.addEventListener('keydown',key);return()=>{document.body.style.overflow=prevOverflow;document.removeEventListener('keydown',key);previous.current?.focus?.();};
  },[]);
  return <div className={`overlay ${wide?'drawer-overlay':''}`} onMouseDown={e=>{if(e.target===e.currentTarget)onClose();}}><section ref={dialog} className={wide?'drawer':'modal'} role="dialog" aria-modal="true" aria-label={title}>{children}</section></div>;
}
function JobDrawer({job,profile,onClose,onUpdate,onProfile,onNotify}) {
  const [tab,setTab]=useState('details'), [form,setForm]=useState(job),[draft,setDraft]=useState('');
  useEffect(()=>{setForm(job);setDraft('');},[job.id]);
  function save(e){e.preventDefault();onUpdate({status:form.status,nextAction:form.nextAction,dueDate:form.dueDate,notes:form.notes,appliedAt:form.appliedAt||(form.status==='applied'?localDate():''),interviewAt:form.interviewAt||''});onNotify('Opportunity updated.');}
  function makeDraft(){
    const p=profile;
    setDraft(`Hi ${job.company} team,\n\nI'd like to apply for the ${job.title} role.\n\n${p.background ? p.background+'\n\n' : '[Add a specific reason this role interests you and a relevant project.]\n\n'}${p.portfolio ? `Portfolio: ${p.portfolio}\n` : 'Portfolio: [add your link]\n'}${p.resume ? `Résumé: ${p.resume}\n` : ''}${p.availability ? `Availability: ${p.availability}\n` : ''}\nThank you for considering my application.\n${p.name||'[Your name]'}`);setTab('draft');
  }
  const emailHref = job.email ? `mailto:${job.email}?subject=${encodeURIComponent(job.subject||job.title)}&body=${encodeURIComponent(draft)}` : '';
  return <ModalFrame title={`${job.company} opportunity`} onClose={onClose} wide><div className="drawer-header"><span>OPPORTUNITY DETAILS</span><button className="icon-button" aria-label="Close opportunity" onClick={onClose}><X size={20}/></button></div><div className="drawer-title"><span className="company-initial">{job.company.slice(0,2)}</span><div><p>{job.company}</p><h2>{job.title}</h2></div></div><div className="drawer-summary"><span className="tag">{job.workMode}</span><span>{job.location}</span><strong>{stipend(job)}</strong></div><div className="drawer-actions"><Link className="button primary" href={job.applicationUrl||job.sourceUrl}>Open application<ArrowUpRight size={15}/></Link><button className="button secondary" onClick={makeDraft}><FileText size={15}/>Prepare draft</button><Link href={job.sourceUrl} className="icon-button" ><ExternalLink size={18}/><span className="sr-only">View original source</span></Link></div><div className="drawer-tabs"><button className={tab==='details'?'active':''} onClick={()=>setTab('details')}>Details & next steps</button><button className={tab==='draft'?'active':''} onClick={()=>{if(!draft)makeDraft();else setTab('draft');}}>Application draft</button><button className={tab==='activity'?'active':''} onClick={()=>setTab('activity')}>Activity</button></div>
    <div className="drawer-body">{tab==='details'&&<><div className={`evidence-box ${payMatch(job)==='meets'?'confirmed':''}`}><strong>{PAY_LABELS[payMatch(job)]}</strong><p>{job.evidence}</p></div><h3>What the role needs</h3><p className="readable">{job.requirements}</p><div className="route-box"><Mail size={17}/><div><strong>{job.applicationMethod || 'Manual review'}</strong><p>{job.automationNotes||'Open the original listing and review its application requirements.'}</p>{job.email&&<Link href={`mailto:${job.email}`}>{job.email}</Link>}</div></div><div className="date-grid"><div><span>Posted</span><strong>{job.postedLabel||dateLabel(job.postedAt)}</strong></div><div><span>First discovered</span><strong>{dateLabel(job.firstSeen)}</strong></div><div><span>Source checked</span><strong>{dateLabel(job.checkedAt)}</strong></div></div><form onSubmit={save}><h3>Your next step</h3><div className="form-grid"><Field label="Status"><select value={form.status} onChange={e=>setForm({...form,status:e.target.value})}>{STAGES.map(s=><option key={s.id} value={s.id}>{s.label}</option>)}</select></Field><Field label="Action due"><input type="date" value={form.dueDate||''} onChange={e=>setForm({...form,dueDate:e.target.value})}/></Field></div><Field label="Next action"><input value={form.nextAction||''} placeholder="For example: tailor portfolio and confirm stipend" onChange={e=>setForm({...form,nextAction:e.target.value})}/></Field><div className="form-grid"><Field label="Applied date"><input type="date" value={form.appliedAt||''} onChange={e=>setForm({...form,appliedAt:e.target.value})}/></Field><Field label="Interview date & time (your local time)"><input type="datetime-local" value={form.interviewAt||''} onChange={e=>setForm({...form,interviewAt:e.target.value})}/></Field></div><Field label="Notes"><textarea rows={4} value={form.notes||''} onChange={e=>setForm({...form,notes:e.target.value})} placeholder="Recruiter replies, questions, portfolio version…"/></Field><button className="button primary" type="submit">Save changes</button></form></>}
    {tab==='draft'&&<><div className="info-panel compact"><FileText size={19}/><div><strong>Review before you send</strong><p>This draft uses only the facts in your profile. Add a specific connection to the role, follow the employer's instructions and remove any placeholders.</p></div></div>{job.applicationInstructions&&<div className="evidence-box"><strong>Employer's application instructions</strong><p>{job.applicationInstructions}</p></div>}<textarea className="draft-text" aria-label="Application draft" rows={17} value={draft} onChange={e=>setDraft(e.target.value)}/><div className="drawer-actions"><button className="button primary" onClick={async()=>{try{await navigator.clipboard.writeText(draft);onNotify('Draft copied.');}catch{onNotify('Select and copy the draft text.');}}}>Copy draft</button>{job.email&&<Link href={emailHref} className="button secondary">Open email draft<Mail size={15}/></Link>}<button className="text-button" onClick={onProfile}>Edit profile</button></div><p className="muted">Opening a form or email does not mark this role as applied. Update the board after you submit.</p></>}
    {tab==='activity'&&<><div className="activity-item"><span className="activity-date">{dateLabel(job.firstSeen)}</span><strong>Added to researched opportunities</strong><p>{job.sourceType}</p></div>{job.events?.map((event,i)=><div className="activity-item" key={i}><span className="activity-date">{dateLabel(event.at)}</span><strong>{event.label}</strong></div>)}{!job.events?.length&&<p className="muted">Your status changes will appear here.</p>}</>}
    </div></ModalFrame>;
}
function AddModal({onClose,onAdd}) {
  const [form,setForm]=useState({company:'',title:'',location:'Remote, India',workMode:'Remote',region:'India',sourceUrl:'',applicationUrl:'',payMin:'',payMax:'',requirements:'',applicationMethod:'Manual review',payVerified:false}),[error,setError]=useState('');
  function submit(e){e.preventDefault();try{if(!form.company.trim()||!form.title.trim())throw new Error('Company and role are required.');if(form.sourceUrl&&!safeUrl(form.sourceUrl))throw new Error('Enter a valid source URL.');if(form.payMax&&+form.payMax<+form.payMin)throw new Error('Maximum stipend must be at least the minimum.');onAdd({...form,company:form.company.trim(),title:form.title.trim(),payMin:form.payMin===''?null:+form.payMin,payMax:form.payMax===''?null:+form.payMax});}catch(err){setError(err.message);}}
  const change=(key,value)=>setForm({...form,[key]:value});
  return <ModalFrame title="Add opportunity" onClose={onClose}><div className="modal-header"><h2>Add opportunity</h2><button className="icon-button" onClick={onClose} aria-label="Close add opportunity"><X size={20}/></button></div><p className="muted">Found a role in a post or a company page? Keep it here.</p><form onSubmit={submit}>{error&&<div className="error-banner" role="alert">{error}</div>}<div className="form-grid"><Field label="Company *"><input required value={form.company} onChange={e=>change('company',e.target.value)}/></Field><Field label="Role *"><input required value={form.title} onChange={e=>change('title',e.target.value)}/></Field></div><Field label="Source URL"><input type="url" value={form.sourceUrl} placeholder="https://…" onChange={e=>change('sourceUrl',e.target.value)}/></Field><div className="form-grid"><Field label="Location"><input value={form.location} onChange={e=>change('location',e.target.value)}/></Field><Field label="Work mode"><select value={form.workMode} onChange={e=>change('workMode',e.target.value)}><option>Remote</option><option>On-site</option><option>Hybrid</option><option>Unconfirmed</option></select></Field></div><Field label="Region"><select value={form.region} onChange={e=>change('region',e.target.value)}><option>India</option><option>Gujarat</option><option>Maharashtra</option><option>Southern India</option><option>Goa</option></select></Field><div className="form-grid"><Field label="Minimum stipend / month (INR)"><input type="number" min="0" value={form.payMin} onChange={e=>change('payMin',e.target.value)}/></Field><Field label="Maximum stipend / month (INR)"><input type="number" min="0" value={form.payMax} onChange={e=>change('payMax',e.target.value)}/></Field></div><label className="check-field"><input type="checkbox" checked={form.payVerified} onChange={e=>change('payVerified',e.target.checked)}/>I checked this stipend in the original employer listing.</label><button className="button primary" type="submit">Add to discovered</button></form></ModalFrame>;
}
createRoot(document.getElementById('root')).render(<React.StrictMode><App/></React.StrictMode>);
