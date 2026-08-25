import os
import re

posts_info = [
    {
        "title": "Beyond the Hype: My Production Workflow with Claude Code",
        "slug": "coding-with-claude-code-in-production",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "desc": "A battle-tested guide to coding with Claude Code. Learn the Design-Plan-Execute framework, repository setup, delegated tasks, and failure modes.",
        "tags": "AI · Developer Tools · Claude Code · Workflow"
    },
    {
        "title": "Building an Autonomous AWS Ops Agent with Model Context Protocol",
        "slug": "autonomous-aws-ops-agent-mcp",
        "date": "AUG 25, 2026",
        "read_time": "12 MIN READ",
        "desc": "Architecting an autonomous AWS cloud operations agent using Model Context Protocol (MCP), safety guardrails, and automated rollbacks.",
        "tags": "AWS · Cloud · MCP · Automation"
    },
    {
        "title": "Zero Trust Architecture for AI Agents in Istio and Kubernetes",
        "slug": "zero-trust-ai-agents-istio-kubernetes",
        "date": "AUG 25, 2026",
        "read_time": "14 MIN READ",
        "desc": "Securing autonomous AI agents in Kubernetes using Istio service mesh, SPIFFE/SPIRE identities, mTLS, and egress control.",
        "tags": "Kubernetes · Istio · Security · AI"
    },
    {
        "title": "Preventing RAG API Hallucinations: Least-Derived Evidence & Grounding",
        "slug": "preventing-rag-api-hallucinations",
        "date": "AUG 25, 2026",
        "read_time": "11 MIN READ",
        "desc": "How to prevent hallucinations in RAG-powered API applications by enforcing least-derived evidence and strict grounding policies.",
        "tags": "RAG · LLM · APIs · Data Integrity"
    },
    {
        "title": "File-Based Multi-Agent State Machines for Deterministic Code Generation",
        "slug": "file-based-multi-agent-state-machine",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "desc": "Designing file-based multi-agent state machines for reliable, deterministic code generation without complex framework overhead.",
        "tags": "AI Agents · Architecture · State Machines · Orchestration"
    },
    {
        "title": "Saturating Gigabit Fiber: Building a High-Throughput Download Manager in Rust and Tauri",
        "slug": "saturating-gigabit-fiber-rust-tauri-nexdm",
        "date": "AUG 25, 2026",
        "read_time": "9 MIN READ",
        "desc": "How to saturate 1 Gbps fiber connections using concurrent TCP chunking, zero-copy buffers, and Tokio in Rust & Tauri.",
        "tags": "Rust · Tauri · Networking · Performance"
    },
    {
        "title": "High-Performance React Data Grid Virtualization for Heavy Datasets",
        "slug": "react-datagrid-virtualization-space-explorer",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "desc": "Building 60 FPS React data grid virtualization for rendering 100,000+ records with smooth scrolling and dynamic row heights.",
        "tags": "React · Performance · Frontend · Virtualization"
    },
    {
        "title": "Vectorized Payment Aging Pipelines in Python with Polars",
        "slug": "vectorized-payment-aging-pipeline-python",
        "date": "AUG 25, 2026",
        "read_time": "11 MIN READ",
        "desc": "Accelerating financial payment aging calculations by 50x using vectorized Polars lazy evaluation and Rust backends.",
        "tags": "Python · Polars · Data Engineering · Performance"
    },
    {
        "title": "High-Throughput Streaming I/O: Lessons from ACM-ICPC Competitive Programming",
        "slug": "streaming-io-lessons-from-acm-icpc",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "desc": "Applying competitive programming fast I/O techniques, memory layout optimization, and streaming buffers to backend systems.",
        "tags": "Performance · I/O · Algorithms · Systems"
    },
    {
        "title": "Contract Testing Microservices with Least-Derived Evidence",
        "slug": "contract-testing-least-derived-evidence",
        "date": "AUG 25, 2026",
        "read_time": "11 MIN READ",
        "desc": "Eliminating brittle microservice integration tests with contract testing driven by least-derived evidence schemas.",
        "tags": "Microservices · Testing · API · Architecture"
    },
    {
        "title": "Building an AI Evaluation Harness with Benchmark Provenance",
        "slug": "ai-evaluation-harness-benchmark-provenance",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "desc": "Designing reproducible AI evaluation harnesses with benchmark provenance, versioned test suites, and regression tracking.",
        "tags": "AI · Evaluation · Benchmarks · Testing"
    },
    {
        "title": "Essential Reading List for AI Systems Engineers",
        "slug": "essential-books-for-ai-systems-engineers",
        "date": "AUG 25, 2026",
        "read_time": "9 MIN READ",
        "desc": "The foundational books every engineer must read to build scalable, resilient, and production-ready AI systems.",
        "tags": "AI Engineering · Architecture · Books · Career"
    },
    {
        "title": "Engineering Culture: Psychological Safety, Humor, and Blameless Postmortems",
        "slug": "engineering-culture-psychological-safety-humor",
        "date": "AUG 25, 2026",
        "read_time": "8 MIN READ",
        "desc": "Why psychological safety, technical humor, and blameless postmortems build resilient engineering organizations.",
        "tags": "Culture · Engineering Leadership · DevOps · Teamwork"
    },
    {
        "title": "Durable Memory: Why Vector Databases Aren't Enough",
        "slug": "durable-memory-vector-databases",
        "date": "AUG 14, 2026",
        "read_time": "12 MIN READ",
        "desc": "Why durable memory is more than persistent storage, and why the real architectural problem in AI systems begins at the write boundary.",
        "tags": "AI · LLM · Databases · Memory Stack"
    },
    {
        "title": "Docker on Windows with WSL 2: What Actually Happens Under the Hood",
        "slug": "docker-on-windows-wsl2-under-the-hood",
        "date": "AUG 14, 2026",
        "read_time": "14 MIN READ",
        "desc": "A practical deep dive into WSL 2, Linux kernel microVMs, container isolation, filesystem performance, and native WSL containers (wslc).",
        "tags": "Windows · WSL · Docker · Containers"
    },
    {
        "title": "Instatic CMS: The Complete Technical Guide",
        "slug": "instatic-cms-complete-guide",
        "date": "JUL 25, 2026",
        "read_time": "12 MIN READ",
        "desc": "Instatic CMS is a self-hosted visual CMS that outputs clean static HTML. Learn its architecture, deployment options, and how it compares to Webflow and WordPress.",
        "tags": "CMS · Static Site · Self-Hosting"
    }
]

