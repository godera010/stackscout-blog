import os
import re

posts_dir = r"c:\Users\Godwin\Documents\projects\instatic\public-site\posts"
research_dir = r"c:\Users\Godwin\Documents\projects\instatic\research\dev.to"

articles = [
    {
        "slug": "coding-with-claude-code-in-production",
        "title": "Beyond the Hype: My Production Workflow with Claude Code",
        "desc": "A battle-tested guide to coding with Claude Code. Learn the Design-Plan-Execute framework, repository setup, delegated tasks, and failure modes.",
        "author": "GODWIN ERA · SENIOR SYSTEMS ARCHITECT",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "image": "claude_code_workflow.jpg",
        "image_caption": "Figure 1: Claude Code Terminal REPL Workflow showing tool dispatch, test loops, and git commit generation.",
        "related": ["file-based-multi-agent-state-machine", "ai-evaluation-harness-benchmark-provenance"]
    },
    {
        "slug": "autonomous-aws-ops-agent-mcp",
        "title": "Building an Autonomous AWS Ops Agent with Model Context Protocol",
        "desc": "Architecting an autonomous AWS cloud operations agent using Model Context Protocol (MCP), safety guardrails, and automated rollbacks.",
        "author": "GODWIN ERA · CLOUD INFRASTRUCTURE LEAD",
        "date": "AUG 25, 2026",
        "read_time": "12 MIN READ",
        "image": "aws_mcp_ops_architecture.jpg",
        "image_caption": "Figure 1: Autonomous AWS Ops Agent Architecture with MCP tool execution, CloudWatch telemetry, and automated rollback loop.",
        "related": ["zero-trust-ai-agents-istio-kubernetes", "coding-with-claude-code-in-production"]
    },
    {
        "slug": "zero-trust-ai-agents-istio-kubernetes",
        "title": "Zero Trust Architecture for AI Agents in Istio and Kubernetes",
        "desc": "Securing autonomous AI agents in Kubernetes using Istio service mesh, SPIFFE/SPIRE identities, mTLS, and egress control.",
        "author": "GODWIN ERA · SECURITY & PLATFORM LEAD",
        "date": "AUG 25, 2026",
        "read_time": "14 MIN READ",
        "image": "zero_trust_istio_k8s.jpg",
        "image_caption": "Figure 1: Zero Trust AI Agent Security in Istio & Kubernetes with Envoy sidecars, SPIFFE identities, and strict egress policies.",
        "related": ["autonomous-aws-ops-agent-mcp", "contract-testing-least-derived-evidence"]
    },
    {
        "slug": "preventing-rag-api-hallucinations",
        "title": "Preventing RAG API Hallucinations: Least-Derived Evidence & Grounding",
        "desc": "How to prevent hallucinations in RAG-powered API applications by enforcing least-derived evidence and strict grounding policies.",
        "author": "GODWIN ERA · AI SYSTEMS ENGINEER",
        "date": "AUG 25, 2026",
        "read_time": "11 MIN READ",
        "image": "rag_api_grounding.jpg",
        "image_caption": "Figure 1: RAG API Hallucination Prevention Pipeline showing Least-Derived Evidence Verification and Grounding checks.",
        "related": ["durable-memory-vector-databases", "contract-testing-least-derived-evidence"]
    },
    {
        "slug": "file-based-multi-agent-state-machine",
        "title": "File-Based Multi-Agent State Machines for Deterministic Code Generation",
        "desc": "Designing file-based multi-agent state machines for reliable, deterministic code generation without complex framework overhead.",
        "author": "GODWIN ERA · SENIOR SYSTEMS ARCHITECT",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "image": "multi_agent_state_machine.jpg",
        "image_caption": "Figure 1: File-Based Multi-Agent State Machine Architecture showing JSON lock files, state transitions, and deterministic disk tasks.",
        "related": ["coding-with-claude-code-in-production", "streaming-io-lessons-from-acm-icpc"]
    },
    {
        "slug": "saturating-gigabit-fiber-rust-tauri-nexdm",
        "title": "Saturating Gigabit Fiber: Building a High-Throughput Download Manager in Rust and Tauri",
        "desc": "How to saturate 1 Gbps fiber connections using concurrent TCP chunking, zero-copy buffers, and Tokio in Rust & Tauri.",
        "author": "GODWIN ERA · HIGH PERFORMANCE SYSTEMS ENGINEER",
        "date": "AUG 25, 2026",
        "read_time": "9 MIN READ",
        "image": "rust_tauri_gigabit_network.jpg",
        "image_caption": "Figure 1: Saturating Gigabit Fiber Architecture in Rust and Tauri with Tokio async loop and zero-copy buffer pool.",
        "related": ["streaming-io-lessons-from-acm-icpc", "react-datagrid-virtualization-space-explorer"]
    },
    {
        "slug": "react-datagrid-virtualization-space-explorer",
        "title": "High-Performance React Data Grid Virtualization for Heavy Datasets",
        "desc": "Building 60 FPS React data grid virtualization for rendering 100,000+ records with smooth scrolling and dynamic row heights.",
        "author": "GODWIN ERA · FRONTEND PERFORMANCE ARCHITECT",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "image": "react_datagrid_virtualization.jpg",
        "image_caption": "Figure 1: React Data Grid Virtualization Architecture showing viewport calculations, spatial row index, and 60 FPS rendering pipeline.",
        "related": ["saturating-gigabit-fiber-rust-tauri-nexdm", "vectorized-payment-aging-pipeline-python"]
    },
    {
        "slug": "vectorized-payment-aging-pipeline-python",
        "title": "Vectorized Payment Aging Pipelines in Python with Polars",
        "desc": "Accelerating financial payment aging calculations by 50x using vectorized Polars lazy evaluation and Rust backends.",
        "author": "GODWIN ERA · DATA SYSTEMS ENGINEER",
        "date": "AUG 25, 2026",
        "read_time": "11 MIN READ",
        "image": "polars_vectorized_pipeline.jpg",
        "image_caption": "Figure 1: Vectorized Payment Aging Architecture with Polars, Apache Arrow memory buffers, and SIMD execution.",
        "related": ["streaming-io-lessons-from-acm-icpc", "react-datagrid-virtualization-space-explorer"]
    },
    {
        "slug": "streaming-io-lessons-from-acm-icpc",
        "title": "High-Throughput Streaming I/O: Lessons from ACM-ICPC Competitive Programming",
        "desc": "Applying competitive programming fast I/O techniques, memory layout optimization, and streaming buffers to backend systems.",
        "author": "GODWIN ERA · SYSTEMS PROGRAMMING SPECIALIST",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "image": "streaming_fast_io.jpg",
        "image_caption": "Figure 1: High-Throughput Streaming I/O Pipeline showing memory-mapped buffers, ring buffer queues, and zero-syscall bulk ingestion.",
        "related": ["saturating-gigabit-fiber-rust-tauri-nexdm", "vectorized-payment-aging-pipeline-python"]
    },
    {
        "slug": "contract-testing-least-derived-evidence",
        "title": "Contract Testing Microservices with Least-Derived Evidence",
        "desc": "Eliminating brittle microservice integration tests with contract testing driven by least-derived evidence schemas.",
        "author": "GODWIN ERA · DISTRIBUTED SYSTEMS ARCHITECT",
        "date": "AUG 25, 2026",
        "read_time": "11 MIN READ",
        "image": "contract_testing_schema.jpg",
        "image_caption": "Figure 1: Contract Testing Architecture with Least-Derived Evidence, OpenAPI validation, and automated CI/CD gating.",
        "related": ["preventing-rag-api-hallucinations", "ai-evaluation-harness-benchmark-provenance"]
    },
    {
        "slug": "ai-evaluation-harness-benchmark-provenance",
        "title": "Building an AI Evaluation Harness with Benchmark Provenance",
        "desc": "Designing reproducible AI evaluation harnesses with benchmark provenance, versioned test suites, and regression tracking.",
        "author": "GODWIN ERA · AI EVALUATION ARCHITECT",
        "date": "AUG 25, 2026",
        "read_time": "10 MIN READ",
        "image": "ai_eval_harness.jpg",
        "image_caption": "Figure 1: AI Evaluation Harness with Benchmark Provenance showing test fixtures, regression dashboard, and audit lineage.",
        "related": ["preventing-rag-api-hallucinations", "coding-with-claude-code-in-production"]
    },
    {
        "slug": "essential-books-for-ai-systems-engineers",
        "title": "Essential Reading List for AI Systems Engineers",
        "desc": "The foundational books every engineer must read to build scalable, resilient, and production-ready AI systems.",
        "author": "GODWIN ERA · PRINCIPAL ARCHITECT",
        "date": "AUG 25, 2026",
        "read_time": "9 MIN READ",
        "image": "ai_books_engineering.jpg",
        "image_caption": "Figure 1: Foundational literature for distributed AI systems engineering, high-throughput pipelines, and systems design.",
        "related": ["engineering-culture-psychological-safety-humor", "durable-memory-vector-databases"]
    },
    {
        "slug": "engineering-culture-psychological-safety-humor",
        "title": "Engineering Culture: Psychological Safety, Humor, and Blameless Postmortems",
        "desc": "Why psychological safety, technical humor, and blameless postmortems build resilient engineering organizations.",
        "author": "GODWIN ERA · VP OF ENGINEERING",
        "date": "AUG 25, 2026",
        "read_time": "8 MIN READ",
        "image": "engineering_culture_postmortem.jpg",
        "image_caption": "Figure 1: Collaborative Blameless Postmortem Analysis showing shared incident timeline and root-cause transparency.",
        "related": ["essential-books-for-ai-systems-engineers", "coding-with-claude-code-in-production"]
    },
    {
        "slug": "durable-memory-vector-databases",
        "title": "Durable Memory: Why Vector Databases Aren't Enough",
        "desc": "Why durable memory is more than persistent storage, and why the real architectural problem in AI systems begins at the write boundary.",
        "author": "GODWIN ERA · PRINCIPAL AI ARCHITECT",
        "date": "AUG 14, 2026",
        "read_time": "12 MIN READ",
        "image": "durable_memory_architecture.jpg",
        "image_caption": "Figure 1: AI Memory Layers Architecture showing Durable Memory policy layer feeding Active Working Memory and LLM Context.",
        "related": ["preventing-rag-api-hallucinations", "file-based-multi-agent-state-machine"]
    },
    {
        "slug": "docker-on-windows-wsl2-under-the-hood",
        "title": "Docker on Windows with WSL 2: What Actually Happens Under the Hood",
        "desc": "A practical deep dive into WSL 2, Linux kernel microVMs, container isolation, filesystem performance, and native WSL containers (wslc).",
        "author": "GODWIN ERA · SYSTEMS INFRASTRUCTURE ENGINEER",
        "date": "AUG 14, 2026",
        "read_time": "14 MIN READ",
        "image": "wsl2_architecture.jpg",
        "image_caption": "Figure 1: Windows 11 Virtualization Architecture showing Host Compute Service (HCS), LightVM microkernel, and container cgroups v2.",
        "related": ["zero-trust-ai-agents-istio-kubernetes", "instatic-cms-complete-guide"]
    },
    {
        "slug": "instatic-cms-complete-guide",
        "title": "Instatic CMS: The Complete Technical Guide",
        "desc": "Instatic CMS is a self-hosted visual CMS that outputs clean static HTML. Learn its architecture, deployment options, and how it compares to Webflow and WordPress.",
        "author": "GODWIN ERA · PLATFORM ARCHITECT",
        "date": "JUL 25, 2026",
        "read_time": "12 MIN READ",
        "image": "instatic_architecture.jpg",
        "image_caption": "Figure 1: Instatic CMS Architecture showing single Bun runtime, SQLite/Postgres persistence, visual canvas, and static compiler.",
        "related": ["react-datagrid-virtualization-space-explorer", "docker-on-windows-wsl2-under-the-hood"]
    }
]

