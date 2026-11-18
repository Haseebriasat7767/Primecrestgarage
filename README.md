# Primecrest Garage — Luxury Car Repair, Dubai

Where luxury meets precision. A fast, fully responsive one-page site for a luxury
car repair and detailing garage in Al Quoz, Dubai.

## Stack
- Static HTML, hand-written CSS and vanilla JavaScript (no build step, no dependencies)
- Custom gold-on-black crest artwork (SVG + PNG exports in `assets/img/brand/`)
- Original AI-generated photography in `assets/img/`
- Google Fonts: Cormorant Garamond (display) + Jost (interface)

## Structure
```
index.html              all sections + JSON-LD AutoRepair schema
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
