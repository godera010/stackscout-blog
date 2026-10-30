import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getPosts } from '../lib/posts';
import { SITE_TITLE, SITE_TAGLINE, AUTHOR_NAME } from '../lib/site';

export async function GET(context: APIContext) {
  const posts = await getPosts();
  return rss({
    title: SITE_TITLE,
    description: SITE_TAGLINE,
    site: context.site!,
    trailingSlash: true,
    customData: '<language>en-us</language>',
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.description,
      link: `/posts/${p.id}/`,
      pubDate: p.data.date,
      author: AUTHOR_NAME,
    })),
  });
}
