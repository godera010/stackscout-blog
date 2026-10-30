# Agent guide — StackScout blog

Astro static site. Articles are Markdown in `src/content/posts/`; everything else is generated at build time.
Humans review every change via a pull request (Cloudflare Pages posts a preview URL on the PR). **Never push to `main`.**

## Writing or editing an article
1. `npm run new "Title"` creates `src/content/posts/<slug>.md` as `draft: true`. (Or copy an existing post.)
2. Fill the frontmatter. The schema in `src/content.config.ts` is the source of truth and the build fails if it's violated:
   - `title` (10–120 chars), `description` (50–300 chars), `date` (YYYY-MM-DD), `tags` (1–7)
   - optional: `tldr`, `image` + `imageAlt` (alt is mandatory with an image), `series`, `part`, `updated`, `featured`
   - `draft: true` hides the post from production builds; remove it when the article is ready for review/publish.
3. Body: start headings at `##` (the layout renders the title as the H1). Don't add a TOC, TL;DR box, FAQ boilerplate,
   byline, share buttons, or recommended-reading — the layout generates those.
4. Images: put the file in `src/assets/images/`, reference it with a relative path in frontmatter
   (`image: ../../assets/images/foo.jpg`). Astro resizes and converts to WebP. Don't commit images over ~1 MB.
5. Code blocks: always give a language (` ```ts `). ASCII/box-drawing diagrams use ` ```text `.

## Before opening a PR
```bash
npm run check   # astro check: types + frontmatter validation
npm run build   # must succeed; look for new warnings
```
Open a PR titled `Post: <title>` (or `Fix:`/`Site:` for non-content). In the description list: slug, what changed, any
facts/claims that need a human to verify, and sources used.

## Do not
- Edit `dist/`, `.astro/`, or `package-lock.json` by hand.
- Change URLs of existing posts (the slug is the filename) — they're indexed by Google and in RSS.
- Hardcode the domain; use `SITE_URL` from `src/lib/site.ts`.

## Layout of the repo
- `src/content/posts/` — articles (the only place content lives)
- `src/pages/` — routes: home, `/posts/`, `/posts/<slug>/`, about, 404, `rss.xml`, `sitemap.xml`
- `src/components/`, `src/layouts/` — header, footer, cards, base HTML
- `src/styles/global.css` — design system (light/dark via `data-theme`)
- `src/lib/` — site constants, post helpers, related-article scoring
- `public/` — copied as-is (`_headers`, `robots.txt`)
