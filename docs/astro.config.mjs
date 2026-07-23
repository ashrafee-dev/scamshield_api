// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'ScamShield Documentation',

      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/<your-github-username>/<your-repo>',
        },
      ],

      sidebar: [
        {
          label: 'Guides',
          items: [
            {
              label: 'Quick Start',
              slug: 'guides/quickstart',
            },
          ],
        },
        {
          label: 'Reference',
          items: [
            {
              autogenerate: {
                directory: 'reference',
              },
            },
          ],
        },
      ],
    }),
  ],
});
