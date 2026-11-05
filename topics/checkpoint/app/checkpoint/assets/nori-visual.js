'use strict';
const NORI_BASE={red:151,green:190,blue:175,stretch:0,tension:0,smile:0,eyes:1,brow:0,energy:.2,jaw:0,laugh:0,eye_left:1,eye_right:1,brow_skew:0,mouth_wide:0,pressed:0,pucker:0,snarl:0,asymmetry:0,teeth:0,hand:0,hand_side:1,mouth_visible:1,tears:0,lean:0};
function drawNori(ctx,v,phase,unknown,still,time){
 const s=153.6;let cx=160,cy=160;
 if(!still)cy-=s*.016*v.laugh*(.5+.5*Math.sin(phase*6));
 ctx.setTransform(2,0,0,2,0,0);ctx.clearRect(0,0,320,320);
 ctx.fillStyle='rgba(52,69,62,.075)';ctx.beginPath();ctx.ellipse(cx,cy+s*.83,s*.64,s*.07,0,0,Math.PI*2);ctx.fill();
 const body=`rgb(${Math.round(v.red)},${Math.round(v.green)},${Math.round(v.blue)})`,ink='#34453e',pts=[];
 for(let i=0;i<64;i++){let a=2*Math.PI*i/64,r=.76+.045*Math.sin(3*a+.5)+.025*Math.cos(2*a-.8)+v.tension*.02*Math.cos(4*a)+.012*Math.sin(phase)*Math.sin(a)**2;pts.push([cx+(Math.cos(a)*r*(1-v.stretch*.35)+v.lean*Math.sin(a))*s,cy+Math.sin(a)*r*(1+v.stretch)*s])}
 ctx.beginPath();ctx.moveTo(...pts[0]);for(let i=0;i<64;i++){const p0=pts[(i+63)%64],p1=pts[i],p2=pts[(i+1)%64],p3=pts[(i+2)%64];ctx.bezierCurveTo(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6,p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6,...p2)}ctx.closePath();ctx.fillStyle=body;ctx.strokeStyle=unknown?'#8b9d92':ink;ctx.lineWidth=2.8;ctx.lineJoin='round';ctx.fill();ctx.stroke();
 cx+=v.lean*s*.25;const ey=cy-s*.02,ex=s*.23,blink=!unknown&&!still&&time%7.8>7.63?.12:1;
 ctx.strokeStyle=ink;ctx.fillStyle=ink;ctx.lineCap='round';
 for(const d of[-1,1]){const x=cx+d*ex,eye=d<0?v.eye_left:v.eye_right;ctx.beginPath();if((v.smile>.28&&eye<.9)||v.laugh>.15){ctx.moveTo(x-s*.05,ey+s*.018);ctx.quadraticCurveTo(x,ey-s*.08,x+s*.05,ey+s*.018);ctx.stroke()}else{ctx.ellipse(x,ey,s*.035,Math.max(1.8,s*.065*eye*blink),0,0,Math.PI*2);ctx.fill()}}
 if(Math.max(Math.abs(v.brow),Math.abs(v.brow_skew))>.15)for(const d of[-1,1]){const x=cx+d*ex,y=ey-s*.18,b=v.brow+d*v.brow_skew;ctx.beginPath();ctx.moveTo(x-s*.075,y+d*b*s*.09);ctx.lineTo(x+s*.075,y-d*b*s*.09);ctx.stroke()}
 if(v.mouth_visible>.5){const mw=s*(.14+.065*v.mouth_wide+.055*Math.max(0,v.smile)-.055*v.pucker),y=ey+s*.21,ly=y+v.asymmetry*s*.045,ry=y-v.asymmetry*s*.045,curve=y+s*(v.smile*.26-v.snarl*.06),opening=s*Math.max(v.jaw*.27*(1-.65*v.pressed),v.teeth*.075);
 const mouth=new Path2D();mouth.moveTo(cx-mw,ly);mouth.quadraticCurveTo(cx,curve,cx+mw,ry);if(opening>s*.015){mouth.quadraticCurveTo(cx,curve+opening,cx-mw,ly);mouth.closePath();ctx.fill(mouth)}ctx.stroke(mouth);
 if(v.teeth>.15&&opening>s*.025){ctx.save();ctx.clip(mouth);ctx.fillStyle='#fffced';ctx.beginPath();ctx.moveTo(cx-mw,ly+1);ctx.quadraticCurveTo(cx,curve+1,cx+mw,ry+1);ctx.quadraticCurveTo(cx,curve+opening*.5+1,cx-mw,ly+opening*.5+1);ctx.closePath();ctx.fill();ctx.strokeStyle='#9dab9e';ctx.lineWidth=1.2;for(const dx of[-.04,.04]){ctx.beginPath();ctx.moveTo(cx+s*dx,y-s*.1);ctx.lineTo(cx+s*dx,y+s*.3);ctx.stroke()}ctx.restore()}}
 if(v.tears>.05){ctx.fillStyle='#8cbac5';for(const d of[-1,1]){ctx.beginPath();ctx.ellipse(cx+d*ex,ey+s*.18,s*.027,s*.065*v.tears,0,0,Math.PI*2);ctx.fill()}}
 if(v.hand>.025){const side=v.hand_side>=0?1:-1,r=v.hand,sx=cx+side*s*.56,sy=cy+s*.43,x=sx+(cx+side*s*.06-sx)*r,y=sy+(ey+s*.24-sy)*r;ctx.save();ctx.globalAlpha=r;ctx.beginPath();ctx.moveTo(sx,sy);ctx.quadraticCurveTo(sx,y+s*.18,x,y);ctx.strokeStyle=ink;ctx.lineWidth=s*.145;ctx.stroke();ctx.strokeStyle=body;ctx.lineWidth=s*.11;ctx.stroke();ctx.lineWidth=2.5;ctx.strokeStyle=ink;ctx.fillStyle=body;ctx.beginPath();ctx.ellipse(x,y,s*.12,s*.095,0,0,Math.PI*2);ctx.fill();ctx.stroke();for(const dy of[-.025,.025]){ctx.beginPath();ctx.moveTo(x-s*.03,y+s*dy);ctx.lineTo(x+s*.055,y+s*dy);ctx.stroke()}ctx.restore()}
}
