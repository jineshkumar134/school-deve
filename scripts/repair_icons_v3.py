import os
import re

# Mapping based on the label text to HTML Entities (more robust against encoding issues)
label_to_entity = {
    "module completion": "&#128204;", # 📌
    "total goals": "&#127919;", # 🎯
    "high priority": "&#128293;", # 🔥
    "kpis set": "&#128200;", # 📈
    "timeline coverage": "&#128197;", # 📅
    "values added": "&#128161;", # 💡
    "culture themes": "&#127979;", # 🏫
    "revision entries": "&#128338;", # 🕒
    "infrastructure rows": "&#127979;", # 🏫
    "academic offerings": "&#128218;", # 📚
    "campus readiness": "&#9881;", # ⚙️
    "competitors tracked": "&#127970;", # 🏢
    "opportunities / threats": "&#128200;", # 📈
    "market pressure": "&#9889;", # ⚡
    "total actions": "&#128203;", # 📋
    "in progress": "&#9889;", # ⚡
    "completed": "&#9989;", # ✅
    "task coverage": "&#127919;", # 🎯
    "active blocker": "&#128721;", # 🛑
    "saved records": "&#128450;", # 🗂
    "pending modules": "&#8987;", # ⏳
    "completed modules": "&#9989;", # ✅
    "overall completion": "&#128204;", # 📌
    "combined completion": "&#128204;", # 📌
    "leadership roles": "&#128100;", # 👤
    "committees": "&#129513;", # 🧩
    "monitoring logs": "&#128466;", # 🗒
    "school readiness": "&#127979;", # 🏫
    "goals & actions": "&#127919;", # 🎯
}

path = os.getcwd()

# Extended garbled sequences to clean up
garbled_patterns = [
    r'Ã°Å¸â€œâ€¹', r'Ã°Å¸Å½Â¯', r'Ã°Å¸â€ Â¥', r'Ã°Å¸â€œË†', r'Ã°Å¸â€œâ€¦',
    r'Ã°Å¸â€™Â¡', r'Ã°Å¸Â Â«', r'Ã°Å¸â€œâ€™', r'Ã°Å¸â€œËœ', r'Ã¢â„¢â„¢',
    r'Ã°Å¸Â Â¢', r'Ã¢Å¡Â¡', r'Ã°Å¸â€œâ€¹', r'Ã¢Å“â€¦', r'Ã°Å¸â€ºÂ¡',
    r'Ã°Å¸â€â€š', r'Ã¢Å’Â', r'Ã°Å¸â€˜Â¤', r'Ã°Å¸Â§Â©', r'Ã°Å¸â€œâ€ ',
    r'Ã‚Â'
]

def fix_content(content):
    # Fix icons using labels
    pattern = r'(<div class="stat-icon[^>]*>)([^<]*)(</div>\s*</div>\s*(<div[^>]*>\s*)?<div class="stat-label">([^<]+)</div>)'
    def replace_icon_label_reversed(match):
        prefix = match.group(1)
        suffix = match.group(3)
        label = match.group(5).lower().strip()
        
        for key, entity in label_to_entity.items():
            if key in label:
                return f"{prefix}{entity}{suffix}"
        return match.group(0)

    # Some files have label first
    pattern2 = r'(<div class="stat-label">([^<]+)</div>\s*<div class="stat-icon[^>]*>)([^<]*)(</div>)'
    def replace_icon_normal(match):
        prefix = match.group(1)
        label = match.group(2).lower().strip()
        suffix = match.group(4)
        
        for key, entity in label_to_entity.items():
            if key in label:
                return f"{prefix}{entity}{suffix}"
        return match.group(0)

    new_content = re.sub(pattern, replace_icon_label_reversed, content, flags=re.IGNORECASE | re.DOTALL)
    new_content = re.sub(pattern2, replace_icon_normal, new_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Generic cleanup for any remaining garbled strings
    for p in garbled_patterns:
        new_content = re.sub(p, "", new_content)

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
        print(f"Repaired [Entities] in: {filename}")

print("Entity-based repair complete.")
