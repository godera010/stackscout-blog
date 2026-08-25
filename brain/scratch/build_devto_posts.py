import os
import re

research_dir = r"c:\Users\Godwin\Documents\projects\instatic\research\dev.to"
output_posts_dir = r"c:\Users\Godwin\Documents\projects\instatic\public-site\posts"

files = [
    "coding-with-claude-code-in-production.md",
    "autonomous-aws-ops-agent-mcp.md",
    "zero-trust-ai-agents-istio-kubernetes.md",
    "preventing-rag-api-hallucinations.md",
    "ai-evaluation-harness-benchmark-provenance.md",
    "contract-testing-least-derived-evidence.md",
    "file-based-multi-agent-state-machine.md",
    "saturating-gigabit-fiber-rust-tauri-nexdm.md",
    "react-datagrid-virtualization-space-explorer.md",
    "vectorized-payment-aging-pipeline-python.md",
    "streaming-io-lessons-from-acm-icpc.md",
    "essential-books-for-ai-systems-engineers.md",
    "engineering-culture-psychological-safety-humor.md"
]

images_map = {
    "coding-with-claude-code-in-production.md": ("claude_code_workflow.jpg", "Claude Code Terminal Agent Workflow Architecture Diagram"),
    "autonomous-aws-ops-agent-mcp.md": ("aws_mcp_ops_architecture.jpg", "Autonomous AWS Ops Agent with Model Context Protocol Architecture Diagram"),
    "zero-trust-ai-agents-istio-kubernetes.md": ("zero_trust_istio_k8s.jpg", "Zero Trust AI Agent Security in Istio and Kubernetes Architecture Diagram")
}

tags_map = {
    "coding-with-claude-code-in-production.md": ["AI", "Claude Code", "Workflow", "Dev Tools"],
    "autonomous-aws-ops-agent-mcp.md": ["AWS", "Cloud", "MCP", "Automation"],
    "zero-trust-ai-agents-istio-kubernetes.md": ["Kubernetes", "Istio", "Security", "AI"],
    "preventing-rag-api-hallucinations.md": ["RAG", "LLM", "APIs", "Data Integrity"],
    "ai-evaluation-harness-benchmark-provenance.md": ["AI", "Evaluation", "Benchmarks", "Testing"],
    "contract-testing-least-derived-evidence.md": ["Microservices", "Testing", "API", "Architecture"],
    "file-based-multi-agent-state-machine.md": ["AI Agents", "Architecture", "State Machines", "Orchestration"],
    "saturating-gigabit-fiber-rust-tauri-nexdm.md": ["Rust", "Tauri", "Networking", "Performance"],
    "react-datagrid-virtualization-space-explorer.md": ["React", "Performance", "Frontend", "Virtualization"],
    "vectorized-payment-aging-pipeline-python.md": ["Python", "Polars", "Data Engineering", "Performance"],
    "streaming-io-lessons-from-acm-icpc.md": ["Performance", "I/O", "Algorithms", "Systems"],
    "essential-books-for-ai-systems-engineers.md": ["AI Engineering", "Architecture", "Books", "Career"],
    "engineering-culture-psychological-safety-humor.md": ["Culture", "Engineering Leadership", "DevOps", "Teamwork"]
}

