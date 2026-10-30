#!/usr/bin/env python3
"""Generates the hand-drawn cover SVGs in design/cover-sources/.
Render to WebP with: node design/render-covers.mjs
Content must come only from the article text."""
from pathlib import Path
from xml.sax.saxutils import escape as esc
OUT = Path(__file__).parent / 'cover-sources'
BG = '#0b1220'; PANEL = '#111c33'; TXT = '#f1f5f9'; SUB = '#aab6c8'
BLUE, PURPLE, GREEN, AMBER, RED = '#38bdf8', '#a78bfa', '#34d399', '#fbbf24', '#f87171'

def head(title_parts):
    # title_parts: list of (text, colour)
    t = ''.join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in title_parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1376 768" width="1376" height="768" font-family="'Noto Sans','DejaVu Sans',Arial,sans-serif">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#14213d"/></linearGradient>
  <marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7d8aa3"/></marker>
</defs>
<rect width="1376" height="768" fill="url(#bg)"/>
<text x="688" y="84" text-anchor="middle" font-size="46" font-weight="700" fill="{TXT}">{t}</text>
'''
def box(x, y, w, h, color, title, lines=(), tsize=26, lsize=21, fill=PANEL, align='middle', title_color=TXT):
    cx = x + w / 2
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{color}" stroke-width="3"/>\n'
    ty = (y + h / 2 + tsize * 0.35) if not lines else (y + 24 + tsize)
    s += f'<text x="{cx}" y="{ty}" text-anchor="middle" font-size="{tsize}" font-weight="700" fill="{title_color}">{esc(title)}</text>\n'
    for i, l in enumerate(lines):
        s += f'<text x="{cx}" y="{ty + 20 + (i + 1) * (lsize + 12)}" text-anchor="middle" font-size="{lsize}" fill="{SUB}">{esc(l)}</text>\n'
    return s
def arrow(x1, y1, x2, y2, dash=False):
    d = ' stroke-dasharray="8,6"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7d8aa3" stroke-width="3.5" marker-end="url(#ar)"{d}/>\n'
def text(x, y, s, size=22, color=SUB, anchor='middle', weight='400'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(s)}</text>\n'

# 1. payment aging (Pandas) ---------------------------------------------------
s = head([('Vectorized Payment Aging with ', TXT), ('Pandas', BLUE)])
s += box(28, 170, 360, 470, BLUE, 'Data Ingestion Layer', ['CSV export', 'PostgreSQL billing DB', 'Stripe webhook'], lsize=24)
s += box(458, 170, 460, 470, PURPLE, 'Vectorized Pandas Engine',
         ['1. Normalize ISO-8601 timestamps', '2. Compute delinquency deltas', '   (PaymentDate - DueDate)', '3. Age open invoices', '   (Today - DueDate)', '4. Customer GroupBy', '   aggregation & scoring'], lsize=23)
s += box(988, 170, 360, 470, GREEN, 'Actionable Outputs', ['Categorized risk tiers:', 'Excellent · Good', 'Attention', 'High Risk · Critical', '', 'Automated overdue', 'dunning webhooks'], lsize=23)
s += arrow(392, 405, 452, 405) + arrow(922, 405, 982, 405)
s += '</svg>\n'
(OUT / 'pandas_payment_aging_pipeline.svg').write_text(s, encoding='utf-8')

# 2. streaming I/O ---------------------------------------------------------------
s = head([('Streaming I/O: ', TXT), ('O(1) Memory', GREEN), (' vs Batch Buffering', TXT)])
s += f'<rect x="28" y="125" width="1320" height="270" rx="20" fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="10,7"/>\n'
s += text(60, 170, 'Flawed: in-memory batch buffering', 28, RED, 'start', '700')
s += box(80, 205, 320, 150, BLUE, 'Input', ['100k records'])
s += box(528, 205, 320, 150, AMBER, 'Giant buffer array', ['all cases held at once'], lsize=21)
s += box(976, 205, 320, 150, RED, 'Memory Limit', ['Exceeded (MLE)'], tsize=26, lsize=22)
s += arrow(404, 280, 524, 280) + arrow(852, 280, 972, 280)
s += f'<rect x="28" y="420" width="1320" height="320" rx="20" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-dasharray="10,7"/>\n'
s += text(60, 465, 'Correct: streaming single-pass I/O', 28, GREEN, 'start', '700')
s += box(80, 495, 320, 130, BLUE, 'Read line')
s += box(528, 495, 320, 130, PURPLE, 'Process token')
s += box(976, 495, 320, 130, GREEN, 'Flush output')
s += arrow(404, 560, 524, 560) + arrow(852, 560, 972, 560)
s += f'<path d="M1136,630 L1136,690 L240,690 L240,630" fill="none" stroke="#7d8aa3" stroke-width="3.5" stroke-dasharray="8,6" marker-end="url(#ar)"/>\n'
s += text(688, 678, 'Loop per record: constant O(1) storage', 22, TXT, 'middle', '600')
s += '</svg>\n'
(OUT / 'streaming_fast_io.svg').write_text(s, encoding='utf-8')

# 3. durable memory ---------------------------------------------------------------
s = head([('Durable Memory Is a ', TXT), ('Policy', PURPLE), (', Not a Place', TXT)])
xs = [28, 374, 720, 1066]; w = 282
items = [('Durable Memory', 'Curated policies', PURPLE), ('Active Working Memory', 'Task-assembled', BLUE),
         ('Context Window', 'L1/L2 cache', AMBER), ('Model Inference', 'Execution', GREEN)]
for x, (t, sub, c) in zip(xs, items):
    s += box(x, 130, w, 150, c, t, [sub], tsize=20, lsize=21)
for x in xs[:-1]:
    s += arrow(x + w + 4, 205, x + w + 60, 205)
s += text(688, 345, 'Memory is a write problem: what earns a place in durable memory?', 27, TXT, 'middle', '700')
s += box(28, 395, 300, 280, BLUE, 'Observation / output', tsize=22)
s += box(400, 395, 576, 280, PURPLE, 'Write boundary', ['Is it authoritative?', 'Is it verified?', 'Is it a duplicate?', 'Does it expire?'], tsize=28, lsize=24)
s += box(1048, 395, 300, 280, GREEN, 'Durable Memory', ['only what passes', 'the policy'], tsize=26, lsize=22)
s += arrow(332, 535, 396, 535) + arrow(980, 535, 1044, 535)
s += text(1014, 515, 'passed', 19, GREEN)
s += '</svg>\n'
(OUT / 'durable_memory_architecture.svg').write_text(s, encoding='utf-8')

# 4. essential AI engineering books: the recommended reading order ------------
s = head([('10 Essential Books: ', TXT), ('The Recommended Reading Order', BLUE)])
xs = [28, 374, 720, 1066]; w = 282
phases = [
    ('Phase 1: Architecture', ['AI Engineering', 'by Chip Huyen'], BLUE),
    ('Phase 2: Low-Level Mechanics', ['Build an LLM', 'from Scratch — Raschka'], PURPLE),
    ('Phase 3: Operations & RAG', ["LLM Engineer's Handbook", 'Iusztin & Labonne'], AMBER),
    ('Phase 4: Agentic Systems', ['Building Agentic', 'AI Systems', 'Biswas & Talukdar'], GREEN),
]
for x, (t, lines, c) in zip(xs, phases):
    s += box(x, 210, w, 230, c, t, lines, tsize=20, lsize=17)
for x in xs[:-1]:
    s += arrow(x + w + 4, 325, x + w + 60, 325)
s += text(688, 150, 'From end-to-end mental model to low-level mechanics to production RAG to multi-agent systems', 23, SUB, 'middle', '400')
s += text(688, 500, '10 books total, grouped into 4 reading phases — see the full list and comparison table below', 23, SUB, 'middle', '400')
s += '</svg>\n'
(OUT / 'ai_books_engineering.svg').write_text(s, encoding='utf-8')

# 5. NeXDM: saturating gigabit fiber with Rust + Tauri -------------------------
s = head([('NeXDM: Saturating Gigabit Fiber with ', TXT), ('Rust + Tauri', AMBER)])
s += box(28, 150, 1320, 110, BLUE, 'Source File (Remote URL)',
         ['Range 0-25%          Range 26-50%          Range 51-75%          Range 76-100%'], tsize=24, lsize=20)
s += arrow(688, 260, 688, 310)
s += box(188, 314, 1000, 190, PURPLE, 'NeXDM Async Rust Engine (Tokio Core)',
         ['64 concurrent HTTP Range requests (Socket 1..64)', 'Zero-copy ring buffer recycling',
          'Non-blocking asynchronous disk flush'], tsize=24, lsize=21)
s += arrow(688, 504, 688, 554)
s += box(338, 558, 700, 110, GREEN, 'Local Target File (Assembled)', tsize=24)
s += text(688, 710, '64-segment throughput · 4MB binary · 28MB idle RAM', 23, SUB, 'middle', '600')
s += '</svg>\n'
(OUT / 'rust_tauri_gigabit_network.svg').write_text(s, encoding='utf-8')

# 6. zero-trust NEXUS agent blast-radius quarantine (Istio + SPIFFE) -----------
s = head([('Quarantining NEXUS: ', TXT), ('Istio + SPIFFE', PURPLE), (' Blast-Radius Isolation', TXT)])
s += f'<rect x="40" y="130" width="620" height="560" rx="18" fill="#101a30" stroke="{BLUE}" stroke-width="3"/>\n'
s += text(350, 168, 'Istio Service Mesh (Amazon EKS) — mTLS STRICT', 24, BLUE, 'middle', '700')
s += box(90, 300, 520, 220, PURPLE, 'NEXUS Agent Pod',
         ['spiffe://cluster.local/ns/', 'ai-agent/sa/ai-agent-sa', '', 'Envoy sidecar — AuthorizationPolicy'],
         tsize=24, lsize=21)
s += arrow(610, 360, 700, 300, dash=False)
s += arrow(610, 440, 700, 540, dash=False)
s += box(740, 230, 580, 110, GREEN, 'Prometheus :9090 — ALLOW read-only GET', tsize=22)
s += box(740, 530, 580, 110, GREEN, 'Jaeger — ALLOW read-only GET', tsize=22)
s += box(740, 380, 580, 110, RED, 'lsd-payments namespace — DENY all TCP/HTTP', tsize=22)
s += box(740, 650, 580, 90, RED, 'frontend namespace — DENY all TCP/HTTP', tsize=22)
s += text(350, 610, 'Remediation requires an on-call engineer approval', 20, SUB, 'middle', '400')
s += text(350, 635, '(Grafana Cloud IRM or Discord) — NEXUS cannot write directly', 20, SUB, 'middle', '400')
s += '</svg>\n'
(OUT / 'zero_trust_istio_k8s.svg').write_text(s, encoding='utf-8')
print('ok')
