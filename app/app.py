import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LogisticRegression

from style import CSS, HERO, ORANGE, BLUE, BRAND

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
    X = data[["oxygen_used", "members", "hired_staff", "height_m", "season", "commercial_route"]].copy()
    X["height_m"] = X["height_m"] / 1000          # height in km
    X = pd.get_dummies(X, columns=["season"])     # season → columns
    y = data["success"]
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model, X.columns


model, model_columns = train_model(df)

# ---------- Sidebar ----------
st.sidebar.markdown(BRAND, unsafe_allow_html=True)

with st.sidebar.expander("ℹ️ About this dashboard"):
    st.write("A data dashboard for climbers planning a Himalayan expedition. "
             "Explore which mountain, season, company and gear give you the best "
             "chance to reach the summit safely.")
    st.caption("Data: The Himalayan Database via TidyTuesday (2025-01-21). 868 expeditions, 2020–2024.")

st.sidebar.divider()
st.sidebar.subheader("Filters")
# 1) Mountain
mountains = ["All mountains"] + list(df["peak"].value_counts().index)
mountain = st.sidebar.selectbox("Mountain", mountains)

# 2) Season
seasons = st.sidebar.multiselect("Season", ["Spring", "Summer", "Autumn", "Winter"],
                                 default=["Spring", "Summer", "Autumn", "Winter"])

# 3) Peak height
heights = st.sidebar.multiselect("Peak height", ["Under 7,000 m", "7,000-8,000 m", "Over 8,000 m"],
                                 default=["Under 7,000 m", "7,000-8,000 m", "Over 8,000 m"])

# 4) Oxygen
oxygen = st.sidebar.radio("Oxygen", ["All", "Used oxygen", "No oxygen"], horizontal=True)

# 5) Team size
min_team = int(df["members"].min())
max_team = int(df["members"].max())
team = st.sidebar.slider("Team size (climbers)", min_team, max_team, (min_team, max_team))

# ---------- Apply filters ----------
filtered = df.copy()

if mountain != "All mountains":
    filtered = filtered[filtered["peak"] == mountain]

filtered = filtered[filtered["season"].isin(seasons)]
filtered = filtered[filtered["height_group"].isin(heights)]

if oxygen == "Used oxygen":
    filtered = filtered[filtered["oxygen_used"] == True]
elif oxygen == "No oxygen":
    filtered = filtered[filtered["oxygen_used"] == False]

filtered = filtered[(filtered["members"] >= team[0]) & (filtered["members"] <= team[1])]

# stop if no data
if len(filtered) == 0:
    st.warning("No expeditions match these filters. Try changing them.")
    st.stop()

# ---------- Hero banner ----------
st.markdown(HERO, unsafe_allow_html=True)

# ---------- KPI cards ----------
all_success = df["success"].mean() * 100
success = filtered["success"].mean() * 100
death = filtered["any_death"].mean() * 100
days = filtered["total_days"].median()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Expeditions", len(filtered))

if len(filtered) == len(df):
    col2.metric("Success rate", f"{success:.0f}%")
else:
    col2.metric("Success rate", f"{success:.0f}%",
                delta=f"{success - all_success:.0f} pts vs all")

col3.metric("Expeditions with a death", f"{death:.1f}%")

if pd.isna(days):
    col4.metric("Median trip length", "No data")
else:
    col4.metric("Median trip length", f"{days:.0f} days")

st.divider()

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🧗 Check my plan", "🗂 Data"])

