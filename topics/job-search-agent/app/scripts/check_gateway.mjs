// Explicit preview-build smoke test only. Never runs from the normal build.
// Uses fictional facts and at most two bounded model calls, no retries.
import {createRequest} from '../src/applicationKit.js';
import {generateApplication,publicGenerationError} from '../server/applicationGeneration.js';

const request=await createRequest({job:{id:'gateway-smoke-fictional',company:'Fictional Example Co',title:'Design intern',sourceUrl:'https://example.com/jobs/fictional'},profile:{name:'Fictional Test Candidate',background:'Built a prototype for a fictional student project.\nConducted five fictional practice interviews.',availability:'Available for three months in this fictional test.'},posting:'Fictional test role. Design a simple prototype and explain research tradeoffs. No degree, paid work experience or named-tool requirement. Pay is undisclosed. No real application should be made.',requirements:[{id:'R001',text:'Create and explain a prototype.',sourceUrl:'https://example.com/jobs/fictional'}],confirmed:true});
try {
  const output=await generateApplication(request,{signal:AbortSignal.timeout(140000)});
  console.log(JSON.stringify({gatewaySmoke:'passed',model:output.model,claims:output.result.review.claims.length,documents:Object.keys(output.result.documents),usage:output.usage,scope:'Fictional data only; no application sent'}));
}catch(error){const safe=publicGenerationError(error);console.log(JSON.stringify({gatewaySmoke:'blocked',code:safe.code,message:safe.message,settingsUrl:safe.settingsUrl}));}
