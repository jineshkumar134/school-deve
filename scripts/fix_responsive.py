import os
import re

def fix_responsive(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Optimized Mobile Styles
    responsive_css = """
    /* --- COMPREHENSIVE MOBILE RESPONSIVE FIXES --- */
    @media (max-width: 980px) {
      :root {
        --topbar-height: auto;
        --sidebar-width: 100%;
      }

      .sidebar {
        display: none !important;
        position: fixed;
        top: 0;
        left: 0;
        width: 100% !important;
        height: 100vh;
        z-index: 2000;
        background: var(--panel) !important;
        padding: 80px 20px 20px !important;
        overflow-y: auto;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        transform: translateX(-20px);
      }

      .sidebar.active {
        display: block !important;
        opacity: 1;
        visibility: visible;
        transform: translateX(0);
      }

      .sidebar-close {
        display: flex !important;
        position: absolute;
        top: 15px;
        right: 15px;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        border: 1px solid var(--line);
        background: var(--panel-2);
        align-items: center;
        justify-content: center;
        z-index: 2001;
      }

      .topbar {
        height: auto !important;
        padding: 12px 15px !important;
        position: sticky;
        top: 0;
      }

      .topbar-inner {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
      }

      .top-left, .top-right {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        width: 100% !important;
      }

      .mobile-menu-btn {
        display: flex !important;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        border: 1px solid var(--line);
        background: white;
      }

      .school-pill {
        flex: 1;
        min-width: 0;
        padding: 6px 10px !important;
      }

      .school-pill strong {
        font-size: 12px !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .school-pill span { display: none !important; }

      .control {
        height: 40px !important;
        font-size: 13px !important;
        flex: 1;
        min-width: 0;
      }

      .search {
        width: 100% !important;
        flex: none !important;
      }

      .icon-btn {
        width: 40px !important;
        height: 40px !important;
      }

      .page-wrap { padding: 15px !important; }
      .page-header { flex-direction: column !important; align-items: stretch !important; }
      .btn-row { flex-direction: column !important; width: 100%; }
      .btn { width: 100%; }

      .stats-grid, .grid-main, .grid-2, .hero-grid, .module-grid {
        grid-template-columns: 1fr !important;
        gap: 15px !important;
      }
    }
    @media (min-width: 981px) {
      .mobile-menu-btn, .sidebar-close { display: none !important; }
    }
    """

    # Clean up double blocks or old blocks
    content = re.sub(r'/\* --- COMPREHENSIVE MOBILE RESPONSIVE FIXES --- \*/.*?@media \(min-width: 981px\) \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Mobile Responsive Fixes \*/.*?@media \(min-width: 981px\) \{.*?\}', '', content, flags=re.DOTALL)
    
    # Inject one clean block
    content = content.replace('</style>', responsive_css + '\n    </style>')

    # Ensure JS logic is clean
    toggle_js = """
    // Mobile Navigation Toggle
    (function() {
      const mobileMenuBtn = document.getElementById('mobileMenuBtn');
      const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
      const sidebar = document.querySelector('.sidebar');

      if(mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          sidebar.classList.add('active');
          document.body.style.overflow = 'hidden';
        });
      }

      if(sidebarCloseBtn && sidebar) {
        sidebarCloseBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          sidebar.classList.remove('active');
          document.body.style.overflow = '';
        });
      }

      document.addEventListener('click', (e) => {
        if (sidebar && sidebar.classList.contains('active') && !sidebar.contains(e.target) && e.target !== mobileMenuBtn) {
          sidebar.classList.remove('active');
          document.body.style.overflow = '';
        }
      });
    })();
    """
    
    # Remove old JS toggles to avoid dupes
    content = re.sub(r'// Mobile Navigation Toggle.*?\}\)\(\)\;|\/\/ Mobile Navigation Toggle.*?\n\s*\}\s*\}', '', content, flags=re.DOTALL)
    
    # Inject new JS
    if 'lucide.createIcons();' in content:
        content = content.replace('lucide.createIcons();', toggle_js + '\n    lucide.createIcons();')
    else:
        content = content.replace('</body>', f'<script>{toggle_js}</script>\n</body>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# Run for all HTML files
path = 'c:/Users/USER/OneDrive/Desktop/school-development-portal'
for f in os.listdir(path):
    if f.endswith('.html'):
        fix_responsive(os.path.join(path, f))
