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
s = head([('10 Essential Books: ', TXT), ('Recommended Reading Order', BLUE)])
xs = [22, 366, 710, 1054]; w = 300
phases = [
    ('Phase 1', 'Architecture &|Lifecycle', ['AI Engineering', 'Chip Huyen'], BLUE),
    ('Phase 2', 'Low-Level|Mechanics', ['Build a Large', 'Language Model', '(From Scratch)', 'Sebastian Raschka'], PURPLE),
    ('Phase 3', 'Operations|& RAG', ["The LLM Engineer's", 'Handbook', 'Iusztin & Labonne'], AMBER),
    ('Phase 4', 'Agentic|Systems', ['Building Agentic', 'AI Systems', 'Biswas & Talukdar'], GREEN),
]
for x, (ph, t, lines, c) in zip(xs, phases):
    s += f'<rect x="{x}" y="170" width="{w}" height="400" rx="16" fill="{PANEL}" stroke="{c}" stroke-width="3"/>\n'
    s += text(x + w / 2, 225, ph.upper(), 24, c, 'middle', '700')
    s += text(x + w / 2, 275, t.split('|')[0], 28, TXT, 'middle', '700')
    s += text(x + w / 2, 311, t.split('|')[1], 28, TXT, 'middle', '700')
    for k, l in enumerate(lines):
        s += text(x + w / 2, 370 + k * 40, l, 24, SUB if k < len(lines) - 1 else TXT, 'middle', '400' if k < len(lines) - 1 else '600')
for x in xs[:-1]:
    s += arrow(x + w + 3, 370, x + w + 40, 370)
s += text(688, 640, '10 books in total: the full list and comparison table follow in the article', 27, SUB)
s += '</svg>\n'
(OUT / 'ai_books_engineering.svg').write_text(s, encoding='utf-8')

# 5. NeXDM: saturating gigabit fiber with Rust + Tauri -------------------------
s = head([('NeXDM: Gigabit Fiber with ', TXT), ('Rust + Tauri', AMBER)])
s += f'<rect x="28" y="130" width="1320" height="170" rx="16" fill="{PANEL}" stroke="{BLUE}" stroke-width="3"/>\n'
s += text(688, 172, 'Source file (remote URL)', 30, TXT, 'middle', '700')
for x, r in zip([100, 420, 740, 1060], ['Range 0-25%', 'Range 26-50%', 'Range 51-75%', '...']):
    s += f'<rect x="{x}" y="198" width="240" height="68" rx="12" fill="none" stroke="#5b6b86" stroke-width="2"/>\n'
    s += text(x + 120, 242, r, 26, SUB)
s += arrow(688, 304, 688, 350)
s += f'<rect x="28" y="356" width="1320" height="230" rx="16" fill="{PANEL}" stroke="{PURPLE}" stroke-width="3"/>\n'
s += text(688, 400, 'NeXDM async Rust engine (Tokio core)', 30, TXT, 'middle', '700')
for k, l in enumerate(['64 concurrent HTTP Range requests', 'Zero-copy ring buffer recycling', 'Non-blocking asynchronous disk flush']):
    s += text(688, 454 + k * 44, l, 27, SUB)
s += arrow(688, 590, 688, 636)
s += f'<rect x="388" y="640" width="600" height="80" rx="16" fill="{PANEL}" stroke="{GREEN}" stroke-width="3"/>\n'
s += text(688, 691, 'Local target file (assembled)', 29, TXT, 'middle', '700')
s += text(1180, 676, '64 segments · ~4 MB binary', 22, GREEN, 'middle', '600')
s += text(1180, 708, '~28 MB idle RAM', 22, GREEN, 'middle', '600')
s += '</svg>\n'
(OUT / 'rust_tauri_gigabit_network.svg').write_text(s, encoding='utf-8')

# 6. Zero-trust: NEXUS in an Istio mesh ---------------------------------------
s = head([('Quarantining NEXUS: ', TXT), ('Istio + SPIFFE', PURPLE), (' Isolation', TXT)])
s = s.replace('font-size="46"', 'font-size="42"')
s += f'<rect x="28" y="130" width="600" height="600" rx="18" fill="#0f1a30" stroke="{BLUE}" stroke-width="3"/>\n'
s += text(328, 172, 'Istio service mesh (Amazon EKS)', 26, BLUE, 'middle', '700')
s += text(328, 204, 'mTLS STRICT', 22, BLUE, 'middle', '600')
s += f'<rect x="64" y="260" width="528" height="260" rx="14" fill="{PANEL}" stroke="{PURPLE}" stroke-width="3"/>\n'
s += text(328, 306, 'NEXUS agent pod', 30, TXT, 'middle', '700')
s += f'<text x="328" y="352" text-anchor="middle" font-size="22" fill="{SUB}" font-family="DejaVu Sans Mono,monospace">spiffe://cluster.local/ns/</text>\n'
s += f'<text x="328" y="384" text-anchor="middle" font-size="22" fill="{SUB}" font-family="DejaVu Sans Mono,monospace">ai-agent/sa/ai-agent-sa</text>\n'
s += f'<rect x="104" y="420" width="448" height="62" rx="10" fill="none" stroke="{PURPLE}" stroke-width="2"/>\n'
s += text(328, 460, 'Envoy sidecar: AuthorizationPolicy', 22, TXT, 'middle', '600')
s += text(328, 590, 'Remediation needs an on-call engineer\'s approval', 22, SUB)
s += text(328, 622, '(Grafana Cloud IRM or Discord).', 22, SUB)
s += text(328, 654, 'NEXUS cannot write directly.', 22, SUB)
rows = [('Prometheus :9090', 'ALLOW: read-only GET', GREEN, True), ('lsd-payments namespace', 'DENY: all TCP/HTTP', RED, False),
        ('Jaeger', 'ALLOW: read-only GET', GREEN, True), ('frontend namespace', 'DENY: all TCP/HTTP', RED, False)]
for k, (t, sub, c, ok) in enumerate(rows):
    y = 135 + k * 150
    s += box(760, y, 588, 124, c, t, [sub], tsize=27, lsize=23)
    dash = '' if ok else ' stroke-dasharray="9,7"'
    mk = ' marker-end="url(#ar)"' if ok else ''
    s += f'<line x1="596" y1="390" x2="756" y2="{y + 62}" stroke="{c}" stroke-width="3.5"{dash}{mk}/>\n'
s += '</svg>\n'
(OUT / 'zero_trust_istio_k8s.svg').write_text(s, encoding='utf-8')
print('ok')
