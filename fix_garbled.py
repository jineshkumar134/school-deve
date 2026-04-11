import os

# Mapping of garbled strings to actual emojis
mapping = {
    'Ã°Å¸â€œâ€¹': '📋',
    'Ã¢Å¡Â¡': '⚡',
    'Ã¢Å“â€¦': '✅',
    'Ã°Å¸Å½Â¯': '🎯',
    'Ã¢Å“â€¢': '✖',
    'Ã¢â€ Â»': '↻',
    'Ã¢â‚¬Â¢': '•',
    'Ã°Å¸â€œÅ’': '📌',
    'Ã¢Å“â€': '✓', # Sometimes checking if this is correct
    'Ã¢Â Â³': '⏳',
    'Ã°Å¸â€”â€š': '🗂',
    'Ã°Å¸â€œÂ ': '🗒',
    'Ã°Å¸Â Â«': '🏫',
    'Ã¢â‚¬â€': '—',
    'Ã°Å¸â€ Â¥': '🔥',
    'Ã°Å¸â€œË†': '📈',
    'Ã°Å¸â€œâ€¦': '📅',
    'Ã°Å¸â€™Â ': '💡',
    'Ã°Å¸â€¢â€™': '🕒',
    'Ã°Å¸Â Â¢': '🏢',
    'Ã°Å¸â€ºâ€˜': '🛑',
    'Ã¢â€ Â ': '←',
    'Ã°Å¸â€œÅ': '📚',
    'Ã¢Å¡â„¢Ã¯Â¸Â ': '⚙️',
    'Ã°Å¸â€™Âª': '💪',
    'Ã°Å¸â€œâ€': '🔍',
    'Ã°Å¸â€˜Â¾': '👾',
    'Ã°Å¸â€œÂ¢': '📣',
    'Ã¢â‚¬â€œ': '–',
    'Ã¢â‚¬â„¢': "'",
    'Ã¢Å“Â¨': '✨',
    'Ã¢Å’Â«': '⌫',
    'Ã¢Â¡ÂÂi': '⚡', # Looking at action-plans.html line 665 it was lightning
    'Ã¢Å’â€!': '✅', # Looking at action-plans.html line 673 it was checkmark
    '✓œ': '✅',
    'Ã¢Â Â³': '⏳',
    'Ã¢Å“â€œ': '✅',
}

path = os.getcwd()

for filename in os.listdir(path):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(path, filename)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    changed = False
    for garbled, actual in mapping.items():
        if garbled in content:
            content = content.replace(garbled, actual)
            changed = True
    
    # Also catch some variants
    if 'Ã°Å¸â€œâ€¹' in content: # Duplicate check just in case
         content = content.replace('Ã°Å¸â€œâ€¹', '📋')
         changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filename}")

print("Artifact cleanup complete.")
