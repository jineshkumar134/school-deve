import re

# Read clean styles from dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    dashboard_html = f.read()

# Extract from <style> to </style> from dashboard (first one)
style_match = re.search(r'<style>.*?</style>', dashboard_html, re.DOTALL)
if style_match:
    base_styles = style_match.group(0)
else:
    print("Could not find style in dashboard")
    exit(1)

with open('global-preview.html', 'r', encoding='utf-8') as f:
    preview_html = f.read()

# Fix the truncated JS in global-preview.html
# The broken JS section is around 'container.innerHTML = foundAny ? reportHTML : `'
# followed by '    // Mobile Navigation Toggle'

fixed_js = """
       container.innerHTML = foundAny ? reportHTML : `
          <div class="window" style="text-align:center; padding:40px; color:var(--danger);">
             Please select at least one section to generate report.
          </div>
       `;
    }

    function renderSection(id, label, data){
      let body = "";
      if(!data) {
        body = `<div style="padding:20px; text-align:center; background:#fcfdfe; border-radius:12px; border:1px dashed var(--line); color:var(--muted); font-style:italic;">No data recorded for ${label}.</div>`;
      } else {
        if(id === 'dashboard2') body = renderDashboard2();
        else if(id === 'identity') body = renderIdentity(data);
        else if(id === 'swot') body = renderSWOT(data);
        else if(id === 'goals') body = renderGoals(data);
        else if(id === 'actions') body = renderActions(data);
        else if(id === 'info') body = renderInfo(data);
        else if(id === 'teams') body = renderTeams(data);
        else if(id === 'market') body = renderMarket(data);
        else if(id === 'diagnosis') body = renderDiagnosis(data);
        else if(id === 'monitoring') body = renderMonitoring(data);
        else body = `<pre style="font-size:11px; color:var(--text-soft); overflow:auto;">${JSON.stringify(data, null, 2)}</pre>`;
      }

      return `
        <div class="report-section window">
           <h3><i data-lucide="${sections.find(s=>s.id===id).icon}" size="18" style="vertical-align:middle; margin-right:8px;"></i> ${label}</h3>
           <div class="report-content">${body}</div>
        </div>
      `;
    }

    function renderTeams(data){
      const leaders = data.leaders || [];
      const committees = data.committees || [];
      return `
        <div style="margin-bottom:20px;">
          <h4 style="font-size:13px; margin-bottom:10px; color:var(--secondary);">School Leadership</h4>
          <table class="report-table">
            <thead><tr><th>Role</th><th>Personnel</th><th>Tenure</th></tr></thead>
            <tbody>
              ${leaders.map(l => `<tr><td>${l.role}</td><td>${l.name}</td><td>${l.tenure}</td></tr>`).join("") || '<tr><td colspan="3">None</td></tr>'}
            </tbody>
          </table>
        </div>
        <div style="margin-top:20px;">
          <h4 style="font-size:13px; margin-bottom:10px; color:var(--success);">Committees & Assemblies</h4>
          ${committees.map(c => `
            <div style="padding:10px; border:1px solid var(--line); border-radius:8px; margin-bottom:10px;">
              <strong>${c.name}</strong> <span style="font-size:11px; color:#999;">(${c.type})</span>
              <p style="font-size:12px; margin-top:4px;">Members: ${c.members}</p>
            </div>
          `).join("") || '<p>None</p>'}
        </div>
      `;
    }

    function renderMarket(data){
      const comps = data.competitors || [];
      const offrs = data.offerings || [];
      return `
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
           <div>
              <h4 style="font-size:12px; margin-bottom:8px;">Competitor Landscape</h4>
              <ul style="padding-left:18px; font-size:13px;">
                ${comps.map(c => `<li>${c.name} - ${c.strength}</li>`).join("") || '<li>No competitors tracked.</li>'}
              </ul>
           </div>
           <div>
              <h4 style="font-size:12px; margin-bottom:8px;">Flagship Offerings</h4>
              <ul style="padding-left:18px; font-size:13px;">
                ${offrs.map(o => `<li>${o.name} (${o.focus})</li>`).join("") || '<li>No offerings listed.</li>'}
              </ul>
           </div>
        </div>
      `;
    }

    function renderDiagnosis(data){
      const infra = data.infrastructure || [];
      const acad = data.academic || [];
      return `
        <div style="margin-bottom:15px; padding:10px; background:var(--primary-soft); border-radius:8px; border:1px solid var(--primary-border);">
           <strong>Composite Readiness Score:</strong> <span style="font-size:18px; color:var(--primary);">${data.readiness || '0'} / 100</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
          <div>
            <h4 style="font-size:12px; margin-bottom:8px;">Infrastructure Status</h4>
            <div style="font-size:12px;">${infra.map(i => `<div>• ${i.area}: ${i.status}</div>`).join("") || 'No data'}</div>
          </div>
          <div>
            <h4 style="font-size:12px; margin-bottom:8px;">Academic Maturity</h4>
            <div style="font-size:12px;">${acad.map(a => `<div>• ${a.segment}: ${a.maturity}</div>`).join("") || 'No data'}</div>
          </div>
        </div>
      `;
    }

    function renderMonitoring(data){
      const items = data.reviews || [];
      return `
         <table class="report-table">
            <thead>
               <tr><th>Date</th><th>Action Item</th><th>Review Status</th><th>Findings</th></tr>
            </thead>
            <tbody>
               ${items.map(i => `
                 <tr>
                    <td style="white-space:nowrap;">${i.date}</td>
                    <td><div style="font-size:11px; color:#666;">${i.goal}</div><strong>${i.action}</strong></td>
                    <td><span style="display:inline-block; padding:2px 8px; border-radius:4px; background:#f0f0f0; font-size:11px; font-weight:600;">${i.status}</span></td>
                    <td style="font-size:12px;">${i.findings}</td>
                 </tr>
               `).join("") || '<tr><td colspan="4">No reviews recorded yet.</td></tr>'}
            </tbody>
         </table>
      `;
    }

    function renderIdentity(data){
       return `
         <div style="margin-bottom:20px;">
           <strong style="display:block; font-size:11px; color:var(--primary); text-transform:uppercase; margin-bottom:4px;">Vision</strong>
           <div style="font-size:16px; font-weight:500; line-height:1.6;">${data.vision || 'Not specified'}</div>
         </div>
         <div style="margin-bottom:20px;">
           <strong style="display:block; font-size:11px; color:var(--secondary); text-transform:uppercase; margin-bottom:4px;">Mission</strong>
           <div style="font-size:14px; line-height:1.6;">${data.mission || 'Not specified'}</div>
         </div>
         <div style="margin-bottom:20px;">
           <strong style="display:block; font-size:11px; color:var(--success); text-transform:uppercase; margin-bottom:4px;">Core Values</strong>
           <div style="font-size:14px;">${data.values || 'Not specified'}</div>
         </div>
       `;
    }

    function renderSWOT(data){
      const pts = data.points || [];
      const types = ['Strength', 'Weakness', 'Opportunity', 'Threat'];
      const colors = { Strength: '#2d9b68', Weakness: '#d95353', Opportunity: '#2d81c1', Threat: '#d58d1f' };
      
      return `<div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
        ${types.map(t => `
          <div style="padding:15px; border:1px solid var(--line); border-radius:12px; background:var(--panel-2);">
            <div style="font-weight:700; color:${colors[t]}; font-size:14px; margin-bottom:10px; border-bottom:1px solid var(--line); padding-bottom:5px;">${t}s</div>
            <ul style="padding-left:18px; font-size:13px; color:var(--text);">
              ${pts.filter(p => p.type === t).map(p => `<li style="margin-bottom:6px;">${p.text}</li>`).join("") || '<li>No items</li>'}
            </ul>
          </div>
        `).join("")}
      </div>`;
    }

    function renderGoals(data){
       const items = data.goals || [];
       return `
         <table class="report-table">
            <thead>
               <tr><th>Category</th><th>Strategic Goal</th><th>Timeline</th><th>Status</th></tr>
            </thead>
            <tbody>
               ${items.map(i => `
                 <tr>
                    <td style="font-weight:600;">${i.category}</td>
                    <td>${i.title}</td>
                    <td>${i.timeline}</td>
                    <td><span style="color:var(--secondary); font-weight:600;">Active</span></td>
                 </tr>
               `).join("") || '<tr><td colspan="4">No goals recorded.</td></tr>'}
            </tbody>
         </table>
       `;
    }

    function renderActions(data){
       const items = data.actions || [];
       return `
         <table class="report-table">
            <thead>
               <tr><th>Goal Ref</th><th>Action Item</th><th>Owner</th><th>Due Date</th></tr>
            </thead>
            <tbody>
               ${items.map(i => `
                 <tr>
                    <td style="font-size:11px; color:#666;">${i.goal}</td>
                    <td>${i.title}</td>
                    <td>${i.owner}</td>
                    <td>${i.due}</td>
                 </tr>
               `).join("") || '<tr><td colspan="4">No actions recorded.</td></tr>'}
            </tbody>
         </table>
       `;
    }

    function renderInfo(data){
      return `
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
           <div>
              <strong style="font-size:11px; color:var(--muted);">Total Students</strong>
              <div style="font-size:18px; font-weight:600;">${data.students || '0'}</div>
           </div>
           <div>
              <strong style="font-size:11px; color:var(--muted);">Total Teachers</strong>
              <div style="font-size:18px; font-weight:600;">${data.teachers || '0'}</div>
           </div>
        </div>
        <div style="margin-top:20px; border-top:1px solid var(--line); padding-top:15px;">
           <strong style="font-size:11px; color:var(--muted);">Address / Location</strong>
           <p style="margin-top:5px;">${data.address || 'Not specified'}</p>
        </div>
      `;
    }

    function renderDashboard2(){
      return `
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:20px;">
          <div style="padding:15px; border:1px solid var(--line); border-radius:12px; background:var(--bg);">
             <div style="font-size:11px; color:var(--secondary); font-weight:700; text-transform:uppercase;">Score</div>
             <div style="font-size:24px; font-weight:700;">72%</div>
          </div>
          <div style="padding:15px; border:1px solid var(--line); border-radius:12px; background:var(--bg);">
             <div style="font-size:11px; color:var(--secondary); font-weight:700; text-transform:uppercase;">Goals</div>
             <div style="font-size:24px; font-weight:700;">8</div>
          </div>
          <div style="padding:15px; border:1px solid var(--line); border-radius:12px; background:var(--bg);">
             <div style="font-size:11px; color:var(--secondary); font-weight:700; text-transform:uppercase;">Actions</div>
             <div style="font-size:24px; font-weight:700;">14</div>
          </div>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
          <div>
            <h4 style="font-size:12px; margin-bottom:10px;">School Health Indices</h4>
            <div style="margin-bottom:8px;">
              <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;"><span>Academic Readiness</span><span>81%</span></div>
              <div style="height:5px; background:var(--line); border-radius:5px; overflow:hidden;"><div style="height:100%; background:var(--secondary); width:81%;"></div></div>
            </div>
            <div style="margin-bottom:8px;">
              <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;"><span>Teacher Capability</span><span>72%</span></div>
              <div style="height:5px; background:var(--line); border-radius:5px; overflow:hidden;"><div style="height:100%; background:var(--primary); width:72%;"></div></div>
            </div>
          </div>
          <div>
            <h4 style="font-size:12px; margin-bottom:10px;">SWOT Overview</h4>
            <div style="display:grid; grid-template-columns: 1fr; gap:5px; font-size:11px;">
               <div style="padding:4px 8px; background:var(--success-soft); border-radius:4px;"><b>S:</b> Strong board results</div>
               <div style="padding:4px 8px; background:var(--danger-soft); border-radius:4px;"><b>W:</b> Low tech adoption</div>
            </div>
          </div>
        </div>
      `;
    }

    init();
"""

