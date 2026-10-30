import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'posts'>;

/** Drafts show in dev, and in builds with SHOW_DRAFTS=1 (useful for preview deploys). */
const includeDrafts = import.meta.env.DEV || process.env.SHOW_DRAFTS === '1';

/** All publishable posts, newest first. */
export async function getPosts(): Promise<Post[]> {
  const all = await getCollection('posts', ({ data }) => includeDrafts || !data.draft);
  return all.sort((a, b) => {
    const byDate = b.data.date.valueOf() - a.data.date.valueOf();
    return byDate || a.id.localeCompare(b.id);
  });
}

export function readingTime(body = ''): string {
  const words = body.match(/\w+/g)?.length ?? 0;
  return `${Math.max(1, Math.ceil(words / 210))} MIN READ`;
}

export function formatDate(d: Date): string {
  return d
    .toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric', timeZone: 'UTC' })
    .toUpperCase();
}

const words = (s: string) => new Set(s.toLowerCase().match(/\w{4,}/g) ?? []);

/**
 * Build-time "Recommended reading": 12 pts per shared tag + 2 pts per shared 4+ letter
 * word in title/description; ties broken by recency.
 */
export function recommend(target: Post, all: Post[], limit = 2): Post[] {
  const tTags = new Set(target.data.tags.map((t) => t.toLowerCase()));
  const tWords = words(`${target.data.title} ${target.data.description}`);
  return all
    .filter((p) => p.id !== target.id)
    .map((p) => {
      const sharedTags = p.data.tags.filter((t) => tTags.has(t.toLowerCase())).length;
      const cWords = words(`${p.data.title} ${p.data.description}`);
      const sharedWords = [...cWords].filter((w) => tWords.has(w)).length;
      return { p, score: sharedTags * 12 + sharedWords * 2 };
    })
    .sort((a, b) => b.score - a.score || b.p.data.date.valueOf() - a.p.data.date.valueOf())
    .slice(0, limit)
    .map((x) => x.p);
}

export const tagSlug = (t: string) =>
  t.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

/** Map of tag slug -> { name, posts } across all published posts. */
export function groupByTag(posts: Post[]) {
  const map = new Map<string, { name: string; posts: Post[] }>();
  for (const p of posts) {
    for (const t of p.data.tags) {
      const slug = tagSlug(t);
      if (!map.has(slug)) map.set(slug, { name: t, posts: [] });
      map.get(slug)!.posts.push(p);
    }
  }
  return map;
}
