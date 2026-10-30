import { defineConfig } from 'astro/config';

// ASCII/box-drawing diagrams get a `.diagram` class instead of syntax highlighting.
const BOX_CHARS = /[┌┐└┘│─├┤┬┴┼▶◀▲▼]|\+--/;
const diagramTransformer = {
  name: 'stackscout-diagram',
  pre(node) {
    const lang = this.options.lang;
    if (lang === 'text' || lang === 'ascii' || lang === 'plaintext' || BOX_CHARS.test(this.source)) {
      this.addClassToHast(node, 'diagram');
    }
  },
};

export default defineConfig({
  site: 'https://stackscout.blog',
  trailingSlash: 'always', // keeps existing /posts/<slug>/ URLs identical
  build: { format: 'directory' },
  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      defaultColor: false, // colours come from CSS variables so the theme toggle works
      transformers: [diagramTransformer],
    },
  },
});
