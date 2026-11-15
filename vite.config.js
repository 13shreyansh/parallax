import { defineConfig } from 'vite';
export default defineConfig({
  publicDir: 'public-parallax',
  plugins: [{name:'build-provenance',transformIndexHtml(html){return html.replace('<head>',`<head><meta name="parallax-commit" content="${process.env.VITE_PARALLAX_COMMIT || 'development'}">`);}}],
  // PARALLAX_DEV_API points the dev server at a hosted API instead of a local one.
  server: process.env.PARALLAX_DEV_API ? { proxy: { '/api/parallax': { target: process.env.PARALLAX_DEV_API, changeOrigin: true } } } : { proxy: { '/api/parallax': { target: 'http://127.0.0.1:18808', rewrite: (path) => { const u = new URL(path, 'http://local'); const mode = u.searchParams.get('mode') || 'home'; u.searchParams.delete('mode'); return `/${mode}?${u.searchParams}`; } } } },
});
