#!/usr/bin/env node
import {readFile} from 'node:fs/promises';
import {importResult} from '../src/applicationKit.js';

try {
  const [requestPath,resultPath]=process.argv.slice(2);
  if(!requestPath||!resultPath)throw Error('Usage: node scripts/check_application_result.mjs REQUEST.json RESULT.json');
  const request=JSON.parse(await readFile(requestPath,'utf8'));
  const result=await importResult(JSON.parse(await readFile(resultPath,'utf8')),request);
  console.log(JSON.stringify({valid:true,jobId:result.jobId,documents:Object.keys(result.documents),claims:result.review.claims.length}));
}catch(error){console.error(JSON.stringify({error:error.message}));process.exitCode=1;}
