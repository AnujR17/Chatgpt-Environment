import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react(),{
  name:'local-assistant-api',
  configureServer(server){server.middlewares.use('/api/assistant',async(req,res)=>{
    let size=0;const chunks=[];
    try{
      for await(const chunk of req){size+=chunk.length;if(size>250000){res.statusCode=413;res.end('Request too large');return;}chunks.push(chunk);}
      const raw=Buffer.concat(chunks).toString();req.body=raw?JSON.parse(raw):undefined;
      res.status=code=>{res.statusCode=code;return res;};res.json=value=>{res.setHeader('Content-Type','application/json');res.end(JSON.stringify(value));return res;};
      const {default:handler}=await import('./api/assistant.js');await handler(req,res);
    }catch{res.statusCode=400;res.setHeader('Content-Type','application/json');res.end(JSON.stringify({error:{code:'invalid_request',message:'Could not read the application request.'}}));}
  });},
}]});
