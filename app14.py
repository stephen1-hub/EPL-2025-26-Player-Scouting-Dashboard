import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

st.title("⚽ EPL 2025/2026 Player Scouting Dashboard")

st.markdown("""
This interactive dashboard analyzes player performance in the English Premier League (2025/26 season) 
using expected goals (xG) and expected assists (xA).

Key objectives:
- Identify high-impact players  
- Detect hidden gems  
- Evaluate team dependency  
- Support recruitment decisions  
""")

st.info(
    "📌 Insight: A small number of players generate a disproportionately large share of attacking output "
    "across the EPL, highlighting the importance of elite attackers and system dependency."
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("league-players.xlsx")

    # Clean team names
    df["team"] = df["team"].str.split(",").str[0]

    # Metrics
    df["total_xG_xA"] = df["xG"] + df["xA"]
    df["total_xG_xA90"] = df["xG90"] + df["xA90"]
    df["finishing_diff"] = df["goals"] - df["xG"]

    # Team totals
    team_totals = df.groupby("team")["total_xG_xA"].sum().reset_index()
    team_totals.rename(columns={"total_xG_xA": "team_total_xG_xA"}, inplace=True)

    df = df.merge(team_totals, on="team", how="left")

    # Contribution %
    df["team_contribution_pct"] = df["total_xG_xA"] / df["team_total_xG_xA"]

    return df

df = load_data()

# -----------------------------
# LEAGUE OVERVIEW
# -----------------------------
st.subheader("📊 League Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Players", len(df))
col2.metric("Total Teams", df["team"].nunique())
col3.metric("Avg xG per Player", round(df["xG"].mean(), 2))

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

min_minutes = st.sidebar.slider("Minimum Minutes", 0, 3000, 900)

team = st.sidebar.selectbox(
    "Select Team",
    ["All"] + sorted(df["team"].unique())
)

player_search = st.sidebar.selectbox(
    "🔎 Player Scouting Report",
    ["None"] + sorted(df["player"].unique())
)

# Apply filters
df_filtered = df[df["min"] >= min_minutes]

if team != "All":
    df_filtered = df_filtered[df_filtered["team"] == team]

# -----------------------------
# PLAYER SCOUTING REPORT
# -----------------------------
if player_search != "None":
    player_data = df[df["player"] == player_search].iloc[0]

    st.subheader(f"📋 Scouting Report: {player_search}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Goals", player_data["goals"])
    col2.metric("xG", round(player_data["xG"], 2))
    col3.metric("xA", round(player_data["xA"], 2))

    col4, col5 = st.columns(2)
    col4.metric("xG+xA (90)", round(player_data["total_xG_xA90"], 2))
    col5.metric("Team Contribution %", round(player_data["team_contribution_pct"] * 100, 1))

    st.markdown("---")

# -----------------------------
# SECTION 1: TOP PERFORMERS
# -----------------------------
st.subheader("📊 Top Performers (Per 90 Output)")

top_per90 = df_filtered.sort_values("total_xG_xA90", ascending=False).head(10)

st.dataframe(top_per90[[
    "player", "team", "total_xG_xA90", "xG90", "xA90"
]])

if st.button("💡 Insight: Per 90 Output"):
    st.info(
        "Players with the highest xG+xA per 90 generate the most attacking impact per minute. "
        "This highlights both elite performers and hidden gems."
    )

# -----------------------------
# SECTION 2: FINISHING
# -----------------------------
st.subheader("🎯 Finishing Efficiency")

fig1, ax1 = plt.subplots()
ax1.scatter(df_filtered["xG"], df_filtered["goals"])
ax1.set_xlabel("xG")
ax1.set_ylabel("Goals")
ax1.set_title("Goals vs Expected Goals")
st.pyplot(fig1)

if st.button("💡 Insight: Finishing"):
    st.info(
        "Players above the trend are overperforming, while those below are underperforming. "
        "Underperformers can be strong buy-low targets."
    )

# -----------------------------
# SECTION 3: HIDDEN GEMS
# -----------------------------
st.subheader("💎 Hidden Gems")

hidden_gems = df[
    (df["min"] < 1200) &
    (df["total_xG_xA90"] > 0.6)
].sort_values("total_xG_xA90", ascending=False)

st.dataframe(hidden_gems[[
    "player", "team", "min", "total_xG_xA90"
]])

if st.button("💡 Insight: Hidden Gems"):
    st.info(
        "Low-minute players with high per-90 output are potential breakout stars and smart recruitment targets."
    )

# -----------------------------
# SECTION 4: TEAM DEPENDENCY
# -----------------------------
st.subheader("🏗️ Team Dependency")

top_dependency = df_filtered.sort_values(
    "team_contribution_pct", ascending=False
).head(10)

st.dataframe(top_dependency[[
    "player", "team", "team_contribution_pct"
]])

if st.button("💡 Insight: Team Dependency"):
    st.info(
        "Higher percentages indicate players who carry a large share of team attack — valuable but risky dependency."
    )

# -----------------------------
# SECTION 5: ROLE PROFILE
# -----------------------------
st.subheader("⚖️ Role Profile")

fig2, ax2 = plt.subplots()
ax2.scatter(df_filtered["xG90"], df_filtered["xA90"])
ax2.set_xlabel("xG per 90")
ax2.set_ylabel("xA per 90")
ax2.set_title("Scorer vs Creator")
st.pyplot(fig2)

if st.button("💡 Insight: Role Profile"):
    st.info(
        "Right = scorers, Top = creators. Balanced players contribute in both areas."
    )

# -----------------------------
# FINAL TAKEAWAYS
# -----------------------------
st.subheader("🧾 Key Takeaways")

if st.button("📌 Show Final Insights"):
    st.markdown("""
- ⭐ Elite attackers dominate team output  
- 🎯 Creative players drive attacking systems  
- 💎 Hidden gems exist in low-minute players  
- 🏗️ High contribution % = system dependency  
- ⚖️ Balanced teams spread attacking responsibility  
""")