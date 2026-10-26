# Design for the dashboard (colors, fonts and the mountain banner from the Figma design)

# colors
ORANGE = "#E07A3F"
BLUE = "#6FA8C9"

# CSS: fonts, dark sidebar and KPI cards
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600&family=Source+Sans+3:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #13202F; }

/* Sidebar: dark navy */
[data-testid="stSidebar"] { background-color: #0E1A2B; }
[data-testid="stSidebar"] * { color: #E8ECF2; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #FFFFFF; }
[data-testid="stSidebar"] [data-baseweb="select"] > div { background-color: #1C2C42; border-color: #2A3D57; }

/* KPI cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E7EE;
    border-top: 4px solid #E07A3F;
    border-radius: 14px;
    padding: 16px 20px;
}
[data-testid="stMetricValue"] { font-family: 'Fraunces', serif; }
</style>
"""

# Hero banner with mountains (same drawing as in Figma)
HERO = """
<div style="position:relative; height:240px; border-radius:20px; overflow:hidden; margin-bottom:24px;
background:linear-gradient(180deg, #16243B 0%, #3A4E70 55%, #E59A62 100%);">
<svg viewBox="0 0 1060 240" preserveAspectRatio="none" style="position:absolute; bottom:0; left:0; width:100%; height:100%;">
<circle cx="840" cy="135" r="44" fill="#F2B35B" opacity="0.9"/>
<polygon points="0,240 0,160 90,115 170,150 260,85 350,140 430,105 520,160 600,95 700,140 780,75 880,130 960,100 1060,140 1060,240" fill="#5A7194" opacity="0.75"/>
<polygon points="0,240 0,195 120,140 210,180 330,115 420,170 540,125 640,185 760,105 860,175 980,130 1060,165 1060,240" fill="#2E4265"/>
<polygon points="0,240 0,215 180,185 300,205 470,95 560,160 620,140 760,210 900,185 1060,220 1060,240" fill="#13202F"/>
<polygon points="470,95 433,120 448,116 460,125 474,115 488,123 501,120" fill="#F3F5F8"/>
</svg>
<div style="position:absolute; top:30px; left:36px; max-width:420px;">
<p style="color:#F2B35B; font-weight:700; letter-spacing:2px; font-size:12px; margin:0;">HIMALAYAN EXPEDITIONS · 2020–2024</p>
<p style="font-family:Fraunces, serif; color:white; font-size:38px; font-weight:600; margin:6px 0; line-height:1.1;">Plan your climb with data</p>
<p style="color:#D5DEEA; font-size:15px; margin:0;">868 expeditions across the Himalaya. See what makes a climb succeed, then check your own plan.</p>
</div>
</div>
"""

# Logo + title for the top of the sidebar
BRAND = """
<div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
<svg width="48" height="48" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
<rect width="34" height="34" rx="9" fill="#E07A3F"/>
<path d="M5 26 L14 12 L19 19 L22 15 L29 26 Z" fill="#0E1A2B"/>
<path d="M14 12 L11.2 16.4 L13.2 15.4 L14.6 17 L16.2 15.4 Z" fill="#F3F5F8"/>
</svg>
<div>
<p style="font-family:Fraunces, serif; font-size:24px; font-weight:600; color:#FFFFFF; margin:0; line-height:1.1;">Summit Planner</p>
<p style="font-size:13px; color:#A9B6C8; margin:0;">Himalaya · 2020–2024</p>
</div>
</div>
"""