#!/usr/bin/env python3
"""Build the static brand and brand/service pages. Run from any directory."""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://primecrestgarage.ae/'
# Model examples help customers identify their vehicle; availability must be confirmed.
BRANDS = [
 ('Japanese','toyota','Toyota','Camry, Corolla and Land Cruiser'),
 ('Japanese','lexus','Lexus','ES, RX and LX'),
 ('Japanese','nissan','Nissan','Altima, Patrol and X-Trail'),
 ('Japanese','infiniti','Infiniti','Q50, QX60 and QX80'),
 ('Japanese','honda','Honda','Accord, Civic and CR-V'),
 ('Japanese','mazda','Mazda','Mazda3, Mazda6 and CX-5'),
 ('Japanese','mitsubishi','Mitsubishi','Pajero, Outlander and Lancer'),
 ('Japanese','subaru','Subaru','Forester, Outback and WRX'),
 ('American','ford','Ford','Mustang, Explorer and F-150'),
 ('American','chevrolet','Chevrolet','Tahoe, Camaro and Silverado'),
 ('American','cadillac','Cadillac','Escalade, XT5 and CT5'),
 ('American','jeep','Jeep','Wrangler, Grand Cherokee and Gladiator'),
 ('American','dodge','Dodge','Charger, Challenger and Durango'),
 ('American','gmc','GMC','Yukon, Sierra and Acadia'),
 ('German','mercedes-benz','Mercedes-Benz','C-Class, E-Class and G-Class'),
 ('German','bmw','BMW','3 Series, 5 Series and X5'),
 ('German','audi','Audi','A4, A6 and Q7'),
 ('German','porsche','Porsche','911, Cayenne and Macan'),
 ('German','volkswagen','Volkswagen','Golf, Tiguan and Touareg'),
 ('Korean','hyundai','Hyundai','Elantra, Tucson and Santa Fe'),
 ('Korean','kia','Kia','Sportage, Sorento and Carnival'),
 ('Korean','genesis','Genesis','G70, G80 and GV80'),
]
# Each service has its own practical guidance. Edit these alongside the main service pages.
SERVICES = [
 dict(slug='mechanical-electrical-repairs', name='Mechanical & Electrical Repair', short='mechanical and electrical repairs', image='service-mechanical.jpg',
  intro='Unusual noises, leaks, warning messages or intermittent electrical problems can have more than one cause. An inspection helps establish the appropriate next step before parts are replaced.',
  checks=[('Describe the symptoms','Tell us when the issue occurs, whether the vehicle is hot or cold, and which warning messages appear.'),('Inspect and trace','The team can inspect the relevant mechanical components, wiring or sensors and discuss any further testing needed.'),('Agree on the repair','Once the fault is understood, ask for the proposed work, parts and estimate before authorising repairs.')],
  question='Can an electrical fault cause a mechanical symptom?', answer='Yes. Sensors and control systems can affect how a vehicle runs, but mechanical faults can produce similar symptoms. Testing helps distinguish the cause.'),
 dict(slug='auto-body-shop', name='Body Repair & Paint', short='body repair and paintwork', image='service-body.jpg',
  intro='Dents, scratches and damaged panels call for an assessment of both the surface and the underlying panel. The repair method depends on the damage, material and finish.',
  checks=[('Assess the damage','Share photos or bring the vehicle in so the affected panels and surrounding areas can be inspected.'),('Plan the repair','Discuss panel repair, preparation and paint matching as appropriate to the damage.'),('Review the finish','The scope, timing and final checks depend on the repair; ask your advisor what is included in the estimate.')],
  question='Can a scratched panel be repaired without repainting?', answer='That depends on how deep the scratch is and the condition of the finish. An inspection is needed to determine the suitable approach.'),
 dict(slug='engine-diagnostics', name='Engine Diagnostics', short='engine diagnostics and check engine light inspection', image='service-diagnostics.jpg',
  intro='A check engine light is a reason to investigate, not a diagnosis by itself. Fault codes and the way the vehicle behaves help guide further checks.',
  checks=[('Record the warning','Note whether the light is steady or flashing and whether there is loss of power, overheating or unusual noise.'),('Read and interpret codes','A diagnostic scan identifies stored information; related tests may be necessary to establish the underlying cause.'),('Discuss the findings','Your advisor can explain the results and whether additional testing or repairs are recommended.')],
  question='Is it safe to drive with the check engine light on?', answer='A flashing light, overheating or serious loss of power can indicate a serious problem. Stop safely and seek assistance; even a steady light should be checked promptly.'),
 dict(slug='brake-repair-suspension', name='Brake & Suspension Repair', short='brake and suspension inspection and repair', image='service-brakes.jpg',
  intro='Braking, steering and ride quality can change as components wear. An inspection can help identify the source of vibration, noise or uneven handling.',
  checks=[('Check the symptoms','Report squealing, grinding, a changed pedal feel, pulling or knocking over bumps.'),('Inspect affected components','Brake and suspension components can be checked for wear or damage; alignment may also be considered when relevant.'),('Plan the work','The appropriate parts and checks depend on the vehicle and the condition found during inspection.')],
  question='When should brakes be inspected?', answer='Arrange an inspection promptly for a warning light, grinding, vibration or a change in braking feel. If braking feels unsafe, stop safely and seek assistance.'),
 dict(slug='ceramic-coating-paint-protection-film', name='Ceramic Coating & PPF', short='ceramic coating and paint protection film', image='service-ceramic.jpg',
  intro='Ceramic coating and paint protection film serve different purposes. The best coverage depends on the finish, how the vehicle is used and the protection you want.',
  checks=[('Assess the paint','Existing marks and the condition of the finish determine the preparation needed before protection.'),('Choose the protection','A coating can add gloss and make cleaning easier; PPF provides a physical layer against chips and abrasion.'),('Discuss coverage and care','Choose areas to protect and ask about the maintenance required for the selected product.')],
  question='Does ceramic coating prevent stone chips?', answer='Ceramic coating is not a substitute for a physical film against stone chips. PPF is designed to provide a protective layer, though no protection prevents all damage.'),
 dict(slug='interior-restoration-detailing', name='Interior Detailing & Restoration', short='interior detailing and restoration', image='service-interior.jpg',
  intro='Cabin materials need different treatments. Leather, fabric, Alcantara and trim should be assessed for condition before cleaning or restoration is planned.',
  checks=[('Inspect the cabin','Identify the surfaces and areas of concern, such as staining, worn bolsters or marked trim.'),('Select material-appropriate care','The cleaning or restoration approach depends on the material and its condition.'),('Discuss further work','For significant wear, ask about restoration or re-trimming options and their scope before proceeding.')],
  question='Can worn leather be restored?', answer='Some wear may respond to restoration, while more extensive damage may require re-trimming. The options depend on an inspection of the material.'),
 dict(slug='transmission-engine-repairs', name='Engine & Transmission Repair', short='engine and transmission repair', image='service-transmission.jpg',
  intro='A change in shifting, power delivery or engine sound warrants a careful assessment. The right repair depends on the fault and the vehicle’s engine and transmission.',
  checks=[('Describe the concern','Note whether symptoms appear during starting, acceleration, gear changes or at a particular temperature.'),('Diagnose before repair','Inspection and relevant diagnostic information help establish whether further testing is needed.'),('Review the estimate','Discuss the proposed repair, parts and expected timing after the issue has been assessed.')],
  question='What can indicate a transmission problem?', answer='Slipping, delayed engagement, rough shifts or unusual noises can indicate a fault. If symptoms are severe, avoid driving and seek assistance.'),
 dict(slug='body-kits-customisation', name='Body Kits & Customisation', short='body kits and exterior customisation', image='service-bodykit.jpg',
  intro='Exterior modifications should be planned around the exact model, model year and components. Fitment and finish matter as much as the intended look.',
  checks=[('Confirm compatibility','Share your vehicle details and the specific kit or components you are considering.'),('Plan fitment and finish','Discuss panel fit, preparation and finishing needs before installation is agreed.'),('Check requirements','Modifications may be subject to local rules and approvals; check the applicable requirements before proceeding.')],
  question='Will any body kit fit my vehicle?', answer='No. Compatibility depends on the exact model, year, trim and kit. Confirm fitment before buying or installing components.'),
]

