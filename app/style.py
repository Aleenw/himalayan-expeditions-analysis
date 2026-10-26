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

/* Less empty space at the top of the page */
.block-container, [data-testid="stMainBlockContainer"] { padding-top: 3rem !important; }

/* Sidebar: dark navy */
[data-testid="stSidebar"] { background-color: #0E1A2B; }
[data-testid="stSidebar"] * { color: #E8ECF2; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #FFFFFF; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #1C2C42 !important; border: 1px solid #2A3D57 !important; border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] input { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF; }
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #A9B6C8 !important; }
[data-testid="stSidebar"] label p { font-weight: 600; color: #FFFFFF; font-size: 15px; }

/* Team size slider: white knobs with orange border, hide the small numbers */
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background-color: #FFFFFF !important; border: 3px solid #E07A3F !important;
}
[data-testid="stSidebar"] [data-testid="stSliderThumbValue"],
[data-testid="stSidebar"] [data-testid="stSliderTickBarMin"],
[data-testid="stSidebar"] [data-testid="stSliderTickBarMax"] { display: none !important; }

/* Charts inside white cards */
[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E7EE;
    border-radius: 14px;
    padding: 8px 8px 0 8px;
}

/* Tabs: bigger text (only the tab names, not the question buttons) */
[data-testid="stTabs"] [role="tab"] p { font-size: 18px; }

/* Space between the KPI cards and the tabs */
[data-testid="stTabs"] { margin-top: 32px; }

/* Check my plan: the form is a white card */
[data-testid="stForm"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E7EE !important;
    border-radius: 16px;
    padding: 24px;
}

/* Hide the small link icon next to the titles */
[data-testid="stHeaderActionElements"], .stHeadingContainer a, h1 a, h2 a, h3 a { display: none !important; }

/* KPI cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E7EE;
    border-top: 4px solid #E07A3F;
    border-radius: 14px;
    padding: 16px 20px;
}
[data-testid="stMetricValue"] { font-family: 'Fraunces', serif; }

/* Custom KPI cards (same size, like the Figma design) */
.kpi {
    background-color: #FFFFFF;
    border: 1px solid #E2E7EE;
    border-radius: 14px;
    padding: 18px 20px;
    height: 165px;
    overflow: hidden;
    margin-bottom: 8px;
}
.kpi-bar { width: 28px; height: 4px; border-radius: 2px; margin-bottom: 14px; }
.kpi p { margin: 0 !important; padding: 0 !important; }
.kpi .kpi-label { font-size: 12px !important; font-weight: 600; letter-spacing: 1.5px; color: #607086; line-height: 1.3 !important; white-space: nowrap; }
.kpi .kpi-value { font-family: 'Fraunces', serif; font-size: 42px !important; font-weight: 600; color: #13202F; line-height: 1.2 !important; margin: 4px 0 6px 0 !important; }
.kpi .kpi-sub { font-size: 13px !important; color: #607086; line-height: 1.35 !important; }
</style>
"""

# Logo + title for the top of the sidebar
BRAND = """
<div style="display:flex; align-items:center; gap:12px; margin-top:-40px; margin-bottom:8px;">
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

# Short description under the logo
ABOUT = """
<p style="font-size:14px; color:#A9B6C8; line-height:1.5; margin-top:4px;">
A data dashboard for climbers planning a Himalayan expedition. Explore which mountain,
season, company and gear give you the best chance to reach the summit safely.
</p>
<p style="font-size:12px; color:#7F8EA3;">
Data: The Himalayan Database via TidyTuesday (2025-01-21) · 868 expeditions, 2020–2024.
</p>
"""

# "FILTERS" title in orange
FILTERS_TITLE = """
<p style="color:#F2B35B; font-weight:700; letter-spacing:3px; font-size:13px; margin:0 0 4px 0;">FILTERS</p>
"""


# Team size title: name on the left, chosen range on the right
def team_title(low, high):
    return f"""
<div style="display:flex; justify-content:space-between; margin-bottom:-12px;">
<span style="font-weight:600; color:#FFFFFF; font-size:15px;">Team size (climbers)</span>
<span style="font-weight:600; color:#F2B35B; font-size:15px;">{low} – {high}</span>
</div>
"""


# KPI card: colored bar, label, big number and a small explanation
def kpi_card(label, value, sub, color):
    return f"""
<div class="kpi">
<div class="kpi-bar" style="background-color:{color};"></div>
<p class="kpi-label">{label}</p>
<p class="kpi-value">{value}</p>
<p class="kpi-sub">{sub}</p>
</div>
"""


# Insight on top of a chart: big colored number + one sentence
def insight(number, text, color):
    return f"""
<div style="border-left:4px solid {color}; background-color:#FFFFFF; border-radius:10px;
padding:10px 16px; margin:4px 0 8px 0; display:flex; align-items:center; gap:14px;">
<span style="font-family:Fraunces, serif; font-size:28px; font-weight:600; color:{color}; white-space:nowrap;">{number}</span>
<span style="font-size:14px; color:#13202F; line-height:1.4;">{text}</span>
</div>
"""


# Observation from the notebook, shown under a chart
def note(text):
    return f"""
<div style="background-color:#EEF1F5; border-radius:10px; padding:12px 16px; margin:0 0 16px 0;">
<p style="font-size:11px; font-weight:700; letter-spacing:1.5px; color:#607086; margin:0 0 4px 0;">FROM MY ANALYSIS (ALL 868 EXPEDITIONS)</p>
<p style="font-size:14px; color:#13202F; line-height:1.5; margin:0;">{text}</p>
</div>
"""


# "YOUR PLAN" title inside the form
PLAN_TITLE = """
<p style="color:#E07A3F; font-weight:700; letter-spacing:3px; font-size:13px; margin:0 0 4px 0;">YOUR PLAN</p>
"""


# Dark result card before the climber presses the button
def result_card_empty():
    return """
<div style="background-color:#0E1A2B; border-radius:16px; padding:28px; min-height:420px;">
<p style="color:#F2B35B; font-weight:700; letter-spacing:3px; font-size:13px; margin:0;">ESTIMATED CHANCE OF SUCCESS</p>
<p style="font-family:Fraunces, serif; font-size:24px; color:#FFFFFF; margin:60px 0 8px 0;">Your result will appear here</p>
<p style="color:#A9B6C8; font-size:15px; margin:0;">Fill in your plan and press <b>Check my plan</b>.</p>
</div>
"""


# Dark result card: ring with the chance, a short text and the tips
def result_card(chance, description, tips):
    length = 364 * chance / 100          # 364 = length of the full circle
    if chance >= 70:
        label = "High chance"
        meaning = "usually reach the summit."
    elif chance >= 45:
        label = "Medium chance"
        meaning = "succeed about half of the time."
    else:
        label = "Low chance"
        meaning = "often do not reach the summit."

    # one row for each tip, with a colored circle
    colors = {"good": "#2E8B6A", "warn": "#F2B35B", "bad": "#C2483A"}
    signs = {"good": "✓", "warn": "!", "bad": "!"}
    rows = ""
    for kind, text in tips:
        rows += f"""<div style="display:flex; align-items:center; gap:12px; margin:10px 0;">
<span style="background-color:{colors[kind]}; color:#FFFFFF; border-radius:50%; width:24px; height:24px; min-width:24px;
display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px;">{signs[kind]}</span>
<span style="color:#E8ECF2; font-size:15px;">{text}</span></div>"""

    return f"""
<div style="background-color:#0E1A2B; border-radius:16px; padding:28px;">
<p style="color:#F2B35B; font-weight:700; letter-spacing:3px; font-size:13px; margin:0 0 16px 0;">ESTIMATED CHANCE OF SUCCESS</p>
<div style="display:flex; align-items:center; gap:28px;">
<div style="position:relative; width:150px; height:150px; min-width:150px;">
<svg width="150" height="150" viewBox="0 0 140 140">
<circle cx="70" cy="70" r="58" fill="none" stroke="#2A3D57" stroke-width="12"/>
<circle cx="70" cy="70" r="58" fill="none" stroke="#E07A3F" stroke-width="12" stroke-linecap="round"
stroke-dasharray="{length:.0f} 364" transform="rotate(-90 70 70)"/>
</svg>
<p style="position:absolute; top:50%; left:0; right:0; transform:translateY(-50%); margin:0; text-align:center;
font-family:Fraunces, serif; font-size:38px; font-weight:600; color:#FFFFFF;">{chance:.0f}%</p>
</div>
<div>
<p style="font-family:Fraunces, serif; font-size:28px; font-weight:600; color:#FFFFFF; margin:0 0 6px 0;">{label}</p>
<p style="color:#A9B6C8; font-size:15px; line-height:1.5; margin:0;">Plans like yours ({description}) {meaning}</p>
</div>
</div>
<div style="height:1px; background-color:#2A3D57; margin:22px 0 10px 0;"></div>
{rows}
<p style="color:#7F8EA3; font-size:12px; margin:16px 0 0 0;">Estimate from a logistic regression model (accuracy about 76%). Not a guarantee.</p>
</div>
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
