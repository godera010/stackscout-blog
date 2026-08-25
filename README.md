# StackScout

Dev infrastructure & automation publication. Ultra-fast, zero-dependency static HTML/CSS with automated article recommendations → Cloudflare Pages ($0).

**Live Site:** [stackscout-blog.pages.dev](https://stackscout-blog.pages.dev)

## Architecture

```
instatic/
├── public-site/         # Git-tracked static site root → Cloudflare Pages
│   ├── _headers         # Cloudflare Pages caching & security headers
│   ├── assets/          # CSS design system (styles.css), theme.js, & diagrams
│   ├── posts/           # Engineering articles & markdown sources
│   ├── about/           # About page
│   ├── index.html       # Homepage (auto-compiled)
│   ├── rss.xml          # Auto-generated RSS 2.0 feed
│   ├── sitemap.xml      # Auto-generated SEO sitemap
│   └── robots.txt
├── scripts/
│   ├── build.py         # Static compiler & recommendation engine
│   └── deploy.sh        # Build, stage, commit & push to GitHub
└── research/            # Technical research & post drafts
```

## Quick Start & Workflow

```bash
# 1. Edit or add markdown articles in public-site/posts/<slug>.md
# 2. Compile site & calculate recommendations:
py scripts/build.py

# 3. Preview locally:
python -m http.server 8080 --directory public-site

# 4. Deploy to Cloudflare Pages (automatically runs build.py before git push):
./scripts/deploy.sh "Publish new engineering article"
```

## Commands

| Action | Command |
|--------|---------|
| Compile site & recommendations | `py scripts/build.py` |
| Deploy site (auto-builds & pushes) | `./scripts/deploy.sh` |
| Deploy w/ message | `./scripts/deploy.sh "Add new blog post"` |
| Local preview | `python -m http.server 8080 --directory public-site` |

## Deployment

**Cloudflare Pages** connected to `godera010/stackscout-blog` (`main` branch).

| Setting | Value |
|---------|-------|
| Repository | `godera010/stackscout-blog` |
| Branch | `main` |
| Build output directory | `public-site` |
| Build command (Optional) | `python scripts/build.py` |

Pushes to `main` auto-deploy globally. Use `./scripts/deploy.sh` to compile, commit, and push changes.

## Stack & Features

- **Frontend:** Semantic HTML5 & Vanilla CSS Design System (Zero JS overhead)
- **Recommendation Engine:** Multi-factor tag & keyword similarity scoring computed at build time
- **SEO & Syndication:** Dynamic XML sitemap, RSS 2.0 feed, JSON-LD `TechArticle` structured data
- **Edge Caching:** Cloudflare Pages custom `_headers` with immutable asset caching
- **Hosting:** Cloudflare Pages (Free global CDN)
- **Repo:** [github.com/godera010/stackscout-blog](https://github.com/godera010/stackscout-blog)
