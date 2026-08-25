#!/usr/bin/env python3
"""
StackScout Static Site & Recommendation Engine Compiler
Builds static HTML pages, computes article recommendations, and outputs
homepage, archive, RSS feed, sitemap.xml, and Cloudflare _headers.
"""

import os
import re
import math
import html
import datetime
import urllib.parse

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_DIR = os.path.join(REPO_DIR, "public-site")
POSTS_DIR = os.path.join(PUBLIC_DIR, "posts")
ASSETS_DIR = os.path.join(PUBLIC_DIR, "assets")

SITE_URL = "https://stackscout-blog.pages.dev"
SITE_TITLE = "StackScout"
SITE_TAGLINE = "Dev infrastructure, automation, and deployment deep-dives."
SITE_DESCRIPTION = "Dev infrastructure, automation, and deployment deep-dives."
AUTHOR_NAME = "StackScout Engineering"
GITHUB_URL = "https://github.com/godera010/stackscout-blog"

# Known image diagram pairings for technical deep-dives
IMAGES_MAP = {
    "coding-with-claude-code-in-production": ("claude_code_workflow.jpg", "Claude Code Terminal Agent Workflow Architecture Diagram"),
    "autonomous-aws-ops-agent-mcp": ("aws_mcp_ops_architecture.jpg", "Autonomous AWS Ops Agent with Model Context Protocol Architecture Diagram"),
    "zero-trust-ai-agents-istio-kubernetes": ("zero_trust_istio_k8s.jpg", "Zero Trust AI Agent Security in Istio and Kubernetes Architecture Diagram"),
    "durable-memory-vector-databases": ("durable_memory_architecture.jpg", "Durable Memory and Vector Database Architecture Diagram"),
    "docker-on-windows-wsl2-under-the-hood": ("wsl2_architecture.jpg", "Docker on Windows WSL2 Kernel and MicroVM Architecture Diagram"),
    "instatic-cms-complete-guide": ("instatic_architecture.jpg", "Instatic CMS Bun Architecture and Static Compiler Diagram"),
}

# Standard curated tags for posts if missing in frontmatter
DEFAULT_TAGS_MAP = {
    "coding-with-claude-code-in-production": ["AI", "Developer Tools", "Claude Code", "Workflow"],
    "autonomous-aws-ops-agent-mcp": ["AWS", "Cloud", "MCP", "Automation"],
    "zero-trust-ai-agents-istio-kubernetes": ["Kubernetes", "Istio", "Security", "AI"],
    "preventing-rag-api-hallucinations": ["RAG", "LLM", "APIs", "Data Integrity"],
    "file-based-multi-agent-state-machine": ["AI Agents", "Architecture", "State Machines", "Orchestration"],
    "saturating-gigabit-fiber-rust-tauri-nexdm": ["Rust", "Tauri", "Networking", "Performance"],
    "react-datagrid-virtualization-space-explorer": ["React", "Performance", "Frontend", "Virtualization"],
    "vectorized-payment-aging-pipeline-python": ["Python", "Polars", "Data Engineering", "Performance"],
    "streaming-io-lessons-from-acm-icpc": ["Performance", "I/O", "Algorithms", "Systems"],
    "contract-testing-least-derived-evidence": ["Microservices", "Testing", "API", "Architecture"],
    "ai-evaluation-harness-benchmark-provenance": ["AI", "Evaluation", "Benchmarks", "Testing"],
    "essential-books-for-ai-systems-engineers": ["AI Engineering", "Architecture", "Books", "Career"],
    "engineering-culture-psychological-safety-humor": ["Culture", "Engineering Leadership", "DevOps", "Teamwork"],
    "durable-memory-vector-databases": ["AI", "Vector Databases", "Memory", "LLM"],
    "docker-on-windows-wsl2-under-the-hood": ["Docker", "WSL 2", "Linux", "Virtualization"],
    "instatic-cms-complete-guide": ["CMS", "Jamstack", "Bun", "Static Site", "Architecture"]
}

