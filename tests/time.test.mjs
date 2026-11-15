import test from'node:test';import assert from'node:assert/strict';import{date,day}from'../src/time.js';
test('database UTC timestamps keep their date in Helsinki',()=>{process.env.TZ='Europe/Helsinki';assert.equal(day('2026-11-15 00:05:00'),'2026-11-15');assert.equal(date('2012-11-28 18:04:48Z'),'28 Nov 2012');});
test('unknown dates never render invalid internals',()=>{assert.equal(date('None'),'');assert.equal(day(null),'');});
