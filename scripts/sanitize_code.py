import os
import re

def sanitize_and_fix(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the fresh CSS
    responsive_css = """
    /* --- COMPREHENSIVE MOBILE RESPONSIVE FIXES --- */
    @media (max-width: 1200px) {
      .stats-grid, .grid-main, .grid-2, .hero-grid, .module-grid, .grid {
        grid-template-columns: 1fr !important;
        gap: 15px !important;
      }
    }
    @media (max-width: 980px) {
      :root {
        --topbar-height: auto;
        --sidebar-width: 100%;
      }
      .sidebar {
        display: none !important;
        position: fixed;
        inset: 0;
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
        width: 44px; height: 44px;
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
        width: 40px; height: 40px;
        border-radius: 10px;
        border: 1px solid var(--line);
        background: white;
      }
      .school-pill {
        flex: 1; min-width: 0;
        padding: 6px 10px !important;
      }
      .school-pill strong {
        font-size: 12px !important;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      }
      .school-pill span { display: none !important; }
      .control {
        height: 40px !important;
        font-size: 13px !important;
        flex: 1; min-width: 0;
      }
      .search { width: 100% !important; flex: none !important; }
      .icon-btn { width: 40px !important; height: 40px !important; }
      .page-wrap { padding: 15px !important; }
      .page-header { flex-direction: column !important; align-items: stretch !important; }
      .btn-row { flex-direction: column !important; width: 100%; }
      .btn { width: 100%; }
      .d2-header { padding: 15px !important; }
      .d2-header h1 { font-size: 22px !important; }
    }
    @media (min-width: 981px) {
      .mobile-menu-btn, .sidebar-close { display: none !important; }
    }
    """

    # 1. Clean up CSS inside <style>
    style_pattern = r'<style>(.*?)</style>'
    def style_replacer(match):
        style_content = match.group(1)
        # Remove everything from the first mobile comment or media query
        clean_style = re.split(r'/\* Mobile Responsive \*/|/\* --- COMPREHENSIVE|@media \(max-width: 980px\)|@media \(max-width: 1200px\)', style_content)[0]
        # Remove any lingering stray fragments at the end
        clean_style = clean_style.strip()
        # Ensure it doesn't end with a broken brace
        while clean_style.endswith('}'):
            # Check if there's a matching opening brace for the LAST closing brace
            if clean_style.count('{') < clean_style.count('}'):
                clean_style = clean_style.rsplit('}', 1)[0].strip()
            else:
                break
        
        return f'<style>\n    {clean_style}\n\n    {responsive_css}\n  </style>'

    content = re.sub(style_pattern, style_replacer, content, flags=re.DOTALL)

    # 2. Add THE CLEAN JS BLOCK
    toggle_js_clean = """
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

    # Clean up scripts
    script_pattern = r'<script>(.*?)</script>'
    def script_replacer(match):
        script_content = match.group(1)
        # Remove old toggle logic
        clean_script = re.split(r'// Mobile Navigation Toggle', script_content)[0]
        clean_script = clean_script.strip()
        
        # Look for lucide call
        if 'lucide.createIcons();' in script_content:
             # Put it after our clean logic
             return f'<script>\n    {clean_script}\n\n    {toggle_js_clean}\n\n    lucide.createIcons();\n  </script>'
        else:
             return f'<script>\n    {clean_script}\n\n    {toggle_js_clean}\n  </script>'

    # If lucide is external, we might not have a script tag yet
    if '<script>' not in content:
        content = content.replace('</body>', f'<script>\n    {toggle_js_clean}\n  </script>\n</body>')
    else:
        content = re.sub(script_pattern, script_replacer, content, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# Run for all HTML files
path = 'c:/Users/USER/OneDrive/Desktop/school-development-portal'
for f in sorted(os.listdir(path)):
    if f.endswith('.html'):
        print(f"Sanitizing {f}")
        sanitize_and_fix(os.path.join(path, f))
