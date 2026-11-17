"""Build canvas/home.html for COP 4610 from index.html, in the style of the
Future Edge Networks canvas/home.html (inline styles, no scripts, absolute links).
Usage: python canvas/build_home.py   (run from the repo root after editing index.html)"""
import re
import sys

repo = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else '.'
BASE = 'https://xinliulab.github.io/FSU-COP4610-Operating-Systems/'
src = open(f'{repo}/index.html', encoding='utf-8').read()

a = src.index('<div class="container">') + len('<div class="container">')
b = src.rindex('</div>', 0, src.index('</body>'))
body = src[a:b]

body = re.sub(r'<!--.*?-->', '', body, flags=re.S)                       # comments
body = re.sub(r'<i class="fa[bsr]? [^"]*"></i>\s?', '', body)            # icons
body = body.replace('</br>', '<br>')
# the demo video opens in a JS dialog on GitHub; on Canvas link the file directly
body = re.sub(r"""<a href="#" onclick="openVideo\('([^']+)'\); return false;">""",
              r'<a href="\1" target="_blank" rel="noopener">', body)
# relative links to absolute GitHub Pages links
body = re.sub(r'href="(?!https?:|mailto:|#)\.?/?([^"]+)"', lambda m: f'href="{BASE}{m.group(1)}"', body)
body = re.sub(r'src="(?!https?:)\.?/?([^"]+)"', lambda m: f'src="{BASE}{m.group(1)}"', body)

# headings
m = re.search(r'<h1>(.*?)</h1>', body, flags=re.S)
title = m.group(1).strip()
body = body[:m.start()] + body[m.end():]
body = re.sub(r'<h2>', '<h2 style="font-size: 22px; margin: 28px 0 10px; padding: 8px 0; border-bottom: 2px solid #ceb888; color: #782f40;">', body)
body = re.sub(r'<h3>', '<h3 style="font-size: 18px; margin: 20px 0 8px; color: #4b5563;">', body)
body = body.replace('<ul class="indented">', '<ul>')

# table
CELL = 'border: 1px solid #d1d5db; padding: 8px'
body = re.sub(r'<table[^>]*>', '<table border="1" cellpadding="6" style="width: 100%; border-collapse: collapse; margin: 12px 0 22px; font-size: 14px; border: 1px solid #d1d5db;">', body)
def cell(m):
    tag, attrs = m.group(1), m.group(2)
    extra = CELL + ('; background: #f3f4f6' if tag == 'th' else '')
    if 'style="' in attrs:
        attrs = re.sub(r'style="([^"]*?);?\s*"', lambda s: f'style="{s.group(1)}; {extra}"', attrs, count=1)
    else:
        attrs = f'{attrs} style="{extra}"'
    return f'<{tag}{attrs}>'
body = re.sub(r'<(th|td)((?:\s[^>]*)?)>', cell, body)

head = f'''<!-- Canvas page body for COP 4610 Operating Systems. Built from ../index.html; paste into Canvas with the HTML editor, or push with push_to_canvas.ps1. -->
<div style="max-width: 1100px; margin: 0 auto; font-family: Arial, Helvetica, sans-serif; line-height: 1.55; color: #1f2937;">
<div style="border: 1px solid #ceb888; border-left: 6px solid #782f40; padding: 14px 16px; margin: 0 0 18px; background: #fffaf0;">
  <p style="margin: 0;"><strong>Course materials:</strong> Lecture slides, demo code, and the syllabus are linked to the public course website, <a href="{BASE}" target="_blank" rel="noopener">{BASE}</a>. Canvas is the course hub for announcements and grades.</p>
</div>
<h1 style="font-size: 28px; line-height: 1.25; margin: 0 0 16px; color: #782f40;">{title}</h1>
'''
out = head + body.strip('\n') + '\n</div>\n'
open(f'{repo}/canvas/home.html', 'w', encoding='utf-8', newline='\n').write(out)
print('title:', title)
print('bytes:', len(out.encode()))
print('left: scripts', out.count('<script'), '| icons', out.count('class="fa'), '| rel links', len(re.findall(r'href="(?!https?:|mailto:|#)', out)), '| onclick', out.count('onclick'))
