'use strict';
const NORI_BASE={red:131,green:210,blue:187,stretch:0,tension:0,smile:0,eyes:1,brow:0,energy:.2,jaw:0,laugh:0,eye_left:1,eye_right:1,brow_skew:0,mouth_wide:0,pressed:0,pucker:0,snarl:0,asymmetry:0,teeth:0,hand:0,hand_side:1,mouth_visible:1,tears:0,lean:0};
function drawNori(ctx,v,phase,unknown,still,time){
 const s=153.6;let cx=160,cy=160;
 if(!still)cy-=s*.016*v.laugh*(.5+.5*Math.sin(phase*6));
 ctx.setTransform(2,0,0,2,0,0);ctx.clearRect(0,0,320,320);
 ctx.fillStyle='rgba(52,69,62,.075)';ctx.beginPath();ctx.ellipse(cx,cy+s*.83,s*.64,s*.07,0,0,Math.PI*2);ctx.fill();
 const body=`rgb(${Math.round(v.red)},${Math.round(v.green)},${Math.round(v.blue)})`,ink='#29334b',pts=[];
 for(let i=0;i<64;i++){const a=2*Math.PI*i/64,c=Math.cos(a),t=Math.sin(a);let x=Math.sign(c)*Math.abs(c)**.78*.67,y=Math.sign(t)*Math.abs(t)**.88*.78;x*=1+.10*t;if(t>0){y-=.10*Math.exp(-((x/.22)**2))*t**6;x+=.035*t**3}const b=.007*Math.sin(phase);x*=1-v.stretch*.28+b;y*=1+v.stretch-b;x+=v.lean*t*.45;pts.push([cx+x*s,cy+y*s])}
 ctx.beginPath();ctx.moveTo(...pts[0]);for(let i=0;i<64;i++){const p0=pts[(i+63)%64],p1=pts[i],p2=pts[(i+1)%64],p3=pts[(i+2)%64];ctx.bezierCurveTo(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6,p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6,...p2)}ctx.closePath();ctx.fillStyle=body;ctx.strokeStyle=unknown?'#8b9d92':ink;ctx.lineWidth=2.8;ctx.lineJoin='round';ctx.fill();
 cx+=v.lean*s*.25;const ey=cy-s*.02,ex=s*.23,blink=!unknown&&!still&&time%7.8>7.63?.12:1;
 ctx.strokeStyle=ink;ctx.fillStyle=ink;ctx.lineCap='round';
 for(const d of[-1,1]){const x=cx+d*ex,eye=d<0?v.eye_left:v.eye_right;ctx.beginPath();if((v.smile>.28&&eye<.9)||v.laugh>.15){ctx.moveTo(x-s*.05,ey+s*.018);ctx.quadraticCurveTo(x,ey-s*.08,x+s*.05,ey+s*.018);ctx.stroke()}else{ctx.ellipse(x,ey,s*.035,Math.max(1.8,s*.065*eye*blink),0,0,Math.PI*2);ctx.fill()}}
 if(Math.max(Math.abs(v.brow),Math.abs(v.brow_skew))>.15)for(const d of[-1,1]){const x=cx+d*ex,b=Math.max(-1,Math.min(1,v.brow)),k=Math.max(-1,Math.min(1,v.brow_skew)),y=ey+s*(-.19-d*k*.025),tilt=d*Math.max(-1,Math.min(1,b+d*k))*.025*s;ctx.beginPath();ctx.moveTo(x-s*.055,y+tilt);ctx.quadraticCurveTo(x,y-s*.035,x+s*.055,y-tilt);ctx.stroke()}
 if(v.mouth_visible>.5){const mw=s*(.14+.065*v.mouth_wide+.055*Math.max(0,v.smile)-.055*v.pucker),y=ey+s*.21,ly=y+v.asymmetry*s*.045,ry=y-v.asymmetry*s*.045,curve=y+s*(v.smile*.26-v.snarl*.06),opening=s*Math.max(v.jaw*.27*(1-.65*v.pressed),v.teeth*.075);
 const mouth=new Path2D();mouth.moveTo(cx-mw,ly);mouth.quadraticCurveTo(cx,curve,cx+mw,ry);if(opening>s*.015){mouth.quadraticCurveTo(cx,curve+opening,cx-mw,ly);mouth.closePath();ctx.fill(mouth)}ctx.stroke(mouth);
 if(v.teeth>.15&&opening>s*.025){ctx.save();ctx.clip(mouth);ctx.fillStyle='#fffced';ctx.beginPath();ctx.moveTo(cx-mw,ly+1);ctx.quadraticCurveTo(cx,curve+1,cx+mw,ry+1);ctx.quadraticCurveTo(cx,curve+opening*.5+1,cx-mw,ly+opening*.5+1);ctx.closePath();ctx.fill();ctx.strokeStyle='#9dab9e';ctx.lineWidth=1.2;for(const dx of[-.04,.04]){ctx.beginPath();ctx.moveTo(cx+s*dx,y-s*.1);ctx.lineTo(cx+s*dx,y+s*.3);ctx.stroke()}ctx.restore()}}
 if(v.tears>.05){ctx.fillStyle='#8cbac5';for(const d of[-1,1]){ctx.beginPath();ctx.ellipse(cx+d*ex,ey+s*.18,s*.027,s*.065*v.tears,0,0,Math.PI*2);ctx.fill()}}
 if(v.hand>.025){const side=v.hand_side>=0?1:-1,r=v.hand,x=cx+side*s*(.52-.42*r),y=cy+s*(.43-.20*r);ctx.save();ctx.globalAlpha=r;ctx.fillStyle=body;ctx.beginPath();ctx.moveTo(x-side*s*.10,y+s*.08);ctx.bezierCurveTo(x-side*s*.16,y-s*.05,x-side*s*.03,y-s*.15,x+side*s*.06,y-s*.08);ctx.bezierCurveTo(x+side*s*.18,y-s*.10,x+side*s*.20,y+s*.08,x+side*s*.06,y+s*.12);ctx.closePath();ctx.fill();ctx.restore()}
}