def parse_frontmatter(content):
    """Extract YAML frontmatter and body from markdown content."""
    meta = {}
    body = content
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        body = content[fm_match.end():]
        
        current_list_key = None
        for line in fm_text.splitlines():
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            
            # List item continuation
            if line.startswith("  - ") and current_list_key:
                val = line[4:].strip().strip('"\'')
                meta[current_list_key].append(val)
                continue
            
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                
                if val == "":
                    meta[key] = []
                    current_list_key = key
                elif val.startswith("[") and val.endswith("]"):
                    items = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                    meta[key] = items
                    current_list_key = None
                elif val.lower() == "true":
                    meta[key] = True
                    current_list_key = None
                elif val.lower() == "false":
                    meta[key] = False
                    current_list_key = None
                else:
                    meta[key] = val.strip('"\'')
                    current_list_key = None
    return meta, body.strip()

def calculate_read_time(body_text):
    """Estimate read time in minutes from word count."""
    words = len(re.findall(r"\w+", body_text))
    minutes = max(1, math.ceil(words / 210))
    return f"{minutes} MIN READ"

def format_display_date(date_str):
    """Format YYYY-MM-DD or existing string into AUG 25, 2026 format."""
    if not date_str:
        return "AUG 25, 2026"
    try:
        if len(date_str) == 10 and date_str[4] == "-" and date_str[7] == "-":
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%b %d, %Y").upper()
    except Exception:
        pass
    return str(date_str).upper()

def slugify(text):
    """Convert text into a URL/anchor slug."""
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text)

def markdown_to_html(md_text, images_map_entry=None):
    """Convert markdown content to HTML with TOC and diagrams."""
    # Extract TL;DR
    tldr_match = re.search(r"> \*\*TL;DR:\*\*\s*(.*?)(?=\n\n|\n##|$)", md_text, re.DOTALL)
    if not tldr_match:
        tldr_match = re.search(r"\*\*TL;DR\*\*\s*\n(.*?)(?=\n\n|\n##|$)", md_text, re.DOTALL)
    
    tldr_text = ""
    clean_body = md_text
    if tldr_match:
        tldr_text = tldr_match.group(1).strip()
        clean_body = clean_body.replace(tldr_match.group(0), "").strip()

    # Remove H1 if first line
    clean_body = re.sub(r"^#\s+.*\n*", "", clean_body).strip()

    # Image diagram figure
    img_html = ""
    if images_map_entry:
        img_file, img_alt = images_map_entry
        img_html = f'''
      <figure>
        <picture>
          <img src="/assets/images/{img_file}" alt="{html.escape(img_alt)}" loading="lazy" decoding="async" width="1200" height="630">
        </picture>
        <figcaption>Figure 1: {html.escape(img_alt)}.</figcaption>
      </figure>'''

    # Extract H2s for TOC
    h2_matches = re.findall(r"^##\s+(.*)", clean_body, re.MULTILINE)
    toc_items = []
    for idx, h2 in enumerate(h2_matches, 1):
        anchor = slugify(h2)
        toc_items.append(f'<li><a href="#{anchor}">{idx}. {html.escape(h2)}</a></li>')

    toc_html = f'''
      <div class="toc">
        <div class="toc-title">Contents</div>
        <ol>
          {''.join(toc_items)}
        </ol>
      </div>''' if toc_items else ""

    # Replace Code Blocks
    def code_block_repl(m):
        lang = m.group(1) or ""
        code_content = html.escape(m.group(2).strip("\n"))
        is_diagram = lang.lower() in ["text", "ascii"] or any(c in code_content for c in ["┌", "│", "└", "─", "+--", "|"])
        cls = "diagram" if is_diagram else f"lang-{lang}" if lang else ""
        return f'<pre class="{cls}"><code>{code_content}</code></pre>'

    html_body = re.sub(r"```(\w*)\n(.*?)```", code_block_repl, clean_body, flags=re.DOTALL)

    # Replace Headings
    def h4_repl(m):
        txt = m.group(1).strip()
        return f'<h4 id="{slugify(txt)}">{txt}</h4>'
    html_body = re.sub(r"^####\s+(.*)", h4_repl, html_body, flags=re.MULTILINE)

    def h3_repl(m):
        txt = m.group(1).strip()
        return f'<h3 id="{slugify(txt)}">{txt}</h3>'
    html_body = re.sub(r"^###\s+(.*)", h3_repl, html_body, flags=re.MULTILINE)

    def h2_repl(m):
        txt = m.group(1).strip()
        return f'<h2 id="{slugify(txt)}">{txt}</h2>'
    html_body = re.sub(r"^##\s+(.*)", h2_repl, html_body, flags=re.MULTILINE)

    # Horizontal rules
    html_body = re.sub(r"^---+$", "<hr>", html_body, flags=re.MULTILINE)

    # Unordered Lists
    html_body = re.sub(r"^\s*-\s+(.*)", r"<li>\1</li>", html_body, flags=re.MULTILINE)
    html_body = re.sub(r"((?:<li>.*</li>\n?)+)", r"<ul>\1</ul>", html_body)

    # Blockquotes
    html_body = re.sub(r"^>\s+(.*)", r"<blockquote><p>\1</p></blockquote>", html_body, flags=re.MULTILINE)

    # Bold, Italic, Inline Code, Links
    html_body = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html_body)
    html_body = re.sub(r"\*([^\*]+)\*", r"<em>\1</em>", html_body)
    html_body = re.sub(r"`([^`]+)`", r"<code>\1</code>", html_body)
    html_body = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', html_body)

    # Paragraph wrap
    paragraphs = html_body.split("\n\n")
    processed_p = []
    for p in paragraphs:
        p_str = p.strip()
        if not p_str:
            continue
        if (p_str.startswith("<h") or p_str.startswith("<pre") or p_str.startswith("<ul") or 
            p_str.startswith("<ol") or p_str.startswith("<blockquote") or p_str.startswith("<figure") or 
            p_str.startswith("<div") or p_str.startswith("<hr")):
            processed_p.append(p_str)
        else:
            processed_p.append(f"<p>{p_str}</p>")
    final_body_html = "\n\n".join(processed_p)

    return tldr_text, toc_html, img_html, final_body_html

