import os
import re

def fix_responsive(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ensure Mobile Preview Button is in the Topbar Main Row
    if 'class="mobile-preview-btn"' not in content:
        preview_btn = '<a href="global-preview.html" class="mobile-preview-btn" title="Global Preview"><i data-lucide="eye"></i></a>'
        
        # We want to place it next to the menu button on mobile
        if '<button id="mobileMenuBtn"' in content:
             # Find the mobile menu button and add the preview button after it
             content = re.sub(r'(<button id="mobileMenuBtn".*?</button>)', r'\1\n          ' + preview_btn, content, flags=re.DOTALL)
        elif '<div class="topbar-inner">' in content:
             # Fallback
             content = content.replace('<div class="topbar-inner">', f'<div class="topbar-inner">\n          <button id="mobileMenuBtn" class="mobile-menu-btn"><i data-lucide="menu"></i></button>\n          {preview_btn}')

    # 2. Cleanup: If it was accidentally injected into btn-row or elsewhere
    # Look for mobile-preview-btn NOT near mobileMenuBtn and remove it
    # Actually, easier to just remove all and re-inject correctly
    content = re.sub(r'<a href="global-preview.html" class="mobile-preview-btn".*?</a>', '', content, flags=re.DOTALL)
    
    # Re-inject correctly
    preview_btn = '<a href="global-preview.html" class="mobile-preview-btn" title="Global Preview"><i data-lucide="eye"></i></a>'
    if '<button id="mobileMenuBtn"' in content:
         content = re.sub(r'(<button id="mobileMenuBtn".*?</button>)', r'\1\n          ' + preview_btn, content, flags=re.DOTALL)
    elif '<div class="topbar-inner">' in content:
         content = content.replace('<div class="topbar-inner">', f'<div class="topbar-inner">\n          <button id="mobileMenuBtn" class="mobile-menu-btn"><i data-lucide="menu"></i></button>\n          {preview_btn}')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# Run for all HTML files
path = 'c:/Users/USER/OneDrive/Desktop/school-development-portal'
for f in os.listdir(path):
    if f.endswith('.html'):
        fix_responsive(os.path.join(path, f))
