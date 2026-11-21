#!/usr/bin/env python3
import re
import os
from collections import defaultdict

# Parse INDEX.md
entries = []
with open('/home/nim/made/INDEX.md', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('('):
            continue
        # Format: - YYYY-MM-DD type: Title (path1, path2...)
        m = re.match(r'- (\d{4}-\d{2}-\d{2}) (\w+): (.+?) \((.+)\)', line)
        if m:
            date, typ, title, paths = m.groups()
            path_list = [p.strip() for p in paths.split(',')]
            entries.append({
                'date': date,
                'type': typ,
                'title': title,
                'paths': path_list
            })
        else:
            # Some entries might not have paths in parens
            m2 = re.match(r'- (\d{4}-\d{2}-\d{2}) (\w+): (.+)', line)
            if m2:
                date, typ, title = m2.groups()
                entries.append({
                    'date': date,
                    'type': typ,
                    'title': title,
                    'paths': []
                })

# Group by type
groups = defaultdict(list)
for e in entries:
    groups[e['type']].append(e)

# Sort each group by date descending
for typ in groups:
    groups[typ].sort(key=lambda x: x['date'], reverse=True)

# Build HTML
html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>nim-the-frog.github.io — sitemap</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      line-height: 1.6;
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1rem;
      color: #1a1a1a;
      background: #fafafa;
    }
    h1 { font-size: 1.5rem; margin-bottom: 0.5rem; }
    .subtitle { color: #666; margin-bottom: 2rem; font-size: 0.9rem; }
    .section { margin-bottom: 3rem; }
    .section h2 {
      font-size: 1.1rem;
      border-bottom: 1px solid #ddd;
      padding-bottom: 0.3rem;
      margin-bottom: 1rem;
      text-transform: capitalize;
    }
    .count { color: #888; font-size: 0.85rem; font-weight: normal; margin-left: 0.5rem; }
    ul { list-style: none; }
    li { margin-bottom: 0.4rem; }
    a { color: #2c5f8a; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .entry { display: flex; gap: 1rem; align-items: baseline; }
    .entry-date { color: #888; font-size: 0.85rem; white-space: nowrap; min-width: 100px; }
    .entry-title { flex: 1; }
    .entry-paths { color: #888; font-size: 0.75rem; font-family: monospace; }
    .nav { margin-bottom: 2rem; padding: 1rem; background: #fff; border: 1px solid #eee; border-radius: 4px; }
    .nav a { margin-right: 1.5rem; font-size: 0.9rem; }
    .nav a:last-child { margin-right: 0; }
    .type-drawing { border-left: 3px solid #c0392b; padding-left: 0.8rem; }
    .type-tune { border-left: 3px solid #27ae60; padding-left: 0.8rem; }
    .type-writing { border-left: 3px solid #8e44ad; padding-left: 0.8rem; }
    .type-contraption { border-left: 3px solid #e67e22; padding-left: 0.8rem; }
  </style>
</head>
<body>
  <h1>nim-the-frog.github.io</h1>
  <p class="subtitle">Everything made so far. %d entries total.</p>
  
  <div class="nav">
''' % len(entries)

# Navigation links
for typ in ['drawing', 'tune', 'writing', 'contraption']:
    if typ in groups:
        html += f'    <a href="#{typ}s">{typ.capitalize()}s ({len(groups[typ])})</a>\n'

html += '''  </div>
'''

# Sections
type_labels = {
    'drawing': 'Drawings',
    'tune': 'Tunes',
    'writing': 'Writing',
    'contraption': 'Contraptions'
}

for typ in ['drawing', 'tune', 'writing', 'contraption']:
    if typ not in groups:
        continue
    html += f'  <div class="section" id="{typ}s">\n'
    html += f'    <h2>{type_labels[typ]} <span class="count">{len(groups[typ])}</span></h2>\n'
    html += '    <ul>\n'
    for e in groups[typ]:
        html += f'      <li class="type-{typ}">\n'
        html += f'        <div class="entry">\n'
        html += f'          <span class="entry-date">{e["date"]}</span>\n'
        html += f'          <span class="entry-title"><a href="made/{e["paths"][0]}" target="_blank">{e["title"]}</a></span>\n'
        if len(e['paths']) > 1:
            paths_str = ', '.join(e['paths'][1:])
            html += f'          <span class="entry-paths">+ {paths_str}</span>\n'
        html += '        </div>\n'
        html += '      </li>\n'
    html += '    </ul>\n'
    html += '  </div>\n'

html += '''</body>
</html>
'''

with open('/home/nim/nim-the-frog.github.io/index.html', 'w') as f:
    f.write(html)

print(f"Generated sitemap with {len(entries)} entries")
for typ in ['drawing', 'tune', 'writing', 'contraption']:
    if typ in groups:
        print(f"  {typ}: {len(groups[typ])}")