def compute_recommendations(target_post, all_posts, limit=2):
    """
    Intelligently calculate the top recommended articles for target_post.
    Scores candidates based on:
    - Shared tags (high weight)
    - Keyword overlap in title & description (moderate weight)
    - Recency / proximity
    """
    target_tags = set(t.lower() for t in target_post["tags"])
    target_text = (target_post["title"] + " " + target_post["description"]).lower()
    target_words = set(re.findall(r"\w{4,}", target_text))

    scored = []
    for candidate in all_posts:
        if candidate["slug"] == target_post["slug"]:
            continue
        
        cand_tags = set(t.lower() for t in candidate["tags"])
        cand_text = (candidate["title"] + " " + candidate["description"]).lower()
        cand_words = set(re.findall(r"\w{4,}", cand_text))

        # Tag overlap score (12 points per shared tag)
        shared_tags = target_tags.intersection(cand_tags)
        tag_score = len(shared_tags) * 12

        # Keyword overlap score (2 points per shared 4+ letter word)
        shared_words = target_words.intersection(cand_words)
        keyword_score = len(shared_words) * 2

        total_score = tag_score + keyword_score
        scored.append((total_score, candidate))

    # Sort descending by score, tie-breaking by date
    scored.sort(key=lambda x: (x[0], x[1]["date_raw"]), reverse=True)
    return [item[1] for item in scored[:limit]]

