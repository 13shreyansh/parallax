// A fixed authenticated HTTPS bridge to the hosted service. Never a Mac/tunnel fallback.
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const read = new Set(['health', 'home', 'article', 'search', 'method', 'examples']);
  const write = new Set(['review', 'copied']);
  const mode = typeof req.query.mode === 'string' ? req.query.mode : 'home';
  if (!(req.method === 'GET' && read.has(mode)) && !(req.method === 'POST' && write.has(mode))) return res.status(405).json({ error: 'This action is not available.' });
  const origin = process.env.PARALLAX_API_ORIGIN;
  if (!origin || !origin.startsWith('https://') || !process.env.PARALLAX_BRIDGE_TOKEN) return res.status(503).json({ error: 'The database did not answer. Try again in a moment.' });
  try {
    const url = new URL(`/${mode}`, origin);
    for (const key of ['theme', 'sort', 'qid', 'flag', 'asof', 'q', 'claim', 'all']) if (typeof req.query[key] === 'string' && req.query[key].length <= 300) url.searchParams.set(key, req.query[key]);
    const headers = { Accept: 'application/json', 'X-Parallax-Token': process.env.PARALLAX_BRIDGE_TOKEN, 'X-Parallax-Client': String(req.headers['x-forwarded-for'] || '').split(',')[0] };
    const options = { method: req.method, headers, signal: AbortSignal.timeout(55000) };
    if (req.method === 'POST') { headers['Content-Type'] = 'application/json'; options.body = JSON.stringify(req.body); }
    const response = await fetch(url, options);
    return res.status(response.status).json(await response.json());
  } catch { return res.status(503).json({ error: 'The database did not answer. Try again in a moment.' }); }
}
