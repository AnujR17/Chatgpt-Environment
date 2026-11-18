'use strict';
const D=window.REGEN_CASE;
const byId=id=>document.getElementById(id);
const media=matchMedia('(prefers-reduced-motion: reduce)');
let paused=media.matches;
const canvases=new Map();
function register(canvas,art){canvases.set(canvas,{art:{...NORI_BASE,...art},visible:true,dirty:true});return canvas}
function look(key){return D.family.find(x=>x.key===key)?.art||D.presets.find(x=>x.key===key)?.art||NORI_BASE}
for(const canvas of document.querySelectorAll('canvas[data-look]'))register(canvas,look(canvas.dataset.look));
for(const [i,key] of ['frustrated','confused','amused'].entries()){
 const c=document.createElement('canvas');c.width=c.height=640;c.setAttribute('aria-label',D.family.find(x=>x.key===key).label+' authored expression');register(c,look(key));byId('emotion-parade').append(c);
}
for(const item of D.family){
 const cell=document.createElement('div');cell.className='look';const c=document.createElement('canvas');c.width=c.height=640;c.setAttribute('aria-hidden','true');register(c,item.art);const name=document.createElement('span');name.textContent=item.label;cell.append(c,name);byId('character-family').append(cell);
}
const observer=new IntersectionObserver(entries=>{for(const entry of entries){const row=canvases.get(entry.target);if(row)row.visible=entry.isIntersecting}},{rootMargin:'50px'});
for(const canvas of canvases.keys())observer.observe(canvas);
register(byId('demo-character'),D.presets[0].art);observer.observe(byId('demo-character'));
let last=0;
function frame(t){if(t-last>30&&!document.hidden){last=t;for(const [canvas,row] of canvases)if(row.visible&&(!paused||row.dirty)){drawNori(canvas.getContext('2d'),row.art,paused?0:t/1800,false,paused,t/1000);row.dirty=false}}requestAnimationFrame(frame)}
requestAnimationFrame(frame);
function motion(){for(const row of canvases.values())row.dirty=true;byId('motion').textContent=paused?'Play motion':'Pause motion';byId('motion').setAttribute('aria-pressed',String(paused));document.body.dataset.motion=paused?'reduced':'normal'}
byId('motion').addEventListener('click',()=>{paused=!paused;motion()});media.addEventListener('change',()=>{paused=media.matches;motion()});motion();
for(const button of document.querySelectorAll('[data-theme]'))button.addEventListener('click',()=>{const dark=button.dataset.theme==='dark';byId('app-screen').src=dark?'assets/dark.png':'assets/session.png';byId('app-screen').alt='Actual native Regen app in '+(dark?'dark':'light')+' theme';for(const b of document.querySelectorAll('[data-theme]')){b.classList.toggle('selected',b===button);b.setAttribute('aria-pressed',String(b===button))}});
let selected=D.presets[0],override=null,phase='choice',rated='';
function mode(){if(override)return override;const v=Number(byId('pleasantness').value)/100,a=Number(byId('activation').value)/100;if(selected.key==='mixed')return'choice';return v<-.18&&a>.4?'brief':v<-.18&&a<-.4?'small':'choice'}
function render(){
 const m=mode(),small=m==='small',brief=m==='brief',pending=phase==='playing';
 byId('demo-feeling').textContent=selected.label;
 byId('mode-label').textContent=small?'One smaller target':brief?'One cue first':'Choose the amount of help';
 byId('cue-heading').textContent=small?D.cue.target:D.cue.cue;
 byId('cue-target').textContent=small?'Practise this part once.':brief?'One change for the next attempt.':D.cue.target;
 byId('cue-explanation').textContent=D.cue.explanation;
 byId('cue-details').open=!brief;
 byId('smaller').hidden=small||pending;
 byId('cue-feedback').hidden=!pending;
 byId('try-cue').hidden=pending;
 byId('try-cue').textContent=small?'Try the smaller target':'Try this cue';
 byId('dimension-controls').disabled=pending||selected.key==='mixed';
 for(const b of byId('presets').children){b.disabled=pending;b.setAttribute('aria-pressed',String(b.dataset.key===selected.key))}
 for(const [id,output] of [['pleasantness','pleasantness-value'],['activation','activation-value']]){const n=Number(byId(id).value)/100;byId(output).value=selected.key==='mixed'?'Not specified':(n>0?'+':'')+n.toFixed(2)}
 const note=byId('lesson').value.trim();
 byId('demo-status').textContent=pending?'Cue selected. In the app, you return to your game.':rated==='helped'?'Marked helpful.'+(note?' Your note: '+note:''):rated==='stuck'?'Still stuck. Try a smaller target or choose another cue.':'This example uses a chosen check-in, not camera analysis.';
}
function select(row){selected=row;override=null;phase='choice';rated='';byId('lesson').value='';byId('pleasantness').value=Math.round((row.pleasantness||0)*100);byId('activation').value=Math.round((row.activation||0)*100);canvases.get(byId('demo-character')).art={...NORI_BASE,...row.art};canvases.get(byId('demo-character')).dirty=true;byId('demo-character').setAttribute('aria-label','Nori representing '+row.label);render()}
for(const row of D.presets){const b=document.createElement('button');b.textContent=row.label;b.dataset.key=row.key;b.setAttribute('aria-pressed','false');b.addEventListener('click',()=>select(row));byId('presets').append(b)}
for(const id of ['pleasantness','activation'])byId(id).addEventListener('input',()=>{override=null;rated='';render()});
byId('smaller').addEventListener('click',()=>{override='small';rated='';render()});
byId('try-cue').addEventListener('click',()=>{phase='playing';render();byId('lesson').focus()});
byId('helped').addEventListener('click',()=>{phase='choice';rated='helped';render()});
byId('stuck').addEventListener('click',()=>{phase='choice';rated='stuck';override='small';render()});
byId('reset').addEventListener('click',()=>select(D.presets[0]));
select(D.presets[0]);
window.regenCase={get state(){return{mode:mode(),phase,selected:selected.key,paused}},select:key=>select(D.presets.find(r=>r.key===key))};

window.addEventListener('beforeprint',()=>{
 for(const [canvas,row] of canvases){
  const ctx=canvas.getContext('2d');drawNori(ctx,row.art,0,false,true,0);
  let node=canvas.parentElement,color='rgb(245,243,233)';
  while(node){const c=getComputedStyle(node).backgroundColor;if(c!=='transparent'&&!/rgba\(.*,[ ]*0\)/.test(c)){color=c;break}node=node.parentElement}
  ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='destination-over';ctx.fillStyle=color;ctx.fillRect(0,0,canvas.width,canvas.height);ctx.restore();
 }
});