# Generate index.html
index_items_html = []
for idx, p in enumerate(posts_info):
    is_featured = " featured" if idx == 0 else ""
    rel_path = f"./posts/{p['slug']}/"
    safe_title = p['title'].replace("'", "\\'")
    
    item = f'''      <!-- Article {idx+1} -->
      <div class="post-item{is_featured}">
        <div class="meta-line">{p['date']} &nbsp;·&nbsp; {p['read_time']}</div>
        <h2><a href="{rel_path}">{p['title']}</a></h2>
        <p>{p['desc']}</p>
        <div class="post-tags">{p['tags'].replace(' · ', ' <span>·</span> ')}</div>
        <div class="post-actions">
          <a href="{rel_path}" class="read-more">Read article &rarr;</a>
          <button class="share-card-btn" onclick="shareCard(event, 'https://stackscout-blog.pages.dev/posts/{p['slug']}/', '{safe_title}')" title="Share article">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
            Share
          </button>
        </div>
      </div>'''
    index_items_html.append(item)

index_full = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StackScout — Dev Infrastructure &amp; Automation</title>
  <meta name="description" content="Dev infrastructure, automation, and deployment deep-dives.">
  <meta property="og:title" content="StackScout">
  <meta property="og:description" content="Dev infrastructure, automation, and deployment deep-dives.">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary">
  <script src="./assets/theme.js"></script>
  <link rel="stylesheet" href="./assets/styles.css">
