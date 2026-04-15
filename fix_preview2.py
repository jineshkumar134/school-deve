import re

with open('global-preview.html', 'r', encoding='utf-8') as f:
    preview_html = f.read()

# Append brand-chip css
brand_chip_css = """
    .brand-chip{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      gap:8px;
      padding:8px 12px;
      border-radius:999px;
      background:var(--primary-soft);
      border:1px solid var(--primary-border);
      color:var(--primary);
      font-size:11px;
      font-weight:600;
      line-height:normal;
    }
"""
# Insert brand-chip css before the first </style>
preview_html = preview_html.replace('</style>', brand_chip_css + '\n</style>', 1)

# Ensure the JS is correctly formatted.
# Wait, let's see if 8de4de5 actually HAS a working generateReport without my intervention.
# I'll just write this restored version back.
with open('global-preview.html', 'w', encoding='utf-8') as f:
    f.write(preview_html)

print("Restored from 8de4de5 and added brand-chip css.")