# The bad part in preview starts around '    );'
# Wait we can just find '    const settings = JSON.parse(localStorage.getItem(STORAGE_KEYS.settings) || "{}");\n      if(settings.schoolName) document.getElementById("schoolNameTop").textContent = settings.schoolName;'
# and replace everything after it.
inject_point = 'if(settings.schoolName) document.getElementById("schoolNameTop").textContent = settings.schoolName;'

pre_js_match = preview_html.find(inject_point)
if pre_js_match == -1:
    print("Could not find js inject match")
    exit(1)

# we want to close init()
pre_js = preview_html[:pre_js_match + len(inject_point)]

# then add '    }\n\n    function toggleCard...'
rest_of_js = fixed_js

new_html_js_fixed = pre_js + '\n    }\n' + """
    function toggleCard(el, id){
       const chk = document.getElementById(`chk_${id}`);
       chk.checked = !chk.checked;
       el.classList.toggle('active', chk.checked);
    }

    function setAll(val){
      sections.forEach(s => {
        const chk = document.getElementById(`chk_${s.id}`);
        chk.checked = val;
        const card = chk.parentElement;
        card.classList.toggle('active', val);
      });
    }

    function generateReport(){
       const container = document.getElementById("reportPreview");
       const settings = JSON.parse(localStorage.getItem(STORAGE_KEYS.settings) || "{}");
       const customTitle = document.getElementById("customReportTitle").value || `${settings.schoolName || 'Internal'} Development Report`;
       
       let reportHTML = `
         <div class="report-header window" style="padding:40px; text-align:center; background:linear-gradient(rgba(244,124,32,0.05), #fff);">
            <h1 style="font-size:32px; margin-bottom:10px; color:var(--primary);">${customTitle}</h1>
            <p style="color:var(--text-soft);">Academic Year ${settings.academicYear || '2026-27'}</p>
            <div style="margin-top:20px; font-size:12px; color:var(--muted);">Generated via School Development Portal • ${new Date().toLocaleDateString()}</div>
         </div>
       `;
       
       let foundAny = false;
       sections.forEach(s => {
         if(document.getElementById(`chk_${s.id}`).checked){
           const data = JSON.parse(localStorage.getItem(STORAGE_KEYS[s.key]) || "null");
           reportHTML += renderSection(s.id, s.label, data);
           foundAny = true;
         }
       });
""" + rest_of_js + """
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

    lucide.createIcons();
  </script>
</body>
</html>
"""

