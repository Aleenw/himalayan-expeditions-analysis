import os
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from scipy.stats import gaussian_kde
from sklearn.linear_model import LogisticRegression

from style import (CSS, HERO, BRAND, ABOUT, FILTERS_TITLE, team_title, kpi_card, insight, note,
                   PLAN_TITLE, result_card, result_card_empty, ORANGE, BLUE)

# ---------- Page settings ----------
st.set_page_config(page_title="Summit Planner", page_icon="🏔️", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)


# ---------- Load data ----------
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "clean_data.csv")
    df = pd.read_csv(path)

    # helper columns (same as in the notebook)
    df["any_death"] = (df["member_deaths"] + df["hired_deaths"]) > 0
    df["height_group"] = pd.cut(df["height_m"], bins=[0, 7000, 8000, 9000],
                                labels=["Under 7,000 m", "7,000-8,000 m", "Over 8,000 m"])
    df["team_size"] = pd.cut(df["members"], bins=[0, 1, 3, 6, 12, 100],
                             labels=["Solo", "2-3", "4-6", "7-12", "13+"])
    return df


df = load_data()


# ---------- Model ----------
@st.cache_resource
def train_model(data):
    X = data[["oxygen_used", "members", "hired_staff", "height_m", "season"]].copy()
    X["height_m"] = X["height_m"] / 1000          # height in km
    X = pd.get_dummies(X, columns=["season"])     # season → columns
    y = data["success"]
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model, X.columns


model, model_columns = train_model(df)


# show a plotly chart with the numbers written straight, outside the bars
# One look for all charts: fonts, light grid, rounded bars, white background
def show_chart(fig):
    if fig.data and fig.data[0].type == "bar":
        fig.update_traces(textangle=0, textposition="outside", cliponaxis=False,
                          textfont=dict(size=13, color="#13202F"))
    fig.update_layout(
        font=dict(family="Source Sans 3, sans-serif", size=13, color="#607086"),
        title=dict(font=dict(family="Fraunces, serif", size=18, color="#13202F"), x=0, xanchor="left"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=20, t=90, b=10),
        barcornerradius=6,
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Source Sans 3, sans-serif"),
        legend=dict(orientation="h", y=1.0, x=0, xanchor="left", yanchor="bottom", title=""),  # under the title
    )
    fig.update_xaxes(showgrid=False, showline=False, zeroline=False)
    fig.update_yaxes(gridcolor="#EEF1F5", showline=False, zeroline=False)
    # hide the toolbar (zoom, camera...) so it does not cover the title
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---------- Sidebar ----------
st.sidebar.markdown(BRAND, unsafe_allow_html=True)
st.sidebar.markdown(ABOUT, unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown(FILTERS_TITLE, unsafe_allow_html=True)

# 1) Mountain
mountains = ["All mountains"] + list(df["peak"].value_counts().index)
mountain = st.sidebar.selectbox("Mountain", mountains)

# 2) Season (chips)
all_seasons = ["Spring", "Autumn", "Winter", "Summer"]
seasons = st.sidebar.pills("Season", all_seasons, selection_mode="multi", default=all_seasons)
if len(seasons) == 0:          # nothing selected = show all seasons
    seasons = all_seasons

# 3) Peak height
height_choice = st.sidebar.selectbox("Peak height", ["All heights", "Under 7,000 m", "7,000-8,000 m", "Over 8,000 m"])

# 4) Oxygen (toggle)
only_oxygen = st.sidebar.toggle("Only expeditions that used oxygen")

# 5) Team size (title on the left, range on the right)
min_team = int(df["members"].min())
max_team = int(df["members"].max())
current = st.session_state.get("team", (min_team, max_team))
st.sidebar.markdown(team_title(current[0], current[1]), unsafe_allow_html=True)
team = st.sidebar.slider("Team size (climbers)", min_team, max_team, (min_team, max_team),
                         key="team", label_visibility="collapsed")

# ---------- Apply filters ----------
filtered = df.copy()

if mountain != "All mountains":
    filtered = filtered[filtered["peak"] == mountain]

filtered = filtered[filtered["season"].isin(seasons)]

if height_choice != "All heights":
    filtered = filtered[filtered["height_group"] == height_choice]

if only_oxygen:
    filtered = filtered[filtered["oxygen_used"] == True]

filtered = filtered[(filtered["members"] >= team[0]) & (filtered["members"] <= team[1])]

# stop if no data
if len(filtered) == 0:
    st.warning("No expeditions match these filters. Try changing them.")
    st.stop()

# ---------- Hero banner ----------
st.markdown(HERO, unsafe_allow_html=True)

# ---------- KPI cards ----------
total = len(df)
n = len(filtered)
all_success = df["success"].mean() * 100
success = filtered["success"].mean() * 100
death = filtered["any_death"].mean() * 100
oxygen_share = filtered["oxygen_used"].mean() * 100

# card 1: number of expeditions
if n == total:
    sub1 = "All expeditions, 2020–2024"
else:
    sub1 = f"{n / total * 100:.0f}% of all {total} trips"

# card 2: success rate (compare with all data when filtered)
if n == total:
    sub2 = f"{filtered['success'].sum()} teams reached the summit"
else:
    # round first, so the difference matches the numbers shown on the card
    diff = round(success) - round(all_success)
    sub2 = f"{diff:+d} pts vs all ({round(all_success)}%)"

# card 3: deaths
death_trips = filtered[filtered["any_death"] == True]
if len(death_trips) > 0:
    above_8000 = (death_trips["height_m"] >= 8000).mean() * 100
    sub3 = f"{len(death_trips)} trips · {above_8000:.0f}% on 8,000 m peaks"
else:
    sub3 = "No deaths in these trips"

# card 4: oxygen use (the most important factor)
with_o2 = filtered[filtered["oxygen_used"] == True]
without_o2 = filtered[filtered["oxygen_used"] == False]
if len(with_o2) > 0 and len(without_o2) > 0:
    sub4 = f"{with_o2['success'].mean() * 100:.0f}% success with O₂, {without_o2['success'].mean() * 100:.0f}% without"
elif len(with_o2) > 0:
    sub4 = "All these trips used oxygen"
else:
    sub4 = "None of these trips used oxygen"

col1, col2, col3, col4 = st.columns(4)
col1.markdown(kpi_card("EXPEDITIONS", n, sub1, ORANGE), unsafe_allow_html=True)
col2.markdown(kpi_card("SUCCESS RATE", f"{success:.0f}%", sub2, "#2E8B6A"), unsafe_allow_html=True)
col3.markdown(kpi_card("DEATH RISK", f"{death:.1f}%", sub3, "#C2483A"), unsafe_allow_html=True)
col4.markdown(kpi_card("OXYGEN USE", f"{oxygen_share:.0f}%", sub4, BLUE), unsafe_allow_html=True)

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["Overview", "Check my plan", "Data"])

