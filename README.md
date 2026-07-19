# StackScout

Dev infrastructure & automation blog. Self-hosted Instatic CMS (Docker) → Static HTML/CSS → Cloudflare Pages ($0).

**Live:** [stackscout-blog.pages.dev](https://stackscout-blog.pages.dev)

## Architecture

```
instatic/
├── instatic-data/       # Docker volume mount (NOT in git)
│   ├── data/cms.db      # Live SQLite database
│   └── uploads/         # Media library assets
├── public-site/         # Git-tracked static output → Cloudflare Pages
│   ├── assets/          # CSS, fonts, scripts
│   ├── posts/           # Generated post pages
│   ├── index.html
│   ├── sitemap.xml
│   └── robots.txt
├── scripts/
│   ├── deploy.sh        # Git commit + push
│   └── backup.sh        # SQLite backup
├── compose.prod.yml     # Base Docker compose
├── compose.sqlite.yml   # SQLite override
└── .mcp.json            # MCP server config
```

## Quick Start

```bash
# 1. Start CMS
docker compose -f compose.prod.yml -f compose.sqlite.yml up -d

# 2. Open admin
open http://localhost:3001/admin

# 3. Edit content, publish, then deploy
./scripts/deploy.sh
```

## Commands

| Action | Command |
|--------|---------|
| Start CMS | `docker compose -f compose.prod.yml -f compose.sqlite.yml up -d` |
| Stop CMS | `docker compose -f compose.prod.yml -f compose.sqlite.yml down` |
| Logs | `docker compose -f compose.prod.yml -f compose.sqlite.yml logs -f` |
| Update | `docker compose -f compose.prod.yml -f compose.sqlite.yml pull && docker compose -f compose.prod.yml -f compose.sqlite.yml up -d` |
| Deploy site | `./scripts/deploy.sh` |
| Deploy w/ message | `./scripts/deploy.sh "Add new blog post"` |
| Backup DB | `./scripts/backup.sh` |

## Deployment

**Cloudflare Pages** connected to `godera010/stackscout-blog` (main branch).

| Setting | Value |
|---------|-------|
| Repository | `godera010/stackscout-blog` |
| Branch | `main` |
| Build output directory | `public-site` |

Pushes to `main` auto-deploy. Use `./scripts/deploy.sh` to commit and push changes.

## Backup

```bash
./scripts/backup.sh
# Creates: backups/cms-YYYY-MM-DD-HHMMSS.db
```

## MCP

`.mcp.json` connects to the running CMS for programmatic content/page management. Open the Site or Content editor in your browser for editing tools to work.

## Stack

- **CMS:** Instatic (Bun, visual editor)
- **Database:** SQLite
- **Output:** Static HTML/CSS
- **Deploy:** Git push → Cloudflare Pages (free)
- **Repo:** [github.com/godera010/stackscout-blog](https://github.com/godera010/stackscout-blog)
