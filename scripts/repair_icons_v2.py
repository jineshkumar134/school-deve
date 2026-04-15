import os
import re

# Mapping based on the label text
label_to_emoji = {
    "module completion": "📌",
    "total goals": "🎯",
    "high priority": "🔥",
    "kpis set": "📈",
    "timeline coverage": "📅",
    "values added": "💡",
    "culture themes": "🏫",
    "revision entries": "🕒",
    "infrastructure rows": "🏫",
    "academic offerings": "📚",
    "campus readiness": "⚙️",
    "competitors tracked": "🏢",
    "opportunities / threats": "📈",
    "market pressure": "⚡",
    "total actions": "📋",
    "in progress": "⚡",
    "completed": "✅",
    "task coverage": "🎯",
    "active blocker": "🛑",
    "saved records": "🗂",
    "pending modules": "⏳",
    "completed modules": "✅",
    "overall completion": "📌",
    "combined completion": "📌",
    "leadership roles": "👤",
    "committees": "🧩",
    "monitoring logs": "🗒",
    "school readiness": "🏫",
    "goals & actions": "🎯",
}

path = os.getcwd()

def fix_content(content):
    # Regex to find stat-cards and their components
    # <div class="stat-label">Total Goals</div>\s*<div class="stat-icon[^>]*>.*?</div>
    pattern = r'(<div class="stat-label">([^<]+)</div>\s*<div class="stat-icon[^>]*>)([^<]+)(</div>)'
    
    def replace_icon(match):
        prefix = match.group(1)
        label = match.group(2).lower().strip()
        suffix = match.group(4)
        
        for key, emoji in label_to_emoji.items():
            if key in label:
                return f"{prefix}{emoji}{suffix}"
        return match.group(0) # No change if not found

    new_content = re.sub(pattern, replace_icon, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Also fix some standalone icons in headers or other places
    # Module 1: Institutional Identity
    new_content = new_content.replace('Ã¢â‚¬â€œ', '–').replace('Ã¢â‚¬â„¢', "'").replace('Ã¢Å“Â¨', '✨').replace('Ã¢Å’Â«', '⌫')
    new_content = new_content.replace('Ã¢â‚¬Â¢', '•').replace('Ã¢â‚¬â€', '—')
    
    return new_content

for filename in os.listdir(path):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(path, filename)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    new_content = fix_content(content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Repaired icons in: {filename}")

print("Intelligent repair complete.")