def e(text): return escape(text, quote=True)
def path_prefix(depth): return '../' * depth

def shell(depth):
    # Reuse the existing site's navigation and icons, with links rebased to this depth.
    sample = (ROOT/'services/engine-diagnostics/index.html').read_text()
    sprite = sample[sample.index('<!-- ============ ICON SPRITE'):sample.index('<!-- ============ HEADER')]
    header = sample[sample.index('<!-- ============ HEADER'):sample.index('</header>', sample.index('<!-- ============ HEADER'))+len('</header>')]
    footer = sample[sample.index('<!-- ============ FOOTER'):sample.index('<script src="../../assets/js/main.js"')]
    return sprite, header.replace('../../', path_prefix(depth)), footer.replace('../../', path_prefix(depth))

def make_page(path, title, desc, image, body, crumbs, schema_type=None, service_name=None):
    depth = len(Path(path).parts)
    prefix = path_prefix(depth)
    url = DOMAIN + path + '/'
    sprite, header, footer = shell(depth)
    breadcrumb_items = [{'@type':'ListItem','position':i+1,'name':name,'item':link} for i,(name,link) in enumerate(crumbs)]
    graph = [{'@type':'BreadcrumbList','itemListElement':breadcrumb_items}]
    if schema_type:
        graph.append({'@type':'Service','name':service_name,'description':desc,'url':url,'areaServed':{'@type':'City','name':'Dubai'},'provider':{'@type':'AutoRepair','name':'Primecrest Garage','url':DOMAIN,'telephone':'+971568778354','address':{'@type':'PostalAddress','streetAddress':'First Al Khail Street, Al Quoz Industrial Area 1','addressLocality':'Dubai','addressCountry':'AE'}}})
    schema = json.dumps({'@context':'https://schema.org','@graph':graph}, ensure_ascii=False).replace('</','<\\/')
    head = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#070708">