# ===== Tab 1: Overview =====
with tab1:
    # The climber picks a question. The answer has 3 parts:
    # 1) insight box (calculated from the filtered data, changes with the filters)
    # 2) the chart(s) from the notebook
    # 3) the observation I wrote in the notebook (about all 868 expeditions)

    questions = ["Which mountain?", "Which season?", "Should I bring oxygen?", "How big a team?",
                 "How many guides?", "How long will it take?", "What could stop me?", "Which company?"]
    question = st.pills("What do you want to know?", questions, selection_mode="single", default=questions[0])
    if question is None:
        question = questions[0]

    st.subheader(question)

    # ---------- Q1: Which mountain? (peak height) ----------
    if question == "Which mountain?":
        height = filtered.groupby("height_group", observed=True).agg(
            success=("success", "mean"), deaths=("any_death", "mean"), trips=("success", "count")).reset_index()
        height["success"] = height["success"] * 100
        height["deaths"] = height["deaths"] * 100

        high = height[height["height_group"] == "Over 8,000 m"]
        low = filtered[filtered["height_m"] < 8000]
        if len(high) > 0 and len(low) > 0:
            st.markdown(insight(f"{high['deaths'].iloc[0]:.1f}%",
                                f"of trips on 8,000 m peaks had a death, compared with "
                                f"{low['any_death'].mean() * 100:.1f}% on lower peaks.", "#C2483A"),
                        unsafe_allow_html=True)
        else:
            st.markdown(insight("—", "Only one height group with these filters, so we can't compare.", "#C2483A"),
                        unsafe_allow_html=True)

        # where do people climb? (height distribution, full width)
        # same histogram as in the notebook (20 bins, black edges, kde line), but interactive
        heights = filtered["height_m"]
        bin_size = (heights.max() - heights.min()) / 20
        if bin_size == 0:               # only one mountain height in the filter
            bin_size = 100

        fig = px.histogram(filtered, x="height_m", title="Height Distribution of the Mountains",
                           color_discrete_sequence=[BLUE])
        fig.update_traces(xbins=dict(start=heights.min(), end=heights.max() + bin_size, size=bin_size),
                          marker_line_color="black", marker_line_width=1, opacity=0.6)

        # kde line (smooth curve), scaled to the number of expeditions
        if heights.nunique() > 1:
            kde = gaussian_kde(heights)
            x_line = np.linspace(heights.min(), heights.max(), 200)
            y_line = kde(x_line) * len(heights) * bin_size
            fig.add_scatter(x=x_line, y=y_line, mode="lines", line=dict(color=BLUE, width=3),
                            name="KDE", hoverinfo="skip")

        fig.update_layout(xaxis_title="Height m", yaxis_title="Number of Expeditions", showlegend=False,
                          bargap=0)
        show_chart(fig)
        st.markdown(note("The distribution shows two groups of mountains: the first is around 6,000–7,500 m and "
                         "the second is above 8,000 m, with almost no expeditions in between. More than half of "
                         "the expeditions (54%) are on mountains above 8,000 m."), unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            fig = px.bar(height, x="height_group", y="success", text_auto=".0f", hover_data=["trips"],
                         title="Success Rate by Peak Height", color_discrete_sequence=[BLUE])
            fig.update_layout(xaxis_title="Peak Height", yaxis_title="Success rate (%)", yaxis_range=[0, 100])
            show_chart(fig)
            st.markdown(note("Peaks over 8,000 m have the highest success rate (75%), and the 7,000–8,000 m "
                             "peaks have the lowest (50%). This does not mean the highest peaks are easier: "
                             "most expeditions on 8,000 m peaks use oxygen."), unsafe_allow_html=True)
        with right:
            fig = px.bar(height, x="height_group", y="deaths", text_auto=".1f", hover_data=["trips"],
                         title="Share of Expeditions With a Death, by Peak Height",
                         color_discrete_sequence=["#C2483A"])
            fig.update_layout(xaxis_title="Peak Height", yaxis_title="Expeditions with a death (%)")
            show_chart(fig)
            st.markdown(note("Peaks over 8,000 m are much more dangerous: 7.2% of expeditions there had at "
                             "least one death, compared with about 1% on lower peaks. 34 of the 37 expeditions "
                             "with a death were on 8,000 m peaks."), unsafe_allow_html=True)

    # ---------- Q2: Which season? ----------
    elif question == "Which season?":
        season = filtered.groupby("season").agg(
            success=("success", "mean"), deaths=("any_death", "mean"), trips=("success", "count")).reset_index()
        season["success"] = season["success"] * 100
        season["deaths"] = season["deaths"] * 100
        order = {"season": ["Spring", "Summer", "Autumn", "Winter"]}

        enough = season[season["trips"] >= 20]
        if len(enough) > 0:
            best = enough.sort_values("success", ascending=False).iloc[0]
            worst = enough.sort_values("deaths", ascending=False).iloc[0]
            if len(enough) == 1:
                text = f"{best['success']:.0f}% success, and {best['deaths']:.1f}% of trips had a death."
            elif best["season"] == worst["season"]:
                text = f"has the highest success ({best['success']:.0f}%) but also the most deaths ({best['deaths']:.1f}%)."
            else:
                text = f"has the highest success ({best['success']:.0f}%). {worst['season']} has the most deaths ({worst['deaths']:.1f}%)."
            st.markdown(insight(best["season"], text, "#2E8B6A"), unsafe_allow_html=True)
        else:
            st.markdown(insight("—", "Not enough trips in any season to compare.", "#2E8B6A"), unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            fig = px.bar(season, x="season", y="success", text_auto=".0f", hover_data=["trips"],
                         category_orders=order, title="Success Rate by Season", color_discrete_sequence=[BLUE])
            fig.update_layout(xaxis_title="Season", yaxis_title="Success rate (%)", yaxis_range=[0, 100])
            show_chart(fig)
            st.markdown(note("Spring has the highest success rate (76%), followed by autumn (66%). Winter is the "
                             "hardest season, with only 33% success. Summer has only 5 expeditions, so we can't "
                             "trust its rate."), unsafe_allow_html=True)
        with right:
            fig = px.bar(season, x="season", y="deaths", text_auto=".1f", hover_data=["trips"],
                         category_orders=order, title="Share of Expeditions With a Death, by Season",
                         color_discrete_sequence=["#C2483A"])
            fig.update_layout(xaxis_title="Season", yaxis_title="Expeditions with a death (%)")
            show_chart(fig)
            st.markdown(note("Spring is the most dangerous season (6.4% of expeditions had a death vs 2.1% in "
                             "autumn), even though it has the highest success rate. This is because most spring "
                             "expeditions are on 8,000 m peaks (77%). Winter and summer have too few expeditions "
                             "(21 and 5) to judge."), unsafe_allow_html=True)

    # ---------- Q3: Should I bring oxygen? ----------
    elif question == "Should I bring oxygen?":
        oxy = filtered.groupby("oxygen_used")["success"].agg(["mean", "count"]).reset_index()
        oxy["mean"] = oxy["mean"] * 100
        oxy["oxygen_used"] = oxy["oxygen_used"].map({True: "With oxygen", False: "Without oxygen"})

        ho = filtered.groupby(["height_group", "oxygen_used"], observed=True)["success"].agg(["mean", "count"]).reset_index()
        ho["mean"] = ho["mean"] * 100
        ho["oxygen_used"] = ho["oxygen_used"].map({True: "With oxygen", False: "Without oxygen"})

        high = ho[ho["height_group"] == "Over 8,000 m"]
        if len(high) == 2:
            no_o2 = high[high["oxygen_used"] == "Without oxygen"]["mean"].iloc[0]
            yes_o2 = high[high["oxygen_used"] == "With oxygen"]["mean"].iloc[0]
            st.markdown(insight(f"{no_o2:.0f}% → {yes_o2:.0f}%", "Above 8,000 m, oxygen changes everything.",
                                ORANGE), unsafe_allow_html=True)
        elif len(oxy) == 2:
            no_o2 = oxy[oxy["oxygen_used"] == "Without oxygen"]["mean"].iloc[0]
            yes_o2 = oxy[oxy["oxygen_used"] == "With oxygen"]["mean"].iloc[0]
            st.markdown(insight(f"{no_o2:.0f}% → {yes_o2:.0f}%", "Success without oxygen vs with oxygen.",
                                ORANGE), unsafe_allow_html=True)
        else:
            st.markdown(insight("—", "Only one group with these filters, so we can't compare oxygen.", ORANGE),
                        unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            fig = px.bar(oxy, x="oxygen_used", y="mean", color="oxygen_used", text_auto=".0f",
                         hover_data=["count"], title="Success Rate With and Without Oxygen",
                         color_discrete_map={"With oxygen": ORANGE, "Without oxygen": BLUE})
            fig.update_layout(showlegend=False, xaxis_title="Oxygen Used", yaxis_title="Success rate (%)",
                              yaxis_range=[0, 100])
            show_chart(fig)
            st.markdown(note("Oxygen has a big effect on success: 89% of expeditions with oxygen succeeded, "
                             "compared with only 55% without oxygen."), unsafe_allow_html=True)
        with right:
            fig = px.bar(ho, x="height_group", y="mean", color="oxygen_used", barmode="group", text_auto=".0f",
                         hover_data=["count"], title="Success Rate by Peak Height and Oxygen Use",
                         color_discrete_map={"With oxygen": ORANGE, "Without oxygen": BLUE})
            fig.update_layout(xaxis_title="Peak Height", yaxis_title="Success rate (%)", yaxis_range=[0, 100],
                              legend_title="")
            show_chart(fig)
            st.markdown(note("Without oxygen, success goes down as the peak gets higher. The biggest effect of "
                             "oxygen is on peaks over 8,000 m: only 14% of expeditions without oxygen succeeded, "
                             "compared with 89% with oxygen. On lower peaks almost nobody uses oxygen (only 3 and "
                             "10 expeditions), so we can't compare there."), unsafe_allow_html=True)

    # ---------- Q4: How big a team? ----------
    elif question == "How big a team?":
        team_rate = filtered.groupby("team_size", observed=True)["success"].agg(["mean", "count"]).reset_index()
        team_rate["mean"] = team_rate["mean"] * 100

        enough = team_rate[team_rate["count"] >= 20]
        if len(enough) > 0:
            best = enough.sort_values("mean", ascending=False).iloc[0]
            st.markdown(insight(f"{best['team_size']} climbers",
                                f"is the most successful team size ({best['mean']:.0f}%).", BLUE),
                        unsafe_allow_html=True)
        else:
            st.markdown(insight("—", "Not enough trips to compare team sizes.", BLUE), unsafe_allow_html=True)

        fig = px.bar(team_rate, x="team_size", y="mean", text_auto=".0f", hover_data=["count"],
                     title="Success Rate by Team Size", color_discrete_sequence=[BLUE])
        fig.update_layout(xaxis_title="Team Size (Number of Climbers)", yaxis_title="Success rate (%)",
                          yaxis_range=[0, 100])
        show_chart(fig)
        st.markdown(note("Bigger teams have higher success rates: from 57% for teams of 2–3 climbers to 88% for "
                         "teams of 13 or more."), unsafe_allow_html=True)

    # ---------- Q5: How many guides? ----------
    elif question == "How many guides?":
        guides = filtered.copy()
        guides["has_guides"] = guides["hired_staff"] > 0
        rate = guides.groupby("has_guides")["success"].agg(["mean", "count"]).reset_index()
        rate["mean"] = rate["mean"] * 100
        rate["has_guides"] = rate["has_guides"].map({True: "With hired staff", False: "No hired staff"})

        if len(rate) == 2:
            no_staff = rate[rate["has_guides"] == "No hired staff"]["mean"].iloc[0]
            with_staff = rate[rate["has_guides"] == "With hired staff"]["mean"].iloc[0]
            st.markdown(insight(f"{no_staff:.0f}% → {with_staff:.0f}%",
                                "Success without hired staff vs with staff.", ORANGE), unsafe_allow_html=True)
        else:
            st.markdown(insight("—", "Only one group with these filters, so we can't compare.", ORANGE),
                        unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            fig = px.bar(rate, x="has_guides", y="mean", text_auto=".0f", hover_data=["count"],
                         title="Success Rate With and Without Hired Staff", color_discrete_sequence=[ORANGE])
            fig.update_layout(xaxis_title="Has Hired Staff", yaxis_title="Success rate (%)", yaxis_range=[0, 100])
            show_chart(fig)
            st.markdown(note("Expeditions with hired staff succeeded 76% of the time, compared with only 43% for "
                             "expeditions without staff."), unsafe_allow_html=True)
        with right:
            fig = px.scatter(filtered, x="members", y="hired_staff", title="Number of Climbers vs Hired Staff",
                             opacity=0.6, color_discrete_sequence=[BLUE])
            fig.update_layout(xaxis_title="Number of Climbers", yaxis_title="Number of Hired Staff")
            show_chart(fig)
            st.markdown(note("There is a strong positive relationship between the number of climbers and the "
                             "number of hired staff (correlation = 0.79): bigger teams hire more staff."),
                        unsafe_allow_html=True)

    # ---------- Q6: How long will it take? ----------
    elif question == "How long will it take?":
        days = filtered.groupby("peak")["total_days"].agg(["median", "count"]).reset_index()
        days = days[days["count"] >= 10].sort_values("median")

        if len(days) == 0:
            st.markdown(insight("—", "Not enough trips with known dates for these filters.", BLUE),
                        unsafe_allow_html=True)
        else:
            short = days.iloc[0]
            long = days.iloc[-1]
            if len(days) == 1:
                st.markdown(insight(f"{short['median']:.0f} days", f"Typical trip length on {short['peak']}.", BLUE),
                            unsafe_allow_html=True)
            else:
                st.markdown(insight(f"{short['median']:.0f} → {long['median']:.0f} days",
                                    f"From {short['peak']} (shortest) to {long['peak']} (longest).", BLUE),
                            unsafe_allow_html=True)
            fig = px.bar(days, x="median", y="peak", orientation="h", text_auto=".0f", hover_data=["count"],
                         title="Typical Trip Length on the Most Climbed Mountains", color_discrete_sequence=[BLUE])
            fig.update_layout(xaxis_title="Median number of days", yaxis_title="Mountain")
            show_chart(fig)
        st.markdown(note("I only included mountains with at least 10 expeditions with known trip length. Ama "
                         "Dablam is the shortest trip (about 13 days), while Everest and Lhotse are the longest "
                         "(about 34–35 days). Higher mountains need longer trips."), unsafe_allow_html=True)

    # ---------- Q7: What could stop me? ----------
    elif question == "What could stop me?":
        failed = filtered[filtered["success"] == False]
        if len(failed) == 0:
            st.markdown(insight("0", "No failed expeditions with these filters.", "#C2483A"), unsafe_allow_html=True)
        else:
            nature = failed["end_reason"].str.startswith(("Bad weather", "Bad conditions")).mean() * 100
            st.markdown(insight(f"{nature:.0f}%", "of failed expeditions were stopped by nature: bad weather or "
                                                  "bad conditions (snow, avalanches).", "#C2483A"),
                        unsafe_allow_html=True)
            reasons = failed["end_reason"].value_counts().reset_index()
            reasons.columns = ["reason", "trips"]
            reasons = reasons.sort_values("trips")
            fig = px.bar(reasons, x="trips", y="reason", orientation="h", text_auto=True,
                         title="Why Expeditions Failed", color_discrete_sequence=["#C2483A"])
            fig.update_layout(xaxis_title="Number of Expeditions", yaxis_title="", height=500)
            show_chart(fig)
        st.markdown(note("About half of the failed expeditions (132 of 257) failed because of nature: bad weather "
                         "or bad conditions. \"Success (subpeak)\" means the team reached a lower summit, not the "
                         "main one."), unsafe_allow_html=True)

    # ---------- Q8: Which company? ----------
    else:
        agencies = filtered[filtered["agency"] != "Unknown"]
        company = agencies.groupby("agency")["success"].agg(["mean", "count"]).reset_index()
        company = company[company["count"] >= 20].copy()

        if len(company) == 0:
            st.markdown(insight("—", "No company has 20 or more expeditions with these filters.", BLUE),
                        unsafe_allow_html=True)
        else:
            company["mean"] = company["mean"] * 100
            company = company.sort_values("mean", ascending=False)
            company["rank"] = range(1, len(company) + 1)
            largest = company.sort_values("count", ascending=False).iloc[0]
            if len(company) == 1:
                text = f"Only {largest['agency']} has 20 or more trips with these filters."
            elif largest["rank"] == 1:
                text = f"{largest['agency']} has the most trips ({largest['count']}) and the highest success."
            else:
                text = f"{largest['agency']} has the most trips ({largest['count']}) but is not the most successful."
            st.markdown(insight(f"#{largest['rank']} of {len(company)}", text, BLUE), unsafe_allow_html=True)

            company["highlight"] = "Other"
            company.loc[company["agency"] == largest["agency"], "highlight"] = "Largest"
            company = company.sort_values("mean")
            fig = px.bar(company, x="mean", y="agency", orientation="h", text_auto=".0f",
                         hover_data={"count": True, "highlight": False}, title="Success Rate of the Main Climbing Companies",
                         color="highlight", color_discrete_map={"Largest": BLUE, "Other": ORANGE})
            fig.update_layout(showlegend=False, xaxis_title="Success rate (%)", yaxis_title="Company",
                              xaxis_range=[0, 100])
            show_chart(fig)
        st.markdown(note("I only included companies with at least 20 expeditions, because a success rate from a "
                         "few trips can be misleading. Elite Exped has the highest success rate (90%). The biggest "
                         "company, Seven Summit Treks (119 expeditions), is only 9th (71%), so the biggest is not "
                         "always the best."), unsafe_allow_html=True)

# ===== Tab 2: Check my plan =====
with tab2:
    st.subheader("Check my plan")
    st.write("Enter your planned expedition and compare it with 868 past expeditions.")

    left, right = st.columns([1.1, 1])

    # ---- Left: the plan (white card) ----
    with left:
        with st.form("plan_form"):
            st.markdown(PLAN_TITLE, unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            p_mountain = c1.selectbox("Mountain", list(df["peak"].value_counts().index))
            p_season = c2.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
            p_members = c1.number_input("Team size (climbers)", min_value=1, max_value=40, value=8)
            p_staff = c2.number_input("Hired staff", min_value=0, max_value=60, value=10)

            p_oxygen = st.toggle("I will use supplemental oxygen", value=True)
            submitted = st.form_submit_button("Check my plan →", type="primary")

    # keep the result on the page after the first click
    if submitted:
        st.session_state["checked"] = True

    # ---- Right: the result (dark card) ----
    with right:
        if not st.session_state.get("checked", False):
            st.markdown(result_card_empty(), unsafe_allow_html=True)
        else:
            height = df[df["peak"] == p_mountain]["height_m"].iloc[0]

            # 1) model prediction
            plan = pd.DataFrame({
                "oxygen_used": [p_oxygen],
                "members": [p_members],
                "hired_staff": [p_staff],
                "height_m": [height / 1000],
                "season": [p_season],
            })
            plan = pd.get_dummies(plan, columns=["season"])
            plan = plan.reindex(columns=model_columns, fill_value=0)
            chance = model.predict_proba(plan)[0][1] * 100

            # 2) tips: (type, text)   type = "good", "warn" or "bad"
            tips = []
            if height >= 8000 and p_oxygen:
                tips.append(("good", "Oxygen planned: 89% success above 8,000 m vs 14% without"))
            if height >= 8000 and not p_oxygen:
                tips.append(("bad", "No oxygen above 8,000 m: only 14% succeeded (vs 89% with oxygen)"))

            if p_season == "Spring":
                tips.append(("good", "Spring is the most successful season (76%)"))
            elif p_season == "Autumn":
                tips.append(("good", "Autumn is the second best season (66%)"))
            elif p_season == "Winter":
                tips.append(("bad", "Winter is the hardest season: only 33% success"))
            else:
                tips.append(("warn", "Very few expeditions climb in summer (only 5 trips)"))

            if p_staff == 0:
                tips.append(("warn", "Teams without hired staff succeeded only 43% of the time"))

            peak_trips = df[df["peak"] == p_mountain]
            trip_days = peak_trips["total_days"].median()
            if not pd.isna(trip_days):
                tips.append(("warn", f"Plan about {trip_days:.0f} days: the typical {p_mountain} trip"))

            similar = peak_trips[(peak_trips["season"] == p_season) & (peak_trips["oxygen_used"] == p_oxygen)]
            if len(similar) >= 5:
                tips.append(("good", f"{len(similar)} similar past trips: {similar['success'].mean() * 100:.0f}% reached the summit"))
            elif len(similar) > 0:
                tips.append(("warn", f"Only {len(similar)} similar past trip(s), so we can't compare much"))

            if height >= 8000:
                tips.append(("bad", "8,000 m peaks are riskier: 7.2% of trips had a death"))

            # short description of the plan
            if height >= 8000:
                peak_type = "8,000 m peak"
            else:
                peak_type = "peak under 8,000 m"
            if p_oxygen:
                oxygen_text = "oxygen"
            else:
                oxygen_text = "no oxygen"
            description = f"{peak_type}, {p_season.lower()}, {oxygen_text}, {p_staff} hired staff"

            st.markdown(result_card(chance, description, tips), unsafe_allow_html=True)

# ===== Tab 3: Data =====
with tab3:
    st.subheader("Data preview")
    st.write(f"Showing **{len(filtered)}** expeditions after filters (out of {len(df)}).")

    # all the columns of the clean data (without the helper columns made in the app)
    helper_columns = ["any_death", "height_group", "team_size"]
    columns = [col for col in filtered.columns if col not in helper_columns]
    st.dataframe(filtered[columns], use_container_width=True, hide_index=True)

    st.subheader("Summary statistics")

    # number columns: mean, min, max...
    st.markdown("**Number columns**")
    st.dataframe(filtered[columns].describe().round(1), use_container_width=True)

    # text and True/False columns: how many values, how many different values, the most common one
    st.markdown("**Text and True/False columns**")
    text_stats = filtered[columns].describe(include=["object", "bool"])
    text_stats.index = ["count", "different values", "most common", "times of most common"]
    st.dataframe(text_stats.astype(str), use_container_width=True)

    st.download_button("Download filtered data (CSV)",
                       data=filtered[columns].to_csv(index=False),
                       file_name="himalayan_expeditions_filtered.csv",
                       mime="text/csv")
