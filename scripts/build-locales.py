"""Generate crawlable English pages from root Chinese HTML and the translation map.
Run: python3 scripts/build-locales.py
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'about.html', 'models.html', 'notes.html', 'research.html', 'why-anthesis.html']
ORIGIN = 'https://anthesis.ac.cn'
TRANSLATIONS = json.loads((ROOT / 'assets/translations-en.json').read_text())

def url(name, english=False):
    return ORIGIN + ('/en/' if english else '/') + ('' if name == 'index.html' else name)

def translate(value):
    if isinstance(value, list): return [translate(item) for item in value]
    if not isinstance(value, str): return value
    key = value.strip()
    return value.replace(key, TRANSLATIONS[key]) if key in TRANSLATIONS else value

def switch(name, english):
    zh = '../' + name if english else './' + name
    en = './' + name if english else './en/' + name
    return ('<div class="language-options" role="group" aria-label="Language / 语言">'
            f'<a href="{zh}" data-language="zh" lang="zh-CN"' + (' aria-current="true"' if not english else '') + '>中文</a>'
            f'<a href="{en}" data-language="en" lang="en"' + (' aria-current="true"' if english else '') + '>English</a></div>')

class EnglishPage(HTMLParser):
    def __init__(self, name):
        super().__init__(convert_charrefs=False)
        self.name, self.output, self.script = name, [], None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script': self.script = attrs.get('type', 'javascript')
        if tag == 'html': attrs['lang'] = 'en'
        for key, value in list(attrs.items()):
            if value is None: continue
            if key in ('aria-label', 'title', 'alt', 'content'): attrs[key] = translate(value)
            if key in ('href', 'src', 'srcset') and re.match(r'(?:\./)?(?:assets/|style\.css|language\.js)', value):
                attrs[key] = '../' + value.removeprefix('./')
        if tag == 'link' and attrs.get('rel') == 'canonical': attrs['href'] = url(self.name, True)
        if tag == 'meta' and attrs.get('property') == 'og:url': attrs['content'] = url(self.name, True)
        self.output.append('<' + tag + ''.join(' ' + k + ('' if v is None else '="' + escape(v, quote=True) + '"') for k,v in attrs.items()) + '>')
    def handle_endtag(self, tag):
        self.output.append('</' + tag + '>')
        if tag == 'script': self.script = None
    def handle_data(self, data):
        if self.script == 'application/ld+json':
            structured = json.loads(data)
            for item in structured.get('@graph', []):
                if item.get('@type') in ('WebPage', 'ProfilePage', 'CollectionPage', 'Article'):
                    item['url'] = url(self.name, True)
                    item['@id'] = url(self.name, True) + ('#' + item['@id'].split('#', 1)[1] if '#' in item.get('@id', '') else '')
                    if 'mainEntityOfPage' in item:
                        item['mainEntityOfPage'] = {'@id': url(self.name, True)}
                    item['inLanguage'] = 'en'
                for key in ('name', 'headline', 'description', 'jobTitle'):
                    if key in item: item[key] = translate(item[key])
            data = json.dumps(structured, ensure_ascii=False, separators=(',', ':'))
        elif not self.script: data = escape(translate(unescape(data)), quote=False)
        self.output.append(data)
    def handle_entityref(self, name): self.output.append('&' + name + ';')
    def handle_charref(self, name): self.output.append('&#' + name + ';')
    def handle_decl(self, decl): self.output.append('<!' + decl + '>')
    def handle_comment(self, data): self.output.append('<!--' + data + '-->')

for name in PAGES:
    path = ROOT / name
    source = path.read_text()
    source = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', '', source)
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{lang}" href="{target}">' for lang,target in [('zh-CN',url(name)),('en',url(name,True)),('x-default',url(name))])
    source = re.sub(r'(<link rel="canonical"[^>]+>)', lambda m:m[0]+'\n'+alternates, source)
    source = re.sub(r'<div class="language-options".*?</div>', switch(name,False), source)
    for asset in ('style.css','language.js'):
        digest = hashlib.sha256((ROOT / asset).read_bytes()).hexdigest()[:12]
        source = re.sub(re.escape(asset)+r'\?v=[a-f0-9]+',asset+'?v='+digest,source)
    path.write_text(source)
    parser = EnglishPage(name)
    parser.feed(source)
    english = ''.join(parser.output)
    english = re.sub(r'<div class="language-options".*?</div>', switch(name,True), english)
    english = english.replace('<span class="language-current">中文</span>', '<span class="language-current">English</span>')
    (ROOT / 'en' / name).write_text(english)

# Dates are omitted so regeneration never implies a content change that did not occur.
locations = [url(name, english) for name in PAGES for english in (False,True)]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+loc+'</loc></url>\n' for loc in locations)+'</urlset>\n')
print('Generated 6 English pages and 12 sitemap entries.')