<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="Primecrest Garage">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}assets/img/{image}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{DOMAIN}assets/img/{image}">
<link rel="icon" href="{prefix}assets/img/brand/favicon-64.png" sizes="64x64" type="image/png"><link rel="apple-touch-icon" href="{prefix}assets/img/brand/apple-touch-icon.png"><link rel="manifest" href="{prefix}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="{prefix}assets/css/style.css">
<script type="application/ld+json">{schema}</script></head><body><a class="skip-link" href="#main">Skip to content</a>
'''
    dest = ROOT/path/'index.html'; dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(head+sprite+header+'\n<main id="main">\n'+body+'\n</main>\n'+footer+f'<script src="{prefix}assets/js/main.js" defer></script>\n</body></html>\n')
    return url

def breadcrumb(links):
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">'+'<span aria-hidden="true">/</span>'.join(f'<a href="{e(href)}">{e(name)}</a>' if href else f'<span aria-current="page">{e(name)}</span>' for name,href in links)+'</nav>'

def hero(prefix, image, alt, links, eyebrow, h1, intro):
    return f'''<section class="service-detail-hero"><img class="service-detail-hero-image" src="{prefix}assets/img/{image}" alt="{e(alt)}" width="900" height="491" fetchpriority="high"><div class="container service-detail-hero-content">{breadcrumb(links)}<p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1><p class="service-detail-lead">{e(intro)}</p><div class="service-detail-actions"><a class="btn btn-gold" href="{prefix}#contact">Request an appointment</a><a class="btn btn-ghost" href="tel:+971568778354">Call +971 56 877 8354</a></div></div></section>'''

def cta(prefix):
    return f'''<section class="service-detail-cta"><div class="container"><p class="eyebrow">Visit us in Al Quoz</p><h2>Let's talk about <em>your car.</em></h2><p>Share your model, year and requirements. Our service advisors can confirm availability and discuss the next step.</p><a class="btn btn-gold" href="{prefix}#contact">Contact our team</a></div></section>'''

def links_grid(links):
    return '<div class="service-detail-links">'+''.join(f'<a href="{e(url)}">{e(text)} <span aria-hidden="true">↗</span></a>' for text,url in links)+'</div>'

urls=[]
# A crawlable directory, organised by country of brand origin.
groups=[]
for country in ('Japanese','American','German','Korean'):
    links=[(name, f'{slug}/') for group,slug,name,models in BRANDS if group==country]
    groups.append(f'<section class="brand-group"><h2>{country} <em>brands.</em></h2>{links_grid(links)}</section>')
