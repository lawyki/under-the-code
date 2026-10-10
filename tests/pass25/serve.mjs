// Static server for the Pass 25 harness: serves under-the-code/public on
// :8123 with Cloudflare-Pages-like routing.
//   /            -> index.html
//   /part-2      -> part-2.html        (extensionless)
//   /part-2.html -> 308 /part-2        (Pages strips .html)
//   /api/*       -> 404 (tests stub it with page/context.route)
// Run standalone:  node serve.mjs   (PORT and ROOT env vars override)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = process.env.UTC_PUBLIC || new URL('../../public', import.meta.url).pathname;
export const PORT = Number(process.env.PORT || 8123);

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.webmanifest': 'application/manifest+json',
};

function safeJoin(root, p) {
  const full = path.normalize(path.join(root, p));
  return full.startsWith(root) ? full : null;
}

function send(res, status, body, headers = {}) {
  res.writeHead(status, Object.assign({ 'Cache-Control': 'no-store' }, headers));
  res.end(body);
}

export function handler(req, res) {
  let url;
  try { url = new URL(req.url, 'http://localhost'); } catch { return send(res, 400, 'bad url'); }
  let p = decodeURIComponent(url.pathname);
  if (p.startsWith('/api/')) {
    return send(res, 404, JSON.stringify({ error: 'not_stubbed', path: p }),
      { 'Content-Type': 'application/json' });
  }
  if (p.endsWith('.html')) {
    let target = p.slice(0, -5);
    if (target.endsWith('/index')) target = target.slice(0, -5);
    return send(res, 308, '', { Location: (target || '/') + url.search });
  }
  if (p.endsWith('/')) p += 'index';
  let file = safeJoin(ROOT, p);
  if (!file) return send(res, 403, 'forbidden');
  let stat = null;
  try { stat = fs.statSync(file); } catch {}
  if (!stat || stat.isDirectory()) {
    const withHtml = file + '.html';
    try { if (fs.statSync(withHtml).isFile()) { file = withHtml; stat = fs.statSync(file); } } catch {}
  }
  if (!stat || !stat.isFile()) {
    const nf = path.join(ROOT, '404.html');
    return send(res, 404, fs.existsSync(nf) ? fs.readFileSync(nf) : 'not found',
      { 'Content-Type': TYPES['.html'] });
  }
  const type = TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream';
  if (req.method === 'HEAD') return send(res, 200, '', { 'Content-Type': type });
  return send(res, 200, fs.readFileSync(file), { 'Content-Type': type });
}

// Start (or reuse) a server. Resolves to {server|null, port, reused}.
export function startServer(port = PORT) {
  return new Promise((resolve, reject) => {
    const server = http.createServer(handler);
    server.on('error', err => {
      if (err.code === 'EADDRINUSE') {
        // Someone (probably another suite or a standalone serve.mjs) already
        // serves this port. Check it answers like us and reuse it.
        http.get({ host: '127.0.0.1', port, path: '/part-1.html' }, r => {
          r.resume();
          if (r.statusCode === 308) resolve({ server: null, port, reused: true });
          else reject(new Error('port ' + port + ' in use by something else (status ' + r.statusCode + ')'));
        }).on('error', reject);
      } else reject(err);
    });
    server.listen(port, () => resolve({ server, port, reused: false }));
  });
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  startServer().then(({ port, reused }) => {
    console.log((reused ? 'already serving' : 'serving ' + ROOT) + ' on http://localhost:' + port);
  }, e => { console.error(e.message); process.exit(1); });
}