# Now we need to fix the <style> tags.
# Replace all multiple <style> tags and their contents with base_styles from dashboard.html + print media

print_media = """
    /* Report Preview Content */
    .report-section{ margin-bottom:40px; border:1px solid var(--line); border-radius:20px; overflow:hidden; }
    .report-section h3{ background:var(--panel-2); padding:16px 24px; font-size:18px; border-bottom:1px solid var(--line); }
    .report-content{ padding:24px; }
    
    .report-table{ width:100%; border-collapse:collapse; margin-top:10px; }
    .report-table th, .report-table td{ padding:12px; border:1px solid var(--line); text-align:left; font-size:13px; }
    .report-table th{ background:var(--panel-2); font-weight:600; }

    /* Selection Grid Styles */
    .selection-grid{ display:grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap:16px; margin-bottom:30px; }
    .selection-card{ background:#fff; border:1.5px solid var(--line); border-radius:16px; padding:16px; display:flex; align-items:center; gap:14px; cursor:pointer; transition:.2s; position:relative; }
    .selection-card:hover{ border-color:var(--secondary-border); background:var(--secondary-soft); }
    .selection-card.active{ border-color:var(--primary); background:var(--primary-soft); }
    .selection-card input{ position:absolute; opacity:0; }
    
    .card-icon{ width:42px; height:42px; border-radius:12px; background:var(--panel-2); border:1px solid var(--line); display:flex; align-items:center; justify-content:center; color:var(--text-soft); }
    .selection-card.active .card-icon{ background:#fff; border-color:var(--primary-border); color:var(--primary); }
    .card-label{ font-size:13px; font-weight:600; flex:1; }
    .card-check{ width:18px; height:18px; border-radius:50%; border:2px solid var(--line); }
    .selection-card.active .card-check{ background:var(--primary); border-color:var(--primary); display:flex; align-items:center; justify-content:center; }
    .selection-card.active .card-check::after{ content:'\u2713'; color:#fff; font-size:10px; font-weight:bold; }


    @media print{
       .sidebar, .topbar, .no-print, .selection-grid { display:none !important; }
       .main{ width:100% !important; border:none !important; padding:0 !important; margin:0 !important; background:#fff !important; }
       .page-wrap{ max-width:100% !important; padding:0 !important; }
       .window{ border:none !important; box-shadow:none !important; margin-bottom:30px !important; }
       .report-section{ page-break-before: always; border: 1px solid #ccc !important; }
       .report-section:first-child { page-break-before: auto; }
       .report-table th{ background:#eee !important; color:#000 !important; }
       body{ background:#fff !important; font-size:12pt; }
       .page-title{ margin-top:0 !important; }
    }
  </style>
"""
final_base_styles = base_styles.replace('</style>', print_media)

# Just tear all <style>...</style> from new_html_js_fixed, and prepend ONE <style> blocks
head_content_without_styles = re.sub(r'<style>.*?</style>', '', new_html_js_fixed, flags=re.DOTALL)
# Inject the new style
head_split = head_content_without_styles.split('</head>')
final_html = head_split[0] + final_base_styles + "\n</head>" + head_split[1]

with open('global-preview.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Fixed global-preview.html")
