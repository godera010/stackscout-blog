# Cover image legibility and accuracy audit

Date: 2026-10-30. Report only — no images were regenerated, cropped, or altered. Each cover
was opened at full size (1376x768) next to its article text. "Phone legibility" is judged
against the main headline and section labels at 390px width (roughly 28% of full size);
anything already small or dense at full size is marked "no."

Severity key: **High** = misleading or factually wrong vs. the article; **Medium** = typo/garble
that could embarrass but doesn't mislead; **Low** = minor/cosmetic.

## Summary table

| Article | Garbled/misspelled/contradicting text | Phone legible | Recommendation |
|---|---|---|---|
| preventing-rag-api-hallucinations | None found | Yes (5-step labels are large) | Keep |
| zero-trust-ai-agents-istio-kubernetes | Minor: example SPIFFE path in image differs from the one in the article body (see below) | No (dense, many small boxes) | Replace with SVG (already planned, Part 3 #6) |
| docker-on-windows-wsl2-under-the-hood | None found | Partial (title yes, inner labels no) | Keep |
| ai-evaluation-harness-benchmark-provenance | "METRIC CALCULAT" and "ENVIRONMENT STATE" box labels are clipped/truncated (pre-existing crop, not a compression artifact) | No (small dense labels) | Regenerate (fix clipped labels) |
| essential-books-for-ai-systems-engineers | "Weer Gystems", "Neoral Netwerk" (should read "Neural Network") — garbled decorative on-screen text | No (background monitor text is illustrative/decorative only) | Keep (decorative illustration, not a technical claim) |
| autonomous-aws-ops-agent-mcp | None found | Partial (box titles yes, bullet labels no) | Keep |
| coding-with-claude-code-in-production | Garbled terminal text: `$ comt aamt 'command'`. **Medium/High**: the 6-step flow shown (Terminal REPL Input → Analyze & Decide → Tool Call → Multi-File Edits → Test Execution → Git Diff Generation) does not depict the article's actual core framework, the three-phase **Design-Plan-Execute** loop | No | Replace with SVG (already planned, Part 3 #4) |
| contract-testing-least-derived-evidence | None found | No (very dense, 20+ small boxes) | Regenerate or replace with SVG (listed as Part 3 phase 2 candidate) |
| durable-memory-vector-databases | **High**: subtitle literally reads "HIGH-QUALITY TECHNICAL DIAGRAM \| VECTOR INFOGRAPHIC" — an AI-generation prompt artifact baked into the image | No | Regenerate |
| engineering-culture-psychological-safety-humor | "DB TENTATIVE FAILURE" (garbled), "INVESTIGATIIION BEGUN" (misspelled), "D4:00 UTC" (should be "04:00 UTC") | No | Regenerate |
| file-based-multi-agent-state-machine | "Monitor Roots" (likely garbled — probably "Monitor Results") | Partial (box titles yes) | Replace with SVG (already planned, Part 3 #2) |
| instatic-cms-complete-guide | None found. Minor completeness note: diagram labels only "SQLITE DATABASE"; article states Instatic supports both SQLite and Postgres | Yes (title + box labels are large) | Keep |
| react-datagrid-virtualization-space-explorer | None found; "60 FPS" matches the article's claim | Partial (title yes, inner labels no) | Replace with SVG (already planned, Part 3 #5) |
| saturating-gigabit-fiber-rust-tauri-nexdm | "TAURI FROND INTERFACE" (should read "TAURI FRONTEND INTERFACE") | No (dense technical boxes) | Regenerate |
| streaming-io-lessons-from-acm-icpc | **High**: diagram depicts `io_uring`, `DPDK`, `mmap`, a lock-free ring buffer, and multi-threaded TCP chunking — none of which appear anywhere in the article body. The article is about a basic buffered-I/O lesson from a collegiate contest, not kernel-bypass networking | No | Regenerate (overstated/invented technical claims) |
| vectorized-payment-aging-pipeline-python | **High**: cover title is "VECTORIZED PAYMENT AGING WITH **POLARS** IN PYTHON" and the central element is a "POLARS QUERY ENGINE" with Apache Arrow/SIMD detail. The article is entirely about **Pandas** (title, TL;DR, code, and ASCII diagram all say Pandas; Polars is never mentioned in the body) | No | Regenerate — wrong library name is a factual contradiction |

## Flagged for human fact-check

These are concrete claims inside images (not prose) that a human should verify before any
regeneration, since a wrong fix could just encode the same error differently:

1. **vectorized-payment-aging-pipeline-python** — confirm the pipeline is Pandas, not Polars (the article body is unanimous, but confirm this wasn't a mid-write library swap that the image happened to get right and the text wrong).
2. **streaming-io-lessons-from-acm-icpc** — confirm no later revision of the article was meant to cover io_uring/DPDK/mmap; as it stands the image describes infrastructure the text doesn't.
3. **zero-trust-ai-agents-istio-kubernetes** — article body uses `spiffe://cluster.local/ns/ai-agent/sa/ai-agent-sa`; the cover image's example reads `spiffe://cluster.local/ns/default/sa/ai-agent-a`. Confirm which (if either) is the "real" example to standardize on.
4. **instatic-cms-complete-guide** — confirm whether the cover should also depict Postgres as a supported database, or whether SQLite-only is intentional (default/zero-config path).

## Notes

- All 16 covers load correctly and none are missing alt text.
- No image was edited as part of this audit (Part 2 is report-only per the handover).
- Of the 16, five are already slated for in-body SVG replacement in Part 3 phase 1
  (preventing-rag-api-hallucinations [cover itself is fine; new SVG is a body figure],
  file-based-multi-agent-state-machine, autonomous-aws-ops-agent-mcp,
  coding-with-claude-code-in-production, react-datagrid-virtualization-space-explorer,
  zero-trust-ai-agents-istio-kubernetes) — those SVGs address body content, not the cover,
  so the cover-level issues above (e.g., the claude-code terminal typo, the zero-trust SPIFFE
  path mismatch) still need a separate decision.
- Three covers have invented or contradicting technical claims and are the highest-priority
  regeneration candidates: **vectorized-payment-aging-pipeline-python** (wrong library),
  **streaming-io-lessons-from-acm-icpc** (invented tech not in the article),
  **durable-memory-vector-databases** (leaked AI-prompt text).
