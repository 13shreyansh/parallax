import { defineConfig } from 'vite';
export default defineConfig({
  publicDir: 'public-parallax',
  plugins: [{name:'build-provenance',transformIndexHtml(html){return html.replace('<head>',`<head><meta name="parallax-commit" content="${process.env.VITE_PARALLAX_COMMIT || 'development'}">`);}}],
  server: { proxy: { '/api/parallax': { target: 'http://127.0.0.1:18808', rewrite: (path) => { const u = new URL(path, 'http://local'); const mode = u.searchParams.get('mode') || 'home'; u.searchParams.delete('mode'); return `/${mode}?${u.searchParams}`; } } } },
});
