#!/usr/bin/env node
// Fails if any internal link or asset in dist/ points to a file that doesn't exist.
// Usage: npm run build && npm run check:links
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const DIST = 'dist';
const htmlFiles = [];
(function walk(d) {
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    statSync(p).isDirectory() ? walk(p) : extname(p) === '.html' && htmlFiles.push(p);
  }
})(DIST);

const resolves = (url) => {
  const path = decodeURIComponent(url.split('#')[0].split('?')[0]);
  if (!path) return true;
  const base = join(DIST, path);
  return existsSync(base) && (!statSync(base).isDirectory() || existsSync(join(base, 'index.html')));
};

const bad = [];
for (const file of htmlFiles) {
  const html = readFileSync(file, 'utf8');
  const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));
  for (const [, attr, url] of html.matchAll(/\s(href|src)="([^"]*)"/g)) {
    if (/^(https?:|mailto:|tel:|data:|javascript:|\/\/)/.test(url) || url === '') continue;
    if (url.startsWith('#')) { if (url.length > 1 && !ids.has(url.slice(1))) bad.push(`${file}: missing anchor ${url}`); continue; }
    if (!url.startsWith('/')) continue;
    if (!resolves(url)) bad.push(`${file}: broken ${attr} ${url}`);
  }
}
if (bad.length) { console.error(bad.join('\n')); console.error(`\n${bad.length} broken link(s)`); process.exit(1); }
console.log(`Checked ${htmlFiles.length} pages: all internal links OK`);