for filename in files:
    filepath = os.path.join(research_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    fm_match = re.search(r'^---\s*\ntitle:\s*"(.*?)"\s*\ndescription:\s*"(.*?)"\s*\n---', content, re.MULTILINE)
    if fm_match:
        title = fm_match.group(1)
        description = fm_match.group(2)
        body = content[fm_match.end():].strip()
    else:
        title = filename.replace('.md', '').replace('-', ' ').title()
        description = "Technical deep-dive on software engineering and architecture."
        body = content

    slug = filename.replace('.md', '')
    
    # Save markdown copy in public-site/posts/
    md_out_path = os.path.join(output_posts_dir, filename)
    with open(md_out_path, 'w', encoding='utf-8') as md_f:
        md_f.write(content)

    # Process HTML post
    post_html_dir = os.path.join(output_posts_dir, slug)
    os.makedirs(post_html_dir, exist_ok=True)
    html_out_path = os.path.join(post_html_dir, "index.html")

    # Extract TL;DR
    tldr_match = re.search(r'> \*\*TL;DR:\*\*\s*(.*)', body)
    tldr_text = tldr_match.group(1).strip() if tldr_match else description

    # Body conversion simple replaces
    clean_body = body
    if tldr_match:
        clean_body = clean_body.replace(tldr_match.group(0), '').strip()

    # Remove main H1 header if present
    clean_body = re.sub(r'^#\s+.*\n', '', clean_body).strip()

    # Generate Image Tag if in map
    img_html = ""
    if filename in images_map:
        img_file, img_alt = images_map[filename]
        img_html = f'''
      <figure>
        <img src="../../assets/images/{img_file}" alt="{img_alt}">
        <figcaption>Figure 1: {img_alt}.</figcaption>
      </figure>'''

    # Extract H2 headings for TOC
    h2_matches = re.findall(r'^##\s+(.*)', clean_body, re.MULTILINE)
    toc_items = []
    for idx, h2 in enumerate(h2_matches, 1):
        anchor = re.sub(r'[^\w\s-]', '', h2).strip().lower().replace(' ', '-')
        toc_items.append(f'<li><a href="#{anchor}">{idx}. {h2}</a></li>')
    toc_html = f'''
      <div class="toc">
        <div class="toc-title">Contents</div>
        <ol>
          {''.join(toc_items)}
        </ol>
      </div>''' if toc_items else ""

    # Convert markdown elements to basic HTML
    html_body = clean_body

    # Replace code blocks
    def code_repl(m):
        lang = m.group(1) or ""
        code_content = m.group(2).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        cls = "diagram" if lang == "text" or "┌" in code_content or "+" in code_content else ""
        return f'<pre class="{cls}"><code>{code_content}</code></pre>'

    html_body = re.sub(r'```(\w*)\n(.*?)```', code_repl, html_body, flags=re.DOTALL)

    # Replace H3s
    def h3_repl(m):
        h3_text = m.group(1).strip()
        anchor = re.sub(r'[^\w\s-]', '', h3_text).strip().lower().replace(' ', '-')
        return f'<h3 id="{anchor}">{h3_text}</h3>'
    html_body = re.sub(r'^###\s+(.*)', h3_repl, html_body, flags=re.MULTILINE)

    # Replace H2s
    def h2_repl(m):
        h2_text = m.group(1).strip()
        anchor = re.sub(r'[^\w\s-]', '', h2_text).strip().lower().replace(' ', '-')
        return f'<h2 id="{anchor}">{h2_text}</h2>'
    html_body = re.sub(r'^##\s+(.*)', h2_repl, html_body, flags=re.MULTILINE)

    # Replace lists
    html_body = re.sub(r'^\s*-\s+(.*)', r'<li>\1</li>', html_body, flags=re.MULTILINE)
    html_body = re.sub(r'((?:<li>.*</li>\n?)+)', r'<ul>\1</ul>', html_body)

    # Replace blockquotes
    html_body = re.sub(r'^>\s+(.*)', r'<blockquote><p>\1</p></blockquote>', html_body, flags=re.MULTILINE)

    # Replace bold & inline code
    html_body = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_body)
    html_body = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_body)

    # Paragraph wrap remaining loose lines
    paragraphs = html_body.split('\n\n')
    processed_p = []
    for p in paragraphs:
        p_str = p.strip()
        if p_str and not p_str.startswith('<h') and not p_str.startswith('<pre') and not p_str.startswith('<ul') and not p_str.startswith('<ol') and not p_str.startswith('<blockquote') and not p_str.startswith('<figure') and not p_str.startswith('<div'):
            processed_p.append(f'<p>{p_str}</p>')
        else:
            processed_p.append(p_str)
    final_body_html = '\n\n'.join(processed_p)

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

    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — StackScout</title>
  <meta name="description" content="{description}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <script src="../../assets/theme.js"></script>
  <link rel="stylesheet" href="../../assets/styles.css">
</head>
<body>
  <header>
    <div class="header-container">
      <div class="header-top">
        <a href="../../" class="logo">StackScout</a>
        <div class="nav-right">
          <a href="../../posts/">Posts</a>
          <a href="../../about/">About</a>
          <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" title="Toggle dark/light mode">
            <svg class="icon-sun" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>
            <svg class="icon-moon" viewBox="0 0 24 24"><path d="M12.3 2a10 10 0 0 0-1.9 20 10 10 0 0 0 9.2-6.2 1 1 0 0 0-1-1.3 8 8 0 1 1-7.6-11.5 1 1 0 0 0-1.3-1z"/></svg>
          </button>
        </div>
      </div>
      <div class="header-tagline">
        Dev infrastructure, automation, and deployment deep-dives.
      </div>
    </div>
  </header>

  <main>
    <article>
      <header>
        <h1>{title}</h1>
        <div class="subtitle">{description}</div>
        <div class="meta">AUG 25, 2026 &nbsp;·&nbsp; 10 MIN READ &nbsp;·&nbsp; BY STACKSCOUT ENGINEERING</div>
      </header>

      <blockquote>
        <p><strong>TL;DR:</strong> {tldr_text}</p>
      </blockquote>

      {toc_html}
      {img_html}

      {final_body_html}

      {faq_html}

      <div class="article-share">
        <span class="share-label">Share Article</span>
        <div class="share-buttons">
          <a href="https://x.com/intent/post?text={title.replace(' ', '%20')}&url=https%3A%2F%2Fstackscout-blog.pages.dev%2Fposts%2F{slug}%2F" target="_blank" rel="noopener" class="share-btn">X (Twitter)</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fstackscout-blog.pages.dev%2Fposts%2F{slug}%2F" target="_blank" rel="noopener" class="share-btn">LinkedIn</a>
          <a href="https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fstackscout-blog.pages.dev%2Fposts%2F{slug}%2F&t={title.replace(' ', '%20')}" target="_blank" rel="noopener" class="share-btn">Hacker News</a>
          <button class="share-btn copy-link-btn" onclick="copyArticleLink(this)">Copy Link</button>
        </div>
      </div>
    </article>
  </main>

  <footer>
    <div>&copy; 2026 StackScout</div>
    <div class="footer-links">
      <a href="https://github.com/godera010/stackscout-blog" target="_blank" rel="noopener">GitHub</a>
      <span>·</span>
      <a href="../../sitemap.xml">RSS</a>
    </div>
  </footer>

  <script type="application/ld+json">
  [
    {{
      "@context": "https://schema.org",
      "@type": "TechArticle",
      "headline": "{title}",
      "description": "{description}",
      "url": "https://stackscout-blog.pages.dev/posts/{slug}/",
      "datePublished": "2026-08-25",
      "dateModified": "2026-08-25",
      "author": {{
        "@type": "Organization",
        "name": "StackScout Engineering",
        "url": "https://stackscout-blog.pages.dev"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "StackScout",
        "url": "https://stackscout-blog.pages.dev"
      }}
    }}
  ]
  </script>
</body>
</html>'''

    with open(html_out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(full_html)

print("All 13 new dev.to articles generated successfully!")
