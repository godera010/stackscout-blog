// Hand-rolled (instead of @astrojs/sitemap) so the URL stays /sitemap.xml,
// which is what Google Search Console already has on file.
import { getPosts } from '../lib/posts';
import { SITE_URL } from '../lib/site';

const iso = (d: Date) => d.toISOString().slice(0, 10);

export async function GET() {
  const posts = await getPosts();
  const newest = posts[0]?.data.date ?? new Date();
  const entries = [
    { loc: '/', lastmod: newest, freq: 'daily', priority: '1.0' },
    { loc: '/posts/', lastmod: newest, freq: 'daily', priority: '0.9' },
    { loc: '/about/', lastmod: newest, freq: 'monthly', priority: '0.5' },
    ...posts.map((p) => ({
      loc: `/posts/${p.id}/`,
      lastmod: p.data.updated ?? p.data.date,
      freq: 'monthly',
      priority: '0.8',
    })),
  ];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${entries
  .map((e) => `  <url>\n    <loc>${SITE_URL}${e.loc}</loc>\n    <lastmod>${iso(e.lastmod)}</lastmod>\n    <changefreq>${e.freq}</changefreq>\n    <priority>${e.priority}</priority>\n  </url>`)
  .join('\n')}
</urlset>
`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
