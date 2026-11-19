"use strict";
const D=window.REGEN_CASE;
function look(key){return D.family.find(x=>x.key===key)?.art||D.presets.find(x=>x.key===key)?.art||NORI_BASE}
function paint(canvas,art){const ctx=canvas.getContext('2d');drawNori(ctx,{...NORI_BASE,...art},0,false,true,0);let n=canvas.parentElement,bg='#f5f3e9';while(n){const c=getComputedStyle(n).backgroundColor;if(c!=='transparent'&&!/rgba\(.*,[ ]*0\)/.test(c)){bg=c;break}n=n.parentElement}ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalCompositeOperation='destination-over';ctx.fillStyle=bg;ctx.fillRect(0,0,canvas.width,canvas.height);ctx.restore()}
for(const canvas of document.querySelectorAll('canvas[data-look]'))paint(canvas,look(canvas.dataset.look));
const parade=document.getElementById('emotion-parade');
for(const key of ['frustrated','surprised','happy']){const c=document.createElement('canvas');c.width=c.height=640;c.setAttribute('aria-label',key);parade.append(c);paint(c,look(key))}
const family=document.getElementById('character-family');
for(const item of D.family){const cell=document.createElement('div');cell.className='look';const c=document.createElement('canvas');c.width=c.height=640;c.setAttribute('aria-hidden','true');const name=document.createElement('span');name.textContent=item.label;cell.append(c,name);family.append(cell);paint(c,item.art)}