def get_shared_header(active_nav=""):
    posts_active = ' class="active"' if active_nav == "posts" else ""
    about_active = ' class="active"' if active_nav == "about" else ""
    
    return f'''  <header>
    <div class="header-container">
      <div class="header-top">
        <a href="/" class="logo">StackScout</a>
        <div class="nav-right">
          <a href="/posts/"{posts_active}>Posts</a>
          <a href="/about/"{about_active}>About</a>
          <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" title="Toggle dark/light mode">
            <svg class="icon-sun" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>
            <svg class="icon-moon" viewBox="0 0 24 24"><path d="M12.3 2a10 10 0 0 0-1.9 20 10 10 0 0 0 9.2-6.2 1 1 0 0 0-1-1.3 8 8 0 1 1-7.6-11.5 1 1 0 0 0-1.3-1z"/></svg>
          </button>
        </div>
      </div>
      <div class="header-tagline">
        {SITE_TAGLINE}
      </div>
    </div>
  </header>'''

def get_shared_footer():
    return f'''  <footer>
    <div>&copy; {datetime.date.today().year} StackScout</div>
    <div class="footer-links">
      <a href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub</a>
      <span>·</span>
      <a href="/rss.xml">RSS</a>
      <span>·</span>
      <a href="/sitemap.xml">Sitemap</a>
    </div>
  </footer>'''

def get_head_tags(title, description, canonical_path="/", og_type="website"):
    escaped_title = html.escape(title)
    escaped_desc = html.escape(description)
    canonical_url = f"{SITE_URL}{canonical_path}"
    
    return f'''  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escaped_title}</title>
  <meta name="description" content="{escaped_desc}">
  
  <!-- Preconnect & Asynchronous Font Loading (Zero Render-Blocking) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400..800;1,400..800&family=JetBrains+Mono:ital,wght@0,400..600;1,400..600&display=swap">
  
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{escaped_title}">
  <meta property="og:description" content="{escaped_desc}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="StackScout">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escaped_title}">
  <meta name="twitter:description" content="{escaped_desc}">
  
  <link rel="alternate" type="application/rss+xml" title="StackScout RSS Feed" href="{SITE_URL}/rss.xml">
  <script src="/assets/theme.js"></script>
  <link rel="stylesheet" href="/assets/styles.css">'''

def generate_post_page(post, recommendations):
    """Generate individual article HTML page with recommendations & JSON-LD."""
    slug = post["slug"]
    title = post["title"]
    desc = post["description"]
    display_date = post["display_date"]
    read_time = post["read_time"]
    canonical_path = f"/posts/{slug}/"
    full_url = f"{SITE_URL}{canonical_path}"

    # Generate Recommendations Grid HTML
    rec_cards = []
    for rec in recommendations:
        rec_tags = " · ".join(rec["tags"][:2])
        rec_cards.append(f'''        <a href="/posts/{rec["slug"]}/" class="recommended-card">
          <div class="meta-line">{rec_tags.upper()} &nbsp;·&nbsp; {rec["read_time"]}</div>
          <h3>{html.escape(rec["title"])}</h3>
          <p>{html.escape(rec["description"])}</p>
          <span class="read-link">Read article &rarr;</span>
        </a>''')

    recommendations_html = f'''
      <section class="recommended-section">
        <div class="section-label">RECOMMENDED READING</div>
        <div class="recommended-grid">
{chr(10).join(rec_cards)}
        </div>
      </section>''' if rec_cards else ""

    # Standard FAQ Block
    faq_html = '''
      <h2 id="faq">Frequently Asked Questions (FAQ)</h2>
      <div class="faq-list">
        <h3>What is the core takeaway of this guide?</h3>
        <p>This guide establishes production patterns and verifiable architecture standards designed to eliminate engineering friction, improve reliability, and optimize system performance.</p>
        <h3>How can teams implement these patterns safely?</h3>
        <p>Start by auditing your current pipeline, applying clear boundaries, enforcing verification commands on disk, and introducing automated checks gradually.</p>
        <h3>Where can I find additional technical reference code?</h3>
        <p>Check the StackScout open-source repository on GitHub for full runnable code samples, architecture benchmarks, and continuous deployment configurations.</p>
      </div>'''

    tldr_html = f'''
      <blockquote>
        <p><strong>TL;DR:</strong> {html.escape(post["tldr"])}</p>
      </blockquote>''' if post["tldr"] else ""

    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(full_url)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{get_head_tags(f"{title} — StackScout", desc, canonical_path, "article")}
