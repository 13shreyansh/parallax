import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
const base=process.env.PARALLAX_URL || 'https://parallax-gamma-red.vercel.app';
const browser=await chromium.launch({headless:true});
const results=[];
for(const width of [1440,390]) {
 const page=await browser.newPage({viewport:{width,height:900}}); const errors=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 await page.goto(base);await page.getByRole('table',{name:'Articles ranked for review'}).waitFor();await page.locator('.table-row').first().waitFor();await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:`artifacts/e2e/core-home-${width}.png`});
 await page.getByRole('button',{name:'Number of issues',exact:true}).click();await page.locator('.table-row[href="/a/Q134949"]').waitFor();await page.locator('.table-row[href="/a/Q134949"]').click();
 await page.locator('.rail[aria-label="Finding evidence"]').waitFor({state:'attached'});
 await page.goto(`${base}/a/Q134949?flag=65c3491c5d1f63e938fe4b3e32617dc9`);
 await page.locator('.rail-heading h2').filter({hasText:'Not in source'}).waitFor({state:'attached'});
 if(width<700)await page.getByRole('button',{name:'Not in source flag',exact:true}).first().click();
 await page.locator('.source-reading .quote').waitFor();await page.locator('.rail-container').evaluate(e=>Promise.all(e.getAnimations().map(a=>a.finished)));await page.screenshot({path:`artifacts/e2e/core-source-${width}.png`});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 results.push({width,errors,overflow});await page.close();
}
await browser.close();await fs.writeFile('artifacts/e2e/core-results.json',JSON.stringify(results,null,2));console.log(results);
