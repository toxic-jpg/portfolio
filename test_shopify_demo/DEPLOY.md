# Deploy test_shopify_demo

## Netlify (drag & drop)
1. Go to app.netlify.com/drop
2. Drag this entire folder (D:\hanibess-automation\portfolio\test_shopify_demo) onto the page
3. Done — live URL in 30 seconds

## Vercel
```bash
cd D:\hanibess-automation\portfolio\test_shopify_demo
npx vercel --prod
```

## GitHub Pages
1. Create repo, push this folder
2. Settings → Pages → Deploy from branch (main)
3. URL: https://yourusername.github.io/repo-name/

## For Shopify Section Builder
- This is a standalone demo. For real Shopify work, you'd create a `sections/` folder in a theme.
- The pattern (schema + render function) maps 1:1 to Shopify Liquid sections.
