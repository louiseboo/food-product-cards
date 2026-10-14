#!/usr/bin/env python3
"""Render approved product data to a standalone offline HTML deck."""
import base64
import html
import json
from pathlib import Path
import sys

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
MIMES = {'.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}


def esc(value):
    return html.escape(str(value), quote=True)


def required(data, keys):
    for key in keys:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError('Missing non-empty text: ' + key)


def image_uri(path):
    if path.suffix.lower() not in MIMES:
        raise ValueError('Unsupported image: ' + str(path))
    raw = path.read_bytes()
    if not raw:
        raise ValueError('Empty image: ' + str(path))
    return 'data:' + MIMES[path.suffix.lower()] + ';base64,' + base64.b64encode(raw).decode()


def render(data, base):
    required(data, ['title'])
    products = data.get('products', [])
    if not isinstance(products, list) or not products:
        raise ValueError('products must be a non-empty list')
    by_id = {}
    for p in products:
        required(p, ['id', 'name', 'subtitle', 'photo', 'diagram'])
        if p['id'] in by_id:
            raise ValueError('Duplicate product id')
        by_id[p['id']] = p
        if p.get('kind', 'food') not in ('food', 'beverage'):
            raise ValueError('Unknown product kind')
        sections = p.get('sections', [])
        if len(sections) != 3:
            raise ValueError('Three complete copy sections required')
        for section in sections:
            required(section, ['heading', 'title', 'body'])
        labels = p.get('labels', [])
        if p.get('kind', 'food') == 'food' and len(labels) < 2:
            raise ValueError('Food needs at least two layer labels')
        for label in labels:
            required(label, ['text'])
            y = label.get('y')
            if isinstance(y, bool) or not isinstance(y, (int, float)) or not 0 <= y <= 95:
                raise ValueError('Label y must be 0–95')
    logo = image_uri(ASSETS / 'peets-coffee-cream.svg')
    def header(title, subtitle):
        return '<header><section><h1>' + esc(title) + '</h1><p>' + esc(subtitle) + '</p></section><section class="brand"><img src="' + logo + '" alt="Peet’s Coffee"></section></header>'
    pages, order = [], []
    groups = data.get('menu', [])
    if len(groups) > 3:
        raise ValueError('Split menu: maximum three groups per page')
    if groups:
        columns = []
        for group in groups:
            required(group, ['title'])
            items = group.get('items', [])
            if not 1 <= len(items) <= 6:
                raise ValueError('Split menu: one to six items per group')
            rows = []
            for item in sorted(items, key=lambda item: not bool(item.get('new'))):
                required(item, ['product_id', 'price'])
                pid = item['product_id']
                if pid not in by_id:
                    raise ValueError('Unknown menu product: ' + pid)
                if pid not in order:
                    order.append(pid)
                badges = ('<span class="badge new-badge">New</span>' if item.get('new') else '') + ('<span class="badge core-badge">Core</span>' if item.get('core') else '')
                rows.append('<section class="menu-row"><aside class="badges">' + badges + '</aside><section class="menu-top"><strong>' + esc(by_id[pid]['name']) + '</strong><span class="price">' + esc(item['price']) + '</span></section><p class="menu-bottom">' + esc(item.get('note', '')) + '</p></section>')
            columns.append('<section class="menu-col"><h2 class="category">' + esc(group['title']) + '</h2>' + ''.join(rows) + '</section>')
        pages.append('<article class="slide">' + header(data['title'], data.get('menu_subtitle', '')) + '<main class="menu-grid">' + ''.join(columns) + '</main></article>')
    order += [p['id'] for p in products if p['id'] not in order]
    for pid in order:
        p = by_id[pid]
        labels = ''.join('<li style="top:' + str(x['y']) + '%">' + esc(x['text']) + '</li>' for x in p.get('labels', []))
        copy = ''.join('<section><h2>' + esc(x['heading']) + '</h2><h3>' + esc(x['title']) + '</h3><p>' + esc(x['body']) + '</p></section>' for x in p['sections'])
        photo, diagram = (image_uri(base / p[k]) for k in ('photo', 'diagram'))
        pages.append('<article class="slide" id="' + esc(pid) + '">' + header(p['name'], p['subtitle']) + '<main class="cake-grid new-product"><section class="photo-frame"><img src="' + photo + '" alt="' + esc(p['name']) + '"></section><section class="diagram-wrap"><img src="' + diagram + '" alt="' + esc(p['name']) + '配图"><ol class="layer-labels">' + labels + '</ol></section><aside class="copy">' + copy + '</aside></main></article>')
    nav = '<nav class="deck-controls" aria-label="翻页"><button id="prev" aria-label="上一页">←</button><span id="counter"></span><button id="next" aria-label="下一页">→</button></nav>'
    script = '''<script>(()=>{const slides=[...document.querySelectorAll('.slide')],prev=document.querySelector('#prev'),next=document.querySelector('#next'),counter=document.querySelector('#counter');let i=0;function update(){counter.textContent=`${i+1} / ${slides.length}`;prev.disabled=i===0;next.disabled=i===slides.length-1}function show(n){i=Math.max(0,Math.min(n,slides.length-1));slides[i].scrollIntoView();update()}prev.onclick=()=>show(i-1);next.onclick=()=>show(i+1);document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown','ArrowLeft','PageUp','Home','End'].includes(e.key)){e.preventDefault();show(e.key==='Home'?0:e.key==='End'?slides.length-1:i+(['ArrowRight','PageDown'].includes(e.key)?1:-1))}});addEventListener('scroll',()=>{i=slides.reduce((a,s,j)=>Math.abs(s.getBoundingClientRect().top)<Math.abs(slides[a].getBoundingClientRect().top)?j:a,0);update()});update()})();</script>'''
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(data['title']) + '</title><style>' + (ASSETS / 'cards.css').read_text() + '</style></head><body>' + ''.join(pages) + nav + script + '</body></html>'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: render.py input.json output.html')
    source, target = map(Path, sys.argv[1:])
    try:
        result = render(json.loads(source.read_text(encoding='utf-8')), source.resolve().parent)
        target.write_text(result, encoding='utf-8')
    except (ValueError, KeyError, TypeError, OSError) as error:
        sys.exit(str(error))
    print(str(target.resolve()))