body=hero('../','about.jpg','Primecrest Garage service bay',[('Home','../'),('Brands',None)],'Find your marque','Car Services by Brand in Dubai','Explore services for Japanese, American, German and Korean car brands. Contact our Al Quoz team to confirm availability for your vehicle and the work you need.')
body+='<div class="section"><div class="container">'+''.join(groups)+'</div></div>'+cta('../')
urls.append(make_page('brands','Car Services by Brand in Dubai | Primecrest Garage','Explore car repair, diagnostics, bodywork and detailing by brand in Al Quoz, Dubai. Enquire about Japanese, American, German and Korean vehicles.','about.jpg',body,[('Home',DOMAIN),('Brands',DOMAIN+'brands/')]))
for country,slug,name,models in BRANDS:
    base=f'brands/{slug}'
    hub_url=DOMAIN+base+'/'
    title=f'{name} Car Repair & Services Dubai | Primecrest Garage'
    desc=f'Explore {name} car repair, diagnostics, bodywork and detailing in Al Quoz, Dubai. Contact Primecrest Garage to discuss your model and service needs.'
    intro=f'Looking for {name} car care in Dubai? Explore our services for {name} vehicles and speak to our Al Quoz team about your model, its condition and the work you need.'
    body=hero('../../','service-mechanical.jpg','Technician working on a car engine',[('Home','../../'),('Brands','../'),(name,None)],f'{country} vehicles · Al Quoz, Dubai',f'{name} Car Services in Dubai',intro)
    body+=f'''<section class="section"><div class="container"><header class="section-head"><p class="eyebrow">Choose a service</p><h2>Care for your <em>{e(name)}.</em></h2><p class="section-sub">From diagnostics and repair to paint and cabin care, explore the options below. Tell us your exact model and year so we can confirm availability.</p></header>{links_grid([(s['name'],s['slug']+'/') for s in SERVICES])}<p class="brand-note">Own a {e(name)}, such as the {e(models)}? Service needs vary by model, year, engine and condition. Contact us to discuss your vehicle and confirm availability. Brand names are used for identification; no manufacturer affiliation is claimed.</p><p class="brand-back"><a class="link-arrow" href="../">← Browse all brands</a></p></div></section>'''+cta('../../')
    urls.append(make_page(base,title,desc,'service-mechanical.jpg',body,[('Home',DOMAIN),('Brands',DOMAIN+'brands/'),(name,hub_url)]))
    for s in SERVICES:
        path=base+'/'+s['slug']; url=DOMAIN+path+'/'
        stitle=f'{name} {s["name"]} Dubai | Primecrest Garage'
        desc=f'{name} {s["short"]} in Al Quoz, Dubai. Contact Primecrest Garage to discuss your model, service needs and availability.'
        intro=f'Need {s["short"]} for your {name} in Dubai? {s["intro"]}'
        body=hero('../../../',s['image'],'Automotive service at Primecrest Garage',[('Home','../../../'),('Brands','../../'),(name,'../'),(s['name'],None)],f'{name} services · Al Quoz, Dubai',f'{name} {s["name"]} in Dubai',intro)
        cards=''.join(f'<article class="service-detail-item"><span>0{i}</span><h3>{e(h)}</h3><p>{e(text)}</p></article>' for i,(h,text) in enumerate(s['checks'],1))
        body+=f'''<section class="section"><div class="container"><header class="section-head"><p class="eyebrow">What to expect</p><h2>A considered approach to <em>your {e(name)}.</em></h2><p class="section-sub">Every job starts with the vehicle and your concerns. The actual work depends on an assessment and your approval.</p></header><div class="service-detail-grid">{cards}</div><p class="brand-note">For a {e(name)} such as the {e(models)}, tell us the model year, engine and symptoms or goals. Requirements and availability vary; please contact our team to confirm. Brand names are used for identification; no manufacturer affiliation is claimed.</p></div></section>'''
        body+=f'''<section class="section service-detail-faq"><div class="container service-detail-faq-layout"><div><p class="eyebrow">Helpful information</p><h2>Questions, <em>answered.</em></h2><p class="section-sub">Talk to our advisors about your specific vehicle.</p></div><div><div class="service-faq-item"><h3>{e(s['question'])}</h3><p>{e(s['answer'])}</p></div><div class="service-faq-item"><h3>How much will this service cost for my {e(name)}?</h3><p>The price depends on the model, condition, parts and scope of work. Contact us with your vehicle details; an inspection may be needed before an estimate.</p></div></div></div></section>'''
        other=[x for x in SERVICES if x['slug']!=s['slug']][:3]
        body+=f'''<section class="section service-detail-related"><div class="container"><p class="eyebrow">Explore more</p><h2>More care for your <em>{e(name)}.</em></h2>{links_grid([(x['name'],'../'+x['slug']+'/') for x in other])}<a class="link-arrow" href="../">View all {e(name)} services →</a><p class="brand-back"><a class="link-arrow" href="../../../services/{s['slug']}/">About {e(s['name'])} →</a></p></div></section>'''+cta('../../../')
        urls.append(make_page(path,stitle,desc,s['image'],body,[('Home',DOMAIN),('Brands',DOMAIN+'brands/'),(name,hub_url),(s['name'],url)],True,f'{name} {s["name"]}'))
# Keep the established home and service URLs; regenerate the complete sitemap deterministically.
existing=[DOMAIN]+[DOMAIN+'services/'+s['slug']+'/' for s in SERVICES]
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ns='http://www.sitemaps.org/schemas/sitemap/0.9'; root=ET.Element(f'{{{ns}}}urlset')
for url in existing+urls:
    entry=ET.SubElement(root,f'{{{ns}}}url'); ET.SubElement(entry,f'{{{ns}}}loc').text=url
ET.indent(root,space='  ')
ET.ElementTree(root).write(ROOT/'sitemap.xml',encoding='UTF-8',xml_declaration=True)
print(f'Generated {len(urls)} brand pages; sitemap contains {len(existing)+len(urls)} URLs.')