</head>
<body>
{get_shared_header("posts")}

  <main>
    <article>
      <header>
        <h1>{html.escape(title)}</h1>
        <div class="subtitle">{html.escape(desc)}</div>
        <div class="meta">{display_date} &nbsp;·&nbsp; {read_time} &nbsp;·&nbsp; BY {AUTHOR_NAME}</div>
      </header>

{tldr_html}
{post["toc_html"]}
{post["img_html"]}

{post["body_html"]}

{faq_html}

{recommendations_html}

      <div class="article-share">
        <span class="share-label">Share Article</span>
        <div class="share-buttons">
          <a href="https://x.com/intent/post?text={encoded_title}&url={encoded_url}" target="_blank" rel="noopener" class="share-btn">X (Twitter)</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}" target="_blank" rel="noopener" class="share-btn">LinkedIn</a>
          <a href="https://news.ycombinator.com/submitlink?u={encoded_url}&t={encoded_title}" target="_blank" rel="noopener" class="share-btn">Hacker News</a>
          <button class="share-btn copy-link-btn" onclick="copyArticleLink(this)">Copy Link</button>
        </div>
      </div>
    </article>
  </main>

{get_shared_footer()}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{html.escape(title)}",
    "description": "{html.escape(desc)}",
    "url": "{full_url}",
    "datePublished": "{post['date_raw']}",
    "dateModified": "{post['date_raw']}",
    "author": {{
      "@type": "Organization",
      "name": "{AUTHOR_NAME}",
      "url": "{SITE_URL}"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "StackScout",
      "url": "{SITE_URL}"
    }}
  }}
  </script>
