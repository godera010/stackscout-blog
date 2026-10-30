# StackScout

Dev infrastructure & automation publication, built with [Astro](https://astro.build) and hosted on Cloudflare Pages.
Live: <https://stackscout.blog>

## Publishing workflow

```bash
npm install                    # once
npm run new "My post title"    # scaffolds src/content/posts/my-post-title.md as a draft
npm run dev                    # live preview at http://localhost:4321 (drafts visible)
npm run check && npm run build # validate frontmatter + types, build site + search index
npm run check:links            # fail on broken internal links (also runs in CI)
```

1. Create a branch, write/edit the Markdown in `src/content/posts/`, drop images in `src/assets/images/`.
2. Push the branch and open a pull request. Cloudflare Pages builds a **preview URL** and CI runs `check` + `build`.
3. Review the preview. Merge to `main` to deploy to production. That's it, with no scripts or generated HTML to commit.

AI agents follow the same flow (see [AGENTS.md](./AGENTS.md)): they open a PR, you review the preview, you merge.

### Frontmatter

```yaml
---
title: "Post title"
description: "50-300 chars; used for SEO, RSS and cards."
date: 2026-10-30
tags: ["AI", "Architecture"]
tldr: "Optional summary box."
image: ../../assets/images/diagram.jpg   # optional
imageAlt: "Required if image is set"
draft: true                               # remove to publish
---
```

The schema lives in `src/content.config.ts`; a bad post fails the build with a precise error.

## What's generated automatically

Article pages, home and archive pages, table of contents, reading time, related-article recommendations,
tag pages (`/tags/`), full-text search (`/search/`, Pagefind, built by `npm run build`), RSS (`/rss.xml`), sitemap (`/sitemap.xml`), JSON-LD, Open Graph images, responsive WebP images, syntax highlighting.

## Deployment (Cloudflare Pages)

| Setting | Value |
|---|---|
| Production branch | `main` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Env var `NODE_VERSION` | `22` |
| Preview env var (optional) | `SHOW_DRAFTS=1` to show drafts on preview deploys |

Branch/PR previews are enabled by default under *Settings → Builds → Branch control*.

## Structure

```
src/content/posts/   articles (Markdown)
src/assets/images/   article images (optimized at build)
src/pages/           routes (home, posts, about, 404, rss, sitemap)
src/components/ src/layouts/ src/styles/ src/lib/
public/              _headers, robots.txt
```
