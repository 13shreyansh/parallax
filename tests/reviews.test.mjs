import test from 'node:test';import assert from 'node:assert/strict';import {mergeFlagEdits} from '../src/reviews.js';
const t='2026-11-15T02:00:00Z';
test('an older read cannot undo an acknowledged dismissal',()=>{assert.equal(mergeFlagEdits([{id:'x',dismissed:false}],{x:{dismissed:true,reviewed_at:t}})[0].dismissed,true);});
test('a same-second older dismissal cannot undo reopen',()=>{assert.equal(mergeFlagEdits([{id:'x',dismissed:true,reviewed_at:t}],{x:{dismissed:false,reviewed_at:t}})[0].dismissed,false);});
test('a later editor action wins and copy count stays monotonic',()=>{const r=mergeFlagEdits([{id:'x',dismissed:false,review_reason:null,reviewed_at:'2026-11-15T02:00:02Z',copied_count:4}],{x:{dismissed:true,review_reason:'earlier',reviewed_at:t,copied_count:3}})[0];assert.equal(r.dismissed,false);assert.equal(r.review_reason,null);assert.equal(r.copied_count,4);});
