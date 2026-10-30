#!/usr/bin/env node
// Usage: npm run new "My Post Title"
// Creates src/content/posts/<slug>.md as a draft with valid frontmatter.
import { existsSync, writeFileSync } from 'node:fs';

const title = process.argv.slice(2).join(' ').trim();
if (!title) {
  console.error('Usage: npm run new "Post title"');
  process.exit(1);
}
const slug = title
  .toLowerCase()
  .replace(/[^a-z0-9\s-]/g, '')
  .trim()
  .replace(/\s+/g, '-')
  .slice(0, 80);
const file = `src/content/posts/${slug}.md`;
if (existsSync(file)) {
  console.error(`Already exists: ${file}`);
  process.exit(1);
}
const today = new Date().toISOString().slice(0, 10);
writeFileSync(
  file,
  `---
title: ${JSON.stringify(title)}
description: "Write a 50-300 character summary used for SEO, the RSS feed, and article cards."
date: ${today}
tags: ["Engineering"]
tldr: "One or two sentences: what the reader will learn."
draft: true
# image: ../../assets/images/your-diagram.jpg   # optional; imageAlt is then required
# imageAlt: "Describe the image"
---

## First section

Write here. The title is rendered from frontmatter, so start body headings at \`##\`.
`,
);
console.log(`Created ${file} (draft: true). Run \`npm run dev\` to preview it.`);
