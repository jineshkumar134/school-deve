import os
import re

# Mapping of labels to Lucide icon names
label_to_lucide = {
    "module completion": "clipboard-list",
    "total goals": "target",
    "high priority": "flame",
    "kpis set": "trending-up",
    "timeline coverage": "calendar",
    "values added": "lightbulb",
    "culture themes": "school",
    "revision entries": "history",
    "infrastructure rows": "building",
    "academic offerings": "book-open",
    "campus readiness": "settings",
    "competitors tracked": "building-2",
    "opportunities / threats": "trending-up",
    "market pressure": "zap",
    "total actions": "clipboard-check",
    "in progress": "zap",
    "completed": "check-circle",
    "task coverage": "target",
    "active blocker": "alert-circle",
    "saved records": "folder-search",
    "pending modules": "clock",
    "completed modules": "check-circle",
    "overall completion": "clipboard-check",
    "combined completion": "clipboard-check",
    "leadership roles": "user-check",
    "committees": "users",
    "monitoring logs": "file-text",
    "review log count": "file-text",
    "school readiness": "graduation-cap",
    "goals & actions": "target",
    "opportunities": "zap",
    "threats": "shield-alert",
    "strengths": "trending-up",
    "weaknesses": "trending-down",
}

path = os.getcwd()

def upgrade_file(content):
    # 1. Add Lucide CDN and alignment styles if missing
    if 'lucide@latest' not in content:
        head_end = content.find('</head>')
        lucide_assets = '  <script src="https://unpkg.com/lucide@latest"></script>\n'
        lucide_assets += '  <style>.lucide { vertical-align: middle; margin-right: 4px; display: inline-block; }</style>\n'
        content = content[:head_end] + lucide_assets + content[head_end:]

    # Ensure styles are there even if CDN was already there
    if '<style>.lucide' not in content:
        head_end = content.find('</head>')
        content = content[:head_end] + '  <style>.lucide { vertical-align: middle; margin-right: 4px; display: inline-block; }</style>\n' + content[head_end:]

    # 2. Replace icons in stat-icon divs
    # (Existing logic...)
    
    # 3. Handle H3 headers (SWOT specific)
    pattern_h3 = r'(<h3>)([^<]*)(Strengths|Weaknesses|Opportunities|Threats)([^<]*)(</h3>)'
    def replace_h3(match):
        tag_start = match.group(1)
        label = match.group(3) # e.g. "Strengths"
        rest = match.group(4) # e.g. " <span>(Internal)</span>"
        tag_end = match.group(5)
        icon_name = label_to_lucide.get(label.lower(), "info")
        return f'{tag_start}<i data-lucide="{icon_name}" size="20"></i> {label}{rest}{tag_end}'
    
    content = re.sub(pattern_h3, replace_h3, content, flags=re.IGNORECASE)

    # (Previous replacement patterns for stat-icon...)
    pattern_normal = r'(<div class="stat-label">([^<]+)</div>\s*<div class="stat-icon[^>]*>)([^<]*)(</div>)'
    def replace_normal(match):
        prefix = match.group(1)
        label = match.group(2).lower().strip()
        suffix = match.group(4)
        icon_name = label_to_lucide.get(label, "info")
        return f'{prefix}<i data-lucide="{icon_name}"></i>{suffix}'

    pattern_rev = r'(<div class="stat-icon[^>]*>)([^<]*)(</div>\s*</div>\s*(<div[^>]*>\s*)?<div class="stat-label">([^<]+)</div>)'
    def replace_rev(match):
        prefix = match.group(1)
        suffix = match.group(3)
        middle = match.group(4) or ""
        label = match.group(5).lower().strip()
        icon_name = label_to_lucide.get(label, "info")
        return f'{prefix}<i data-lucide="{icon_name}"></i>{suffix}{middle}<div class="stat-label">{match.group(5)}</div>'

    new_content = re.sub(pattern_normal, replace_normal, content, flags=re.IGNORECASE | re.DOTALL)
    new_content = re.sub(pattern_rev, replace_rev, new_content, flags=re.IGNORECASE | re.DOTALL)

    # 4. Initialize Lucide at the end of the script
    if 'lucide.createIcons()' not in new_content:
        script_end = new_content.rfind('</script>')
        if script_end != -1:
            # Check if there is already a script block we can append to
            new_content = new_content[:script_end] + '\n    lucide.createIcons();\n  ' + new_content[script_end:]
        else:
            # Add dynamic script if no script tags exist (unlikely in this project)
            new_content = new_content + '\n<script>lucide.createIcons();</script>'

    return new_content

for filename in os.listdir(path):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(path, filename)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    upgraded_content = upgrade_file(content)

    if upgraded_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(upgraded_content)
        print(f"Upgraded to Lucide: {filename}")

print("Global Lucide upgrade complete.")