</body>
</html>'''
    
    post_dir = os.path.join(POSTS_DIR, slug)
    os.makedirs(post_dir, exist_ok=True)
    out_file = os.path.join(post_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_post_card(post, is_featured=False):
    slug = post["slug"]
    title = html.escape(post["title"])
    desc = html.escape(post["description"])
    display_date = post["display_date"]
    read_time = post["read_time"]
    tags_html = " <span>·</span> ".join(post["tags"])
    featured_cls = " featured" if is_featured else ""
    full_url = f"{SITE_URL}/posts/{slug}/"

    return f'''      <!-- Article -->
      <div class="post-item{featured_cls}">
        <div class="meta-line">{display_date} &nbsp;·&nbsp; {read_time}</div>
        <h2><a href="/posts/{slug}/">{title}</a></h2>
        <p>{desc}</p>
        <div class="post-tags">{tags_html}</div>
        <div class="post-actions">
          <a href="/posts/{slug}/" class="read-more">Read article &rarr;</a>
          <button class="share-card-btn" onclick="shareCard(event, '{full_url}', '{title.replace("'", "\\'")}')" title="Share article">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
            Share
          </button>
        </div>
      </div>'''

def generate_homepage(posts):
    """Generate public-site/index.html."""
    cards = []
    for idx, post in enumerate(posts):
        cards.append(generate_post_card(post, is_featured=(idx == 0)))

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{get_head_tags(f"{SITE_TITLE} — Dev Infrastructure & Automation", SITE_DESCRIPTION, "/", "website")}
</head>
<body>
{get_shared_header("")}

  <main>
    <div class="section-label">LATEST &amp; ARCHIVE</div>

    <div class="post-list">
{chr(10).join(cards)}
    </div>
  </main>

{get_shared_footer()}
</body>
</html>'''

    out_file = os.path.join(PUBLIC_DIR, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_archive_page(posts):
    """Generate public-site/posts/index.html."""
    cards = []
    for post in posts:
        cards.append(generate_post_card(post, is_featured=False))

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{get_head_tags("All Posts — StackScout", f"All {len(posts)} dev infrastructure, automation, and deployment deep-dives on StackScout.", "/posts/", "website")}
</head>
<body>
{get_shared_header("posts")}

  <main>
    <div class="section-label">ALL ARTICLES ({len(posts)})</div>

    <div class="post-list">
{chr(10).join(cards)}
    </div>
  </main>

{get_shared_footer()}
</body>
</html>'''

    out_file = os.path.join(POSTS_DIR, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_about_page():
    """Generate public-site/about/index.html."""
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{get_head_tags("About — StackScout", "About StackScout — Practical engineering guides for the stack behind modern software.", "/about/", "website")}
</head>
<body>
{get_shared_header("about")}

  <main>
    <article>
      <header>
        <h1>About StackScout</h1>
        <div class="subtitle">Practical engineering deep dives into the tools and infrastructure behind modern software.</div>
      </header>

      <h2>Editorial Mission</h2>
      <p>StackScout exists to demystify developer infrastructure, container ecosystems, deployment pipelines, and automation tooling. Rather than writing surface-level installation tutorials, we focus on explaining <strong>what actually happens under the hood</strong>.</p>

      <p>Our core content pillars include:</p>
      <ul>
        <li><strong>Containers &amp; Virtualization:</strong> WSL 2, Docker Engine, Podman, cgroups, kernel namespaces, and OCI runtimes.</li>
        <li><strong>DevOps &amp; Automation:</strong> CI/CD workflows, local development orchestration, and Infrastructure as Code.</li>
        <li><strong>Cloud &amp; Networking:</strong> Reverse proxies (Nginx, Traefik, Caddy), DNS, TLS termination, and static hosting platforms.</li>
        <li><strong>Self-Hosted Systems:</strong> Lightweight tools, SQLite operational patterns, and containerized dev environments.</li>
      </ul>

      <h2>Architecture &amp; Tech Stack</h2>
      <p>StackScout is built using a clean, zero-dependency static stack:</p>
      <ul>
        <li><strong>Frontend:</strong> Native semantic HTML5 and vanilla CSS design system.</li>
        <li><strong>Source Code:</strong> Git-tracked Markdown source files for engineering articles.</li>
        <li><strong>Performance:</strong> Zero client-side JavaScript frameworks or dynamic server overhead.</li>
        <li><strong>Hosting &amp; CD:</strong> Automated global static deployment via Git push to Cloudflare Pages.</li>
      </ul>

      <h2>Open Source &amp; Repository</h2>
      <p>The code, templates, and engineering articles for StackScout are open source and available on GitHub:</p>
      <p><a href="{GITHUB_URL}" target="_blank" rel="noopener">{GITHUB_URL.replace('https://', '')} &rarr;</a></p>
    </article>
  </main>

{get_shared_footer()}
</body>
</html>'''

    about_dir = os.path.join(PUBLIC_DIR, "about")
    os.makedirs(about_dir, exist_ok=True)
    out_file = os.path.join(about_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_sitemap(posts):
    """Generate valid sitemap.xml."""
    today = datetime.date.today().isoformat()
    urls = [
        f'  <url>\n    <loc>{SITE_URL}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>',
        f'  <url>\n    <loc>{SITE_URL}/posts/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>',
        f'  <url>\n    <loc>{SITE_URL}/about/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>',
    ]
    for post in posts:
        urls.append(f'  <url>\n    <loc>{SITE_URL}/posts/{post["slug"]}/</loc>\n    <lastmod>{post["date_raw"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>')

    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

    out_file = os.path.join(PUBLIC_DIR, "sitemap.xml")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(xml_content)

def generate_rss_feed(posts):
    """Generate valid RSS 2.0 XML feed."""
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    items = []
    for post in posts:
        try:
            pub_dt = datetime.datetime.strptime(post["date_raw"], "%Y-%m-%d")
            pub_rfc822 = pub_dt.strftime("%a, %d %b %Y 00:00:00 GMT")
        except Exception:
            pub_rfc822 = now_rfc822

        post_url = f"{SITE_URL}/posts/{post['slug']}/"
        items.append(f'''    <item>
      <title>{html.escape(post["title"])}</title>
      <link>{post_url}</link>
      <guid isPermaLink="true">{post_url}</guid>
      <description>{html.escape(post["description"])}</description>
      <pubDate>{pub_rfc822}</pubDate>
      <author>{AUTHOR_NAME}</author>
    </item>''')

    rss_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}/</link>
    <description>{SITE_DESCRIPTION}</description>
    <language>en-us</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>'''

    out_file = os.path.join(PUBLIC_DIR, "rss.xml")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(rss_content)

def generate_cloudflare_headers():
    """Generate Cloudflare Pages _headers configuration."""
    headers_content = """# Cloudflare Pages Caching & Security Headers

/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: interest-cohort=()

# Immutable caching for static assets
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# Fresh delivery for HTML and feeds
/*.html
  Cache-Control: public, max-age=0, must-revalidate
/sitemap.xml
  Cache-Control: public, max-age=3600, must-revalidate
/rss.xml
  Cache-Control: public, max-age=3600, must-revalidate
"""
    out_file = os.path.join(PUBLIC_DIR, "_headers")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(headers_content)

def build_all():
    print("=" * 60)
    print("  StackScout Static Site & Recommendation Engine Compiler")
    print("=" * 60)

    # 1. Discover all markdown post files
    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]
    print(f"Found {len(md_files)} markdown posts in {POSTS_DIR}")

    posts = []
    for md_file in md_files:
        slug = md_file.replace(".md", "")
        file_path = os.path.join(POSTS_DIR, md_file)
        
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        meta, body = parse_frontmatter(raw_content)

        title = meta.get("title") or slug.replace("-", " ").title()
        description = meta.get("description") or meta.get("metaDescription") or "Technical deep dive on software engineering."
        date_raw = meta.get("datePublished") or meta.get("date") or "2026-08-25"
        display_date = format_display_date(date_raw)
        
        # Tags normalization
        raw_tags = meta.get("tags")
        if isinstance(raw_tags, list):
            tags = raw_tags
        elif isinstance(raw_tags, str):
            tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
        else:
            tags = DEFAULT_TAGS_MAP.get(slug, ["Engineering", "Architecture"])

        # Read time
        read_time = meta.get("readTime") or meta.get("read_time") or calculate_read_time(body)
        
        img_entry = IMAGES_MAP.get(slug)
        tldr_text, toc_html, img_html, body_html = markdown_to_html(body, img_entry)

        if not tldr_text and description:
            tldr_text = description

        post_obj = {
            "slug": slug,
            "title": title,
            "description": description,
            "date_raw": date_raw,
            "display_date": display_date,
            "tags": tags,
            "read_time": read_time,
            "tldr": tldr_text,
            "toc_html": toc_html,
            "img_html": img_html,
            "body_html": body_html,
            "meta": meta
        }
        posts.append(post_obj)

    # Sort posts by date descending
    posts.sort(key=lambda p: p["date_raw"], reverse=True)

    # 2. Generate individual article pages with recommendations
    print(f"Generating {len(posts)} article pages with recommendation graphs...")
    for post in posts:
        recs = compute_recommendations(post, posts, limit=2)
        generate_post_page(post, recs)

    # 3. Generate homepage & archives
    print("Generating homepage (index.html)...")
    generate_homepage(posts)

    print("Generating archive (posts/index.html)...")
    generate_archive_page(posts)

    print("Generating about page (about/index.html)...")
    generate_about_page()

    # 4. Generate SEO Feeds & Cloudflare Headers
    print("Generating sitemap.xml & rss.xml...")
    generate_sitemap(posts)
    generate_rss_feed(posts)

    print("Generating Cloudflare _headers...")
    generate_cloudflare_headers()

    print("=" * 60)
    print(f"  Build complete! {len(posts)} articles compiled successfully.")
    print("=" * 60)

if __name__ == "__main__":
    build_all()
