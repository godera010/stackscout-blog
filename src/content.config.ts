import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: ({ image }) =>
    z
      .object({
        title: z.string().min(10).max(120),
        description: z.string().min(50).max(300),
        date: z.coerce.date(),
        updated: z.coerce.date().optional(),
        tags: z.array(z.string()).min(1).max(7),
        /** Short summary shown in the TL;DR box at the top of the article. */
        tldr: z.string().optional(),
        /** Cover/diagram image. Put the file in src/assets/images and use a relative path. */
        image: image().optional(),
        imageAlt: z.string().optional(),
        series: z.string().optional(),
        part: z.number().int().positive().optional(),
        featured: z.boolean().default(false),
        /** Drafts are visible in `npm run dev` but excluded from production builds. */
        draft: z.boolean().default(false),
      })
      .refine((d) => !d.image || !!d.imageAlt, {
        message: 'imageAlt is required whenever image is set',
        path: ['imageAlt'],
      }),
});

export const collections = { posts };
