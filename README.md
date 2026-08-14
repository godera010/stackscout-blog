# StackScout

Dev infrastructure & automation publication. Ultra-fast, zero-dependency static HTML/CSS → Cloudflare Pages ($0).

**Live Site:** [stackscout-blog.pages.dev](https://stackscout-blog.pages.dev)

## Architecture

```
instatic/
├── public-site/         # Git-tracked static site root → Cloudflare Pages
│   ├── assets/          # CSS design system (styles.css)
│   ├── posts/           # Engineering articles & markdown sources
│   ├── about/           # About page
│   ├── index.html       # Homepage
│   ├── sitemap.xml      # SEO sitemap
│   └── robots.txt
├── scripts/
│   └── deploy.sh        # Stage, commit & push to GitHub
└── research/            # Technical research & post drafts
```

## Quick Start & Workflow

```bash
# 1. Edit or add articles in public-site/posts/
# 2. Preview locally using VS Code Live Server or python -m http.server
# 3. Deploy to Cloudflare Pages:
./scripts/deploy.sh "Publish new engineering article"
```

## Commands

| Action | Command |
|--------|---------|
| Deploy site | `./scripts/deploy.sh` |
| Deploy w/ message | `./scripts/deploy.sh "Add new blog post"` |
| Local preview | `python -m http.server 8080 --directory public-site` |

## Deployment

**Cloudflare Pages** connected to `godera010/stackscout-blog` (`main` branch).

| Setting | Value |
|---------|-------|
| Repository | `godera010/stackscout-blog` |
| Branch | `main` |
| Build output directory | `public-site` |

Pushes to `main` auto-deploy globally. Use `./scripts/deploy.sh` to commit and push changes.

## Stack

- **Frontend:** Semantic HTML5 & Vanilla CSS Design System
- **Output:** Pure static HTML/CSS (Zero JS overhead)
- **Hosting:** Cloudflare Pages (Free global CDN)
- **Repo:** [github.com/godera010/stackscout-blog](https://github.com/godera010/stackscout-blog)
