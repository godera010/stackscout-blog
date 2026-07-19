# Instatic Blog Ecosystem

Self-hosted visual CMS (Docker) → Static HTML/CSS → Git push → Live on Vercel/Cloudflare ($0).

## Directory Structure

```
instatic/
├── .github/workflows/   # Future CI/CD
├── instatic-data/       # Docker volume mount (NOT in git)
│   ├── data/cms.db      # Live SQLite database
│   └── uploads/         # Media library assets
├── public-site/         # Git-tracked static output (deploys to hosting)
│   ├── .git/
│   ├── assets/          # CSS, fonts, scripts
│   ├── posts/           # Generated post pages
│   ├── index.html
│   ├── sitemap.xml
│   └── robots.txt
├── scripts/
│   └── deploy.sh        # One-command deploy
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

# 3. Create content via CMS UI, then deploy
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

## Deployment Setup

1. Create a GitHub repo for your static site
2. In `public-site/`, add the remote:
   ```bash
   cd public-site
   git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
   ```
3. Connect the repo to Vercel or Cloudflare Pages
4. Run `./scripts/deploy.sh` after every publish

## Backup

SQLite database backup:
```bash
./scripts/backup.sh
# Creates: backups/cms-YYYY-MM-DD-HHMMSS.db
```

## MCP Integration

The `.mcp.json` connects to the running CMS instance for programmatic content/page management. Open the Site or Content editor in your browser for editing tools to work.

## Stack

- **CMS:** Instatic (Bun, visual editor)
- **Database:** SQLite (file-based, zero-config)
- **Output:** Static HTML/CSS
- **Deploy:** Git push → Vercel/Cloudflare (free tier)
