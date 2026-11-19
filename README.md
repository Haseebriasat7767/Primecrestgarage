# Primecrest Garage — Luxury Car Repair, Dubai

Where luxury meets precision. A fast, fully responsive static site for a luxury
car repair and detailing garage in Al Quoz, Dubai.

## Stack
- Static HTML, hand-written CSS and vanilla JavaScript (no build step, no dependencies)
- Custom gold-on-black crest artwork (SVG + PNG exports in `assets/img/brand/`)
- Original AI-generated photography in `assets/img/`
- Google Fonts: Cormorant Garamond (display) + Jost (interface)

## Structure
```
index.html              home page + JSON-LD AutoRepair schema
services/*/index.html   dedicated, indexable service pages with Service and breadcrumb schema
brands/                 brand directory, brand hubs and brand-specific service pages
scripts/generate_brand_pages.py   data and generator for brand pages and sitemap
assets/css/style.css    design system, layout, responsive rules
assets/js/main.js       sticky nav, reveals, counters, marquee, carousel, FAQ, form
assets/img/             photography + optimised JPGs
assets/img/brand/       crest + horizontal / stacked lockups (transparent + on black)
robots.txt, sitemap.xml, site.webmanifest
```

## Run locally
```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Notes
- The booking form has no backend: it validates, then composes a WhatsApp message
  with the entered details. Point `WhatsAppNumber` in `assets/js/main.js` at the
  live number (currently +971 56 877 8354). Address on file: First Al Khail
  Street, Al Quoz Industrial Area 1, Dubai.
- SEO title: **Primecrest Garage | Luxury Car Repair Dubai**.

Each service has a dedicated static page linked from the home page and listed in `sitemap.xml`. Update page copy, metadata, structured data and sitemap URLs together when services or the production domain change. Submit the sitemap to search engines after deployment; rankings are not guaranteed.

## Brand pages

The brand directory covers Japanese, American, German and Korean marques. Brand hubs link to eight individual service pages each. To update the brand list, model examples, service guidance or generated page layout, edit `scripts/generate_brand_pages.py` and run `python3 scripts/generate_brand_pages.py`. This also regenerates `sitemap.xml` and uses the existing service page for shared navigation and footer markup. Generated HTML is committed so the site remains deployable without a build step. Confirm actual brand, model and service availability with the garage before publishing, and review the pages for unique, accurate business-specific information; generating pages alone does not guarantee indexing or rankings.

Run `python3 scripts/check_site.py` to validate page metadata, JSON-LD, local links and sitemap coverage.