articles_by_slug = {a["slug"]: a for a in articles}

def build_recommended_section(related_slugs):
    cards_html = []
    for s in related_slugs:
        if s in articles_by_slug:
            rel_art = articles_by_slug[s]
            card = f'''        <a href="../../posts/{rel_art['slug']}/" class="recommended-card">
          <div class="meta-line">{rel_art['date']} &nbsp;·&nbsp; {rel_art['read_time']}</div>
          <h3>{rel_art['title']}</h3>
          <p>{rel_art['desc']}</p>
          <span class="read-link">Read article &rarr;</span>
        </a>'''
            cards_html.append(card)
            
    return f'''      <!-- Recommended Reading Section -->
      <section class="recommended-section">
        <div class="section-label">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          RECOMMENDED READING
        </div>
        <div class="recommended-grid">
{chr(10).join(cards_html)}
        </div>
      </section>'''

# Process each article
for art in articles:
    post_html_path = os.path.join(posts_dir, art["slug"], "index.html")
    if not os.path.exists(post_html_path):
        continue
    
    with open(post_html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update meta byline with Sentry-style real engineer byline
    html = re.sub(
        r'<div class="meta">.*?</div>',
        f'<div class="meta">{art["date"]} &nbsp;·&nbsp; {art["read_time"]} &nbsp;·&nbsp; BY {art["author"]}</div>',
        html
    )

    # Ensure Figure Image is present
    img_tag = f'''      <figure>
        <img src="../../assets/images/{art['image']}" alt="{art['title']}">
        <figcaption>{art['image_caption']}</figcaption>
      </figure>'''

    # If figure is not already in the article body or has old image, insert or replace
    if '<figure>' in html:
        html = re.sub(r'<figure>.*?</figure>', img_tag, html, flags=re.DOTALL)
    else:
        # Insert figure right after TOC or blockquote
        if '<div class="toc">' in html:
            html = html.replace('</div>\n\n      <h2', f'</div>\n\n{img_tag}\n\n      <h2', 1)
        elif '</blockquote>' in html:
            html = html.replace('</blockquote>', f'</blockquote>\n\n{img_tag}', 1)

    # Build and insert Recommended Reading section before .article-share or footer
    rec_html = build_recommended_section(art["related"])
    if '<section class="recommended-section">' in html:
        html = re.sub(r'<section class="recommended-section">.*?</section>', rec_html, html, flags=re.DOTALL)
    elif '<div class="article-share">' in html:
        html = html.replace('<div class="article-share">', f'{rec_html}\n\n      <div class="article-share">')

    with open(post_html_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("All 16 articles updated with Sentry style bylines, generated images, and Recommended Reading sections!")
