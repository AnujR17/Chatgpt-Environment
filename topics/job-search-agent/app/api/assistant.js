import {connectionStatus,generateApplication,publicGenerationError,MAX_REQUEST_BYTES} from '../server/applicationGeneration.js';
import {validateRequest} from '../src/applicationKit.js';

export function createHandler({generate=generateApplication,env=process.env}={}) {
  return async function handler(req,res) {
    res.setHeader('Cache-Control','private, no-store');
    res.setHeader('X-Content-Type-Options','nosniff');
    if(req.method==='GET')return res.status(200).json(connectionStatus(env));
    if(req.method!=='POST'){res.setHeader('Allow','GET, POST');return res.status(405).json({error:{code:'method_not_allowed',message:'Use POST to generate application documents.'}});}
    const host=req.headers.host;
    let origin;
    try {origin=new URL(req.headers.origin);}catch{}
    if(!host||!origin||origin.host!==host||req.headers['sec-fetch-site']==='cross-site')return res.status(403).json({error:{code:'origin_rejected',message:'Generate documents from this website.'}});
    if(!String(req.headers['content-type']||'').toLowerCase().includes('application/json'))return res.status(415).json({error:{code:'json_required',message:'Send a JSON application request.'}});
    let body;
    try {
      if(Number(req.headers['content-length']||0)>MAX_REQUEST_BYTES||Buffer.byteLength(JSON.stringify(req.body||''))>MAX_REQUEST_BYTES)throw Error('size');
      body=typeof req.body==='string'?JSON.parse(req.body):req.body;
      await validateRequest(body);
    }catch {return res.status(400).json({error:{code:'invalid_request',message:'The application request is incomplete, too large or changed. Review the posting and confirmed profile, then try again.'}});}
    const controller=new AbortController();
    const timeout=setTimeout(()=>controller.abort(),140_000);
    req.on?.('aborted',()=>controller.abort());
    res.on?.('close',()=>{if(!res.writableEnded)controller.abort();});
    try {
      const result=await generate(body,{env,signal:controller.signal});
      return res.status(200).json(result);
    }catch(error) {
      const safe=publicGenerationError(error);
      return res.status(safe.status).json({error:{code:safe.code,message:safe.message,...(safe.settingsUrl?{settingsUrl:safe.settingsUrl}:{})}});
    }finally{clearTimeout(timeout);}
  };
}
export default createHandler();
