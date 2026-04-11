import os
import re

modules = {
    'dashboard.html': '01',
    'institutional-identity.html': '02',
    'school-information.html': '03',
    'teams-committees.html': '04',
    'market-dynamics.html': '05',
    'diagnosis.html': '06',
    'swot.html': '07',
    'goals.html': '08',
    'action-plans.html': '09',
    'monitoring.html': '10',
    'reports-summary.html': '11',
    'complete-school-view.html': '12',
    'global-preview.html': '13'
}

labels = {
    'dashboard.html': 'Dashboard',
    'institutional-identity.html': 'Institutional Identity',
    'school-information.html': 'School Information',
    'teams-committees.html': 'Teams & Committees',
    'market-dynamics.html': 'Market Dynamics',
    'diagnosis.html': 'Diagnosis',
    'swot.html': 'SWOT Analysis',
    'goals.html': 'Strategic Goals',
    'action-plans.html': 'Action Plans',
    'monitoring.html': 'Monitoring',
    'reports-summary.html': 'Reports & Summary',
    'complete-school-view.html': 'Complete School View',
    'global-preview.html': 'Global Preview & Print'
}

eye_metadata = {
    'institutional-identity.html': ('1', 'Institutional Identity'),
    'school-information.html': ('2', 'School Information'),
    'teams-committees.html': ('3', 'Teams & Committees'),
    'market-dynamics.html': ('4', 'Market Dynamics'),
    'diagnosis.html': ('5', 'Diagnosis'),
    'swot.html': ('6', 'SWOT Analysis'),
    'goals.html': ('7', 'Strategic Goals'),
    'action-plans.html': ('8', 'Action Plans'),
    'monitoring.html': ('9', 'Monitoring'),
    'reports-summary.html': ('10', 'Reports & Summary'),
    'complete-school-view.html': ('11', 'Complete School View'),
    'global-preview.html': ('12', 'Global Preview & Print')
}

path = os.getcwd()

for filename in os.listdir(path):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(path, filename)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Create the standard navigation HTML
    nav_html = '<div class="nav-list">\n'
    nav_order = [
        'dashboard.html', 'institutional-identity.html', 'school-information.html',
        'teams-committees.html', 'market-dynamics.html', 'diagnosis.html',
        'swot.html', 'goals.html', 'action-plans.html',
        'monitoring.html', 'reports-summary.html', 'complete-school-view.html',
        'global-preview.html'
    ]
    
    for k in nav_order:
        active = 'active' if k == filename else ''
        nav_html += f'          <a href="{k}" class="nav-item {active}">\n'
        nav_html += f'            <div class="nav-no">{modules[k]}</div>\n'
        nav_html += f'            <div class="nav-label">{labels[k]}</div>\n'
        nav_html += '          </a>\n'
    nav_html += '        </div>'

    # Replace the navigation block
    # This regex target the entire nav-group including potentially duplicated nav-lists
    content = re.sub(r'(?s)<div class="nav-group">.*?</div>\s*</div>\s*</aside>', 
                     f'<div class="nav-group">\n        <div class="nav-title">Main Navigation</div>\n        {nav_html}\n      </div>\n    </aside>', 
                     content, count=1)

    # Standardize the eyebrow
    if filename in eye_metadata:
        m_no, m_name = eye_metadata[filename]
        content = re.sub(r'<div class="eyebrow">.*?</div>', 
                         f'<div class="eyebrow">Module {m_no}: {m_name}</div>', 
                         content, count=1)

    # Ensure "Back to Dashboard" button exists for all modules except the dashboard itself
    if filename != 'dashboard.html' and 'Back to Dashboard' not in content:
        content = re.sub(r'<div class="btn-row">', 
                         r'<div class="btn-row"><a href="dashboard.html" class="btn secondary">Back to Dashboard</a>', 
                         content, count=1)

    # Fix common encoding artifacts
    content = content.replace('Ã¢â‚¬â€œ', '–').replace('Ã¢â‚¬â„¢', "'").replace('Ã¢Å“Â¨', '✨').replace('Ã¢Å’Â«', '⌫')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Standardization complete.")