# ===== Tab 1: Overview =====
with tab1:
    left, right = st.columns(2)

    # ---- Chart 1: Oxygen ----
    with left:
        st.subheader("Oxygen is the biggest factor")
        oxy = filtered.groupby("oxygen_used")["success"].mean().reset_index()
        oxy["success"] = oxy["success"] * 100
        oxy["oxygen_used"] = oxy["oxygen_used"].map({True: "With oxygen", False: "Without oxygen"})

        fig = px.bar(oxy, x="oxygen_used", y="success", color="oxygen_used", text_auto=".0f",
                     color_discrete_map={"With oxygen": ORANGE, "Without oxygen": BLUE})
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Success rate (%)", yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    # ---- Chart 2: Season ----
    with right:
        st.subheader("Success rate by season")
        season = filtered.groupby("season")["success"].agg(["mean", "count"]).reset_index()
        season["mean"] = season["mean"] * 100

        fig = px.bar(season, x="season", y="mean", text_auto=".0f", hover_data=["count"],
                     category_orders={"season": ["Spring", "Summer", "Autumn", "Winter"]},
                     color_discrete_sequence=[BLUE])
        fig.update_layout(xaxis_title="", yaxis_title="Success rate (%)", yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    # ---- Chart 3: Height x Oxygen ----
    with left:
        st.subheader("Success by peak height and oxygen")
        ho = filtered.groupby(["height_group", "oxygen_used"], observed=True)["success"].agg(["mean", "count"]).reset_index()
        ho["mean"] = ho["mean"] * 100
        ho["oxygen_used"] = ho["oxygen_used"].map({True: "With oxygen", False: "Without oxygen"})

        fig = px.bar(ho, x="height_group", y="mean", color="oxygen_used", barmode="group",
                     text_auto=".0f", hover_data=["count"],
                     color_discrete_map={"With oxygen": ORANGE, "Without oxygen": BLUE})
        fig.update_layout(xaxis_title="", yaxis_title="Success rate (%)", yaxis_range=[0, 100], legend_title="")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Hover on a bar to see the number of trips. Bars with few trips are not reliable.")

    # ---- Chart 4: Companies ----
    with right:
        st.subheader("Success rate of companies")
        agencies = filtered[filtered["agency"] != "Unknown"]
        company = agencies.groupby("agency")["success"].agg(["mean", "count"]).reset_index()
        company = company[company["count"] >= 10].sort_values("mean")
        company["mean"] = company["mean"] * 100

        if len(company) == 0:
            st.info("No company has 10 or more expeditions with these filters.")
        else:
            fig = px.bar(company, x="mean", y="agency", orientation="h", text_auto=".0f",
                         hover_data=["count"], color_discrete_sequence=[ORANGE])
            fig.update_layout(xaxis_title="Success rate (%)", yaxis_title="", xaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Only companies with 10 or more expeditions.")

    # ---- Key insights ----
    st.divider()
    st.subheader("💡 Key insights")

    i1, i2, i3, i4 = st.columns(4)
    i1.metric("Oxygen", "+34 pts", help="Success with oxygen 89% vs 55% without")
    i1.caption("Oxygen raises success from 55% to 89%.")

    i2.metric("Best season", "Spring", help="76% success in spring")
    i2.caption("Spring has the highest success rate (76%).")

    i3.metric("Deaths above 8,000 m", "92%", help="34 of 37 expeditions with a death")
    i3.caption("Almost all expeditions with a death were on 8,000 m peaks.")

    i4.metric("Largest company", "9th", help="Seven Summit Treks: 119 trips, 71% success")
    i4.caption("The biggest company is not the most successful.")

# ===== Tab 2: Check my plan =====
with tab2:
    st.subheader("🧗 Check my plan")
    st.write("Enter your planned expedition and compare it with 868 past expeditions.")

    left, right = st.columns(2)

    # ---- Inputs ----
    with left:
        with st.form("plan_form"):
            p_mountain = st.selectbox("Mountain", list(df["peak"].value_counts().index))
            p_season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
            p_members = st.number_input("Team size (climbers)", min_value=1, max_value=40, value=6)
            p_staff = st.number_input("Hired staff", min_value=0, max_value=60, value=5)
            p_oxygen = st.checkbox("I will use supplemental oxygen", value=True)
            p_route = st.checkbox("Commercial route", value=True)
            submitted = st.form_submit_button("Check my plan →")

    # ---- Result ----
    with right:
        if not submitted:
            st.info("Fill in your plan and press **Check my plan**.")
        else:
            height = df[df["peak"] == p_mountain]["height_m"].iloc[0]

            # 1) model prediction
            plan = pd.DataFrame({
                "oxygen_used": [p_oxygen],
                "members": [p_members],
                "hired_staff": [p_staff],
                "height_m": [height / 1000],
                "season": [p_season],
                "commercial_route": [p_route],
            })
            plan = pd.get_dummies(plan, columns=["season"])
            plan = plan.reindex(columns=model_columns, fill_value=0)
            chance = model.predict_proba(plan)[0][1] * 100

            st.metric("Estimated chance of success", f"{chance:.0f}%")
            st.progress(int(chance))

            # 2) similar past trips
            peak_trips = df[df["peak"] == p_mountain]
            similar = peak_trips[(peak_trips["season"] == p_season) & (peak_trips["oxygen_used"] == p_oxygen)]

            st.write(f"**{p_mountain}** · {height} m")
            if len(similar) > 0:
                st.write(f"Similar past trips (same mountain, season and oxygen): **{len(similar)}**, "
                         f"and **{similar['success'].mean() * 100:.0f}%** reached the summit.")
            else:
                st.write("No similar past trips in the data.")

            trip_days = peak_trips["total_days"].median()
            if not pd.isna(trip_days):
                st.write(f"Typical trip length on {p_mountain}: **{trip_days:.0f} days**")

            # 3) tips from the EDA
            st.markdown("**Tips**")
            if height >= 8000 and not p_oxygen:
                st.error("Above 8,000 m, only 14% of expeditions without oxygen succeeded (vs 89% with oxygen).")
            if p_season == "Spring":
                st.success("Spring is the most successful season (76%).")
            if p_season == "Winter":
                st.warning("Winter is the hardest season: only 33% success.")
            if p_staff == 0:
                st.warning("Expeditions without hired staff succeeded only 43% of the time.")
            if height >= 8000:
                st.warning("8,000 m peaks are riskier: 7.2% of expeditions there had a death.")

            st.caption("Estimate from a logistic regression model trained on past expeditions. Not a guarantee.")

# ===== Tab 3: Data =====
with tab3:
    st.subheader("🗂 Data preview")
    st.write(f"Showing **{len(filtered)}** expeditions after filters (out of {len(df)}).")

    columns = ["peak", "year", "season", "height_m", "members", "hired_staff",
               "oxygen_used", "commercial_route", "agency", "success", "total_days"]
    st.dataframe(filtered[columns], use_container_width=True, hide_index=True)

    st.subheader("📈 Summary statistics")
    st.dataframe(filtered[["height_m", "members", "hired_staff", "total_days"]].describe().round(1),
                 use_container_width=True)

    st.download_button("⬇️ Download filtered data (CSV)",
                       data=filtered.to_csv(index=False),
                       file_name="himalayan_expeditions_filtered.csv",
                       mime="text/csv")