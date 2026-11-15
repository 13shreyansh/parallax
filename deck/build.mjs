// Renders deck.html to Parallax-MariaDB.pdf and one PNG per slide, and reports any slide whose content overflows.
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
const here = fileURLToPath(new URL('.', import.meta.url));
const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('file://' + here + 'deck.html'); await p.evaluate(() => document.fonts.ready);
await p.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
const report = await p.evaluate(() => [...document.querySelectorAll('.slide')].map((s, i) => { const r = s.getBoundingClientRect(), foot = s.querySelector('.foot')?.getBoundingClientRect(); let bottom = 0, right = 0, tiny = 0; for (const e of s.querySelectorAll('*:not(.foot):not(.foot *)')) { const x = e.getBoundingClientRect(); if (!x.width) continue; bottom = Math.max(bottom, x.bottom - r.top); right = Math.max(right, x.right - r.left); if (e.children.length === 0 && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 20) tiny++; } return { slide: i + 1, contentBottom: Math.round(bottom), limit: foot ? Math.round(foot.top - r.top) : 1080, right: Math.round(right), tiny, fonts: [...document.fonts].filter(f => f.status === 'loaded').length }; }));
for (const r of report) console.log(JSON.stringify(r), r.contentBottom > r.limit - 8 || r.right > 1920 - 100 ? 'OVERFLOW' : 'ok');
const slides = p.locator('.slide'); for (let i = 0; i < await slides.count(); i++) await slides.nth(i).screenshot({ path: `${here}png/slide-${i + 1}.png` });
await p.pdf({ path: here + 'Parallax-MariaDB.pdf', width: '1920px', height: '1080px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await b.close();