</head>
<body>
  <header>
    <div class="header-container">
      <div class="header-top">
        <a href="./" class="logo">StackScout</a>
        <div class="nav-right">
          <a href="./posts/">Posts</a>
          <a href="./about/">About</a>
          <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" title="Toggle dark/light mode">
            <svg class="icon-sun" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>
            <svg class="icon-moon" viewBox="0 0 24 24"><path d="M12.3 2a10 10 0 0 0-1.9 20 10 10 0 0 0 9.2-6.2 1 1 0 0 0-1-1.3 8 8 0 1 1-7.6-11.5 1 1 0 0 0-1-1.3z"/></svg>
          </button>
        </div>
      </div>
      <div class="header-tagline">
        Dev infrastructure, automation, and deployment deep-dives.
      </div>
    </div>
  </header>

  <main>
    <div class="section-label">LATEST &amp; ARCHIVE</div>

    <div class="post-list">
{chr(10).join(index_items_html)}
    </div>
  </main>

  <footer>
    <div>&copy; 2026 StackScout</div>
    <div class="footer-links">
      <a href="https://github.com/godera010/stackscout-blog" target="_blank" rel="noopener">GitHub</a>
      <span>·</span>
      <a href="./sitemap.xml">RSS</a>
    </div>
  </footer>
</body>
</html>'''

with open(r"c:\Users\Godwin\Documents\projects\instatic\public-site\index.html", 'w', encoding='utf-8') as f:
    f.write(index_full)

# Generate posts/index.html
archive_items_html = []
for idx, p in enumerate(posts_info):
    rel_path = f"../posts/{p['slug']}/"
    safe_title = p['title'].replace("'", "\\'")
    
    item = f'''      <!-- Article {idx+1} -->
      <div class="post-item">
        <div class="meta-line">{p['date']} &nbsp;·&nbsp; {p['read_time']}</div>
        <h2><a href="{rel_path}">{p['title']}</a></h2>
        <p>{p['desc']}</p>
        <div class="post-tags">{p['tags'].replace(' · ', ' <span>·</span> ')}</div>
        <div class="post-actions">
          <a href="{rel_path}" class="read-more">Read article &rarr;</a>
          <button class="share-card-btn" onclick="shareCard(event, 'https://stackscout-blog.pages.dev/posts/{p['slug']}/', '{safe_title}')" title="Share article">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
            Share
          </button>
        </div>
      </div>'''
    archive_items_html.append(item)

archive_full = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>All Posts — StackScout</title>
  <meta name="description" content="All dev infrastructure, automation, and deployment deep-dives on StackScout.">
  <meta property="og:title" content="All Posts — StackScout">
  <meta property="og:description" content="All dev infrastructure, automation, and deployment deep-dives on StackScout.">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary">
  <script src="../assets/theme.js"></script>
  <link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
  <header>
    <div class="header-container">
      <div class="header-top">
        <a href="../" class="logo">StackScout</a>
        <div class="nav-right">
          <a href="../posts/" class="active">Posts</a>
          <a href="../about/">About</a>
          <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" title="Toggle dark/light mode">
            <svg class="icon-sun" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>
            <svg class="icon-moon" viewBox="0 0 24 24"><path d="M12.3 2a10 10 0 0 0-1.9 20 10 10 0 0 0 9.2-6.2 1 1 0 0 0-1-1.3 8 8 0 1 1-7.6-11.5 1 1 0 0 0-1-1.3z"/></svg>
          </button>
        </div>
      </div>
      <div class="header-tagline">
        Dev infrastructure, automation, and deployment deep-dives.
      </div>
    </div>
  </header>

  <main>
    <div class="section-label">ALL ARTICLES ({len(posts_info)})</div>

    <div class="post-list">
{chr(10).join(archive_items_html)}
    </div>
  </main>

  <footer>
    <div>&copy; 2026 StackScout</div>
    <div class="footer-links">
      <a href="https://github.com/godera010/stackscout-blog" target="_blank" rel="noopener">GitHub</a>
      <span>·</span>
      <a href="../sitemap.xml">RSS</a>
    </div>
  </footer>
</body>
</html>'''

with open(r"c:\Users\Godwin\Documents\projects\instatic\public-site\posts\index.html", 'w', encoding='utf-8') as f:
    f.write(archive_full)

print("index.html and posts/index.html updated successfully!")
