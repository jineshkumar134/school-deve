import os
import re

def fix_responsive(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Mobile Responsive Styles
    responsive_css = """
    /* Mobile Responsive Fixes */
    @media (max-width: 980px) {
      .sidebar {
        display: none !important;
        position: fixed;
        top: 0;
        left: 0;
        width: 100% !important;
        height: 100vh;
        z-index: 1000;
        background: var(--panel) !important;
        padding-top: 80px !important;
        overflow-y: auto;
      }
      .sidebar.active {
        display: block !important;
      }
      .mobile-menu-btn {
        display: flex !important;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        border: 1px solid var(--line);
        background: white;
        cursor: pointer;
        order: -1; /* Place at the start */
      }
      .sidebar-close {
        display: block !important;
        position: absolute;
        top: 20px;
        right: 20px;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        border: 1px solid var(--line);
        background: var(--panel-2);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      }
    }
    @media (min-width: 981px) {
      .mobile-menu-btn, .sidebar-close { display: none !important; }
    }
    """
    
    if '/* Mobile Responsive Fixes */' not in content:
        content = content.replace('</style>', responsive_css + '\n    </style>')

    # 2. Inject Mobile Menu Button into Topbar
    # Look for <div class="topbar-inner">
    if 'id="mobileMenuBtn"' not in content:
        menu_btn = '<button id="mobileMenuBtn" class="mobile-menu-btn"><i data-lucide="menu"></i></button>'
        content = content.replace('<div class="topbar-inner">', f'<div class="topbar-inner">\n          {menu_btn}')

    # 3. Inject Close Button into Sidebar
    # Look for <aside class="sidebar">
    if 'id="sidebarCloseBtn"' not in content:
        close_btn = '<button id="sidebarCloseBtn" class="sidebar-close"><i data-lucide="x"></i></button>'
        content = content.replace('<aside class="sidebar">', f'<aside class="sidebar">\n      {close_btn}')

    # 4. Inject JS Logic for Toggling
    toggle_js = """
    // Mobile Navigation Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
    const sidebar = document.querySelector('.sidebar');

    if(mobileMenuBtn && sidebar) {
      mobileMenuBtn.addEventListener('click', () => {
        sidebar.classList.add('active');
      });
    }

    if(sidebarCloseBtn && sidebar) {
      sidebarCloseBtn.addEventListener('click', () => {
        sidebar.classList.remove('active');
      });
    }
    """
    
    if '// Mobile Navigation Toggle' not in content:
        if 'lucide.createIcons();' in content:
            content = content.replace('lucide.createIcons();', toggle_js + '\n    lucide.createIcons();')
        else:
            content = content.replace('</body>', f'<script>{toggle_js}</script>\n</body>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# Run for all HTML files
for f in os.listdir('.'):
    if f.endswith('.html'):
        print(f"Fixing responsive for {f}")
        fix_responsive(f)
