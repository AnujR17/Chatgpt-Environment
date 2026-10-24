import React from 'react';
import {ExternalLink,ShieldCheck} from 'lucide-react';
import {safeUrl,dateLabel} from './model';

export default function SourceCoverage({coverage=[],jobs=[]}) {
 if(!coverage.length)return null;
 return <section className="source-coverage" aria-label="Search coverage"><div className="section-header"><h2>Sources checked</h2></div>
  <div className="info-panel"><ShieldCheck size={22}/><div><h3>Coverage is separate from the shortlist</h3><p>A source can be checked without yielding a suitable role. Company directories and startup maps help find employers; they do not establish vacancies. Public searches need no linked account. Sign-in, robots restrictions, missing details and expired pages are recorded below.</p></div></div>
  <div className="coverage-source-grid">{coverage.map(source=>{const url=safeUrl(source.url);const findings=Array.isArray(source.findings)?source.findings.join(' '):source.findings;const hostname=url?new URL(url).hostname.replace(/^www\./,''):'';const count=hostname?jobs.filter(job=>[job.sourceUrl,...(job.additionalSources||[]).map(s=>s.url)].some(value=>{try{return new URL(value).hostname.replace(/^www\./,'')===hostname;}catch{return false;}})).length:null;return <article className="coverage-source-card" key={source.id||source.url}><div><h3>{source.source}</h3><span className="pill">{source.status}</span></div><p>{findings}</p>{source.limits&&<p className="coverage-limit">{source.limits}</p>}<div className="coverage-source-meta"><span>Checked {dateLabel(source.checkedAt)}</span>{count!=null&&<span>{count} role {count===1?'record':'records'} linked to this website</span>}</div>{(source.exclusionExamples||[]).length>0&&<details><summary>Examples requiring exclusion or review</summary><ul>{source.exclusionExamples.map((example,i)=><li key={i}>{typeof example==='string'?example:example.reason||example.company}{typeof example==='object'&&safeUrl(example.url)&&<a href={safeUrl(example.url)} target="_blank" rel="noopener noreferrer">Source</a>}</li>)}</ul></details>}{url&&<a href={url} target="_blank" rel="noopener noreferrer">Open source<ExternalLink size={13}/></a>}</article>;})}</div>
 </section>;
}
