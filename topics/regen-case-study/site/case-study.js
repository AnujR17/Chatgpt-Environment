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
let selected=D.presets[0],phase='choice',before=null,response='',outcome='';
const titles={pause:'Take a pause',continue:'Keep playing',smaller_goal:'Smaller goal'};
function mode(){const v=Number(byId('pleasantness').value)/100,a=Number(byId('activation').value)/100;if(selected.key==='mixed')return'choice';return v<D.thresholds.pleasantness&&a>D.thresholds.activation?'brief':v<D.thresholds.pleasantness&&a<-D.thresholds.activation?'small':'choice'}
function render(){
 const m=mode(),choosing=phase==='choice',playing=phase==='playing',follow=phase==='followup',rated=phase==='rated';
 byId('demo-feeling').textContent=selected.label;
 byId('mode-label').textContent=choosing?(m==='brief'?'Unpleasant / high activation':m==='small'?'Unpleasant / low activation':'Your next choice'):follow?'Later check-in':rated?'Your reported sequence':'Your choice';
 byId('cue-heading').textContent=choosing?(m==='brief'?'A pause is available':m==='small'?'One smaller goal':'Choose how to continue'):playing?titles[response]:follow?'A later moment':'Frustration and recovery';
 byId('cue-target').textContent=choosing?'Every response remains your choice.':playing?'First report: '+before.label:follow?'The next check-in can stay the same or change.':'';
 byId('cue-explanation').textContent='CMA combines pleasantness and activation. The prototype can highlight a pause or a smaller goal from a recent check-in. These are design choices to test, not automatic instructions.';
 byId('cue-details').open=false;byId('cue-details').hidden=!choosing;
 byId('smaller').hidden=!choosing;byId('keep-playing').hidden=!choosing;
 byId('cue-feedback').hidden=!follow;byId('try-cue').hidden=!choosing;byId('follow-up').hidden=!playing;
 byId('try-cue').textContent='Take a pause';
 byId('try-cue').className=m==='brief'?'primary-button':'outline-button';byId('smaller').className=m==='small'?'primary-button':'outline-button';
 byId('dimension-controls').disabled=playing||rated||selected.key==='mixed';
 for(const b of byId('presets').children){b.disabled=playing||rated;b.setAttribute('aria-pressed',String(b.dataset.key===selected.key))}
 for(const [id,output] of [['pleasantness','pleasantness-value'],['activation','activation-value']]){const n=Number(byId(id).value)/100;byId(output).value=selected.key==='mixed'?'Not specified':(n>0?'+':'')+n.toFixed(2)}
 byId('demo-status').textContent=rated?'First: '+before.label+'. Choice: '+titles[response]+'. Later: '+selected.label+'. Your feedback: '+(outcome==='yes'?'Helpful.':'Not helpful.')+(byId('lesson').value.trim()?' Note: '+byId('lesson').value.trim():''):'';
}
function select(row){if(phase==='playing'||phase==='rated')return;selected=row;byId('pleasantness').value=Math.round((row.pleasantness||0)*100);byId('activation').value=Math.round((row.activation||0)*100);canvases.get(byId('demo-character')).art={...NORI_BASE,...row.art};canvases.get(byId('demo-character')).dirty=true;byId('demo-character').setAttribute('aria-label','Nori representing '+row.label);render()}
function choose(kind){before={label:selected.label,pleasantness:Number(byId('pleasantness').value)/100,activation:Number(byId('activation').value)/100};response=kind;phase='playing';render()}
for(const row of D.presets){const b=document.createElement('button');b.textContent=row.label;b.dataset.key=row.key;b.setAttribute('aria-pressed','false');b.addEventListener('click',()=>select(row));byId('presets').append(b)}
for(const id of ['pleasantness','activation'])byId(id).addEventListener('input',render);
byId('smaller').addEventListener('click',()=>choose('smaller_goal'));
byId('keep-playing').addEventListener('click',()=>choose('continue'));
byId('try-cue').addEventListener('click',()=>choose('pause'));
byId('follow-up').addEventListener('click',()=>{phase='followup';render()});
byId('helped').addEventListener('click',()=>{outcome='yes';phase='rated';render()});
byId('stuck').addEventListener('click',()=>{outcome='no';phase='rated';render()});
byId('reset').addEventListener('click',()=>{phase='choice';before=null;response='';outcome='';byId('lesson').value='';select(D.presets[0])});
select(D.presets[0]);
window.regenCase={get state(){return{mode:mode(),phase,selected:selected.key,response,outcome,paused}},select:key=>select(D.presets.find(r=>r.key===key))};
window.addEventListener('beforeprint',()=>{
 for(const [canvas,row] of canvases){
  const ctx=canvas.getContext('2d');drawNori(ctx,row.art,0,false,true,0);
  let node=canvas.parentElement,color='rgb(245,243,233)';
  while(node){const c=getComputedStyle(node).backgroundColor;if(c!=='transparent'&&!/rgba\(.*,[ ]*0\)/.test(c)){color=c;break}node=node.parentElement}
  ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='destination-over';ctx.fillStyle=color;ctx.fillRect(0,0,canvas.width,canvas.height);ctx.restore();
 }
});

let playMuted=false,playTimer=0;
byId('simulate-fall').addEventListener('click',()=>{clearTimeout(playTimer);if(playMuted){byId('play-message').textContent='Tips are muted. Keep playing.';return}byId('play-message').textContent='Possible fall. Waiting for a steadier view…';byId('simulate-fall').disabled=true;playTimer=setTimeout(()=>{byId('simulate-fall').disabled=false;if(playMuted)return;const messages={'Next move':'One secure hold. Then try the next reach.','Encouragement':'Still in it. Your next try starts here.','Quiet pause':'A breath before the next try, if you want.'};byId('play-message').textContent=messages[byId('play-style').value]},2000)});
byId('mute-play').addEventListener('click',()=>{playMuted=!playMuted;clearTimeout(playTimer);byId('simulate-fall').disabled=false;byId('mute-play').setAttribute('aria-pressed',String(playMuted));byId('mute-play').textContent=playMuted?'Unmute tips':'Mute tips';byId('play-message').textContent=playMuted?'Tips are muted. Keep playing.':'Ready for the next try.'});
