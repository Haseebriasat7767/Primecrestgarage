#!/usr/bin/env python3
"""Check the generated static pages, structured data, links and sitemap."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / 'index.html', *ROOT.glob('services/*/index.html'), *ROOT.glob('brands/**/index.html')]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.canonicals, self.descriptions, self.schemas = set(), [], [], [], []
        self.headings = self.titles = 0
        self.in_schema, self.data = False, ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'h1': self.headings += 1
        if tag == 'title': self.titles += 1
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a.get('href'))
        if tag == 'meta' and a.get('name') == 'description': self.descriptions.append(a.get('content'))
        if tag == 'script' and a.get('type') == 'application/ld+json': self.in_schema, self.data = True, ''
        self.refs.extend(a[k] for k in ('href', 'src') if k in a)

    def handle_data(self, data):
        if self.in_schema: self.data += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.schemas.append(json.loads(self.data))
            self.in_schema = False

parsed = {}
for path in PAGES:
    page = Page()
    page.feed(path.read_text())
    assert page.headings == page.titles == len(page.canonicals) == len(page.descriptions) == 1 and page.schemas, path
    parsed[path] = page

errors = []
for path, page in parsed.items():
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir(): target /= 'index.html'
        if not target.exists(): errors.append(f'{path.relative_to(ROOT)}: missing {ref}')
        elif url.fragment and target in parsed and url.fragment not in parsed[target].ids:
            errors.append(f'{path.relative_to(ROOT)}: missing fragment {ref}')

namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').getroot().findall(f'{namespace}url/{namespace}loc')]
canonicals = [page.canonicals[0] for page in parsed.values()]
assert len(urls) == len(set(urls)) == len(parsed) and set(urls) == set(canonicals), 'Sitemap and canonical URLs disagree'
assert not errors, '\n'.join(errors)
print(f'Validated {len(parsed)} pages, metadata, JSON-LD, sitemap and local links.')
