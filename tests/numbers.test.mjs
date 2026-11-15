import test from'node:test';import assert from'node:assert/strict';import{keepNumbers}from'../src/numbers.js';
test('grouped numbers keep their digits on one line',()=>{assert.equal(keepNumbers('varav 8 260 ingick'),'varav 8 260 ingick');assert.equal(keepNumbers('48 745 kaatunutta ja 158 863'),'48 745 kaatunutta ja 158 863');});
test('ordinary spaces and years are left alone',()=>{assert.equal(keepNumbers('11 February 1940'),'11 February 1940');assert.equal(keepNumbers('the 28 November'),'the 28 November');});
