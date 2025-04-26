import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return 

df = pd.read_csv("fake_ess_data.csv")

# Sidebar Filters
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Select Country", df["country"].unique())

# Main Dashboard
st.title("European Well-Being Dashboard")
st.write("Visualising well-being across ESS data.")

#New Section-------------------------------------------------------------------------------------------------------------------------------------
filtered_df = df[df["country"] == country]
# Line Chart for Life Satisfaction
st.subheader(f"Life Satisfaction Trend in {country}")
fig = px.line(filtered_df, x="year", y="life_satisfaction", title="Life Satisfaction Over Time")
st.plotly_chart(fig)

# Bar Chart for Key Well-Being Factors
st.subheader(f"Well-Being Breakdown in {country}")
factors = ["income", "social_trust", "health"]
fig = px.bar(filtered_df, x="year", y=factors, barmode="group", title="Key Well-Being Indicators")
st.plotly_chart(fig)

# Show Data Table
st.subheader("Data Preview")
st.dataframe(filtered_df)

# End of section --------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------
# New Section: Granger Causality Visualization
st.sidebar.header("Granger Causality Visualizations")
visualization_choice = st.sidebar.selectbox(
    "Select Visualization", 
    ["Bar Chart", "Heatmap", "Network Graph", "Line Plot", "Box Plot"]
)

st.sidebar.header("Granger Causality Filter")
p_value_threshold = st.sidebar.slider("Select P-value Threshold", 0.0, 1.0, 0.05)
causality_data = pd.read_csv("test_causality_data.csv")
filtered_causality_data = causality_data[causality_data['p_value'] < p_value_threshold]

# Show filtered Granger causality data
st.subheader("Granger Causality Results")
st.write(f"Showing causality relationships with p-value < {p_value_threshold}")
st.dataframe(filtered_causality_data)
filtered_causality_data['causality_pair'] = filtered_causality_data['causality_from'] + ' -> ' + filtered_causality_data['causality_to']

# Step 1: Bar Chart for Causality
if visualization_choice == "Bar Chart":
    if not filtered_causality_data.empty:
        fig_causality = px.bar(filtered_causality_data, x="causality_pair", y="p_value", 
                            title="Granger Causality Test Results (P-values)", labels={'p_value': 'P-value', 'causality_pair': 'Causality Relationship'})
        st.plotly_chart(fig_causality)


# --------------------------------------
# New Section: Batch Data Display
batch_size = st.sidebar.slider("Batch Size", 10, 100, 50)
num_batches = len(filtered_df) // batch_size + 1
batch_index = st.sidebar.slider("Select Batch", 0, num_batches - 1)

start_idx = batch_index * batch_size
end_idx = min((batch_index + 1) * batch_size, len(filtered_df))

# Display selected batch of the filtered data
st.subheader(f"Displaying Batch {batch_index + 1}/{num_batches}")
st.dataframe(filtered_df.iloc[start_idx:end_idx])

# End of section --------------------------------------------------------------------------------------------------------------------------------------

df = pd.read_csv("your_file.csv")  # Update with actual file
df = df[df['stflife'].between(0, 10)]  # Clean life satisfaction
df = df[df['hinctnta'].between(1, 10)]  # Clean income
df = df[df['ppltrst'].between(0, 10)]  # Clean social trust (optional)

# Sidebar for user input
st.sidebar.header("Select a Factor")
selected_factor = st.sidebar.selectbox(
    "Choose a factor to compare with Life Satisfaction:",
    ["Income", "Social Trust", "Employment Status"]
)

# Map selection to correct column
factor_map = {
    "Income": "hinctnta",
    "Social Trust": "ppltrst",
    "Employment Status": "uempla"
}
factor_column = factor_map[selected_factor]

# Generate boxplot
st.title("Well-Being Dashboard")
st.subheader(f"Life Satisfaction vs. {selected_factor}")

fig = px.box(df, x=factor_column, y="stflife",
             labels={factor_column: selected_factor, "stflife": "Life Satisfaction"},
             title=f"Life Satisfaction vs. {selected_factor}")

st.plotly_chart(fig)

# Show correlation
correlation = df[[factor_column, "stflife"]].corr().iloc[0, 1]
st.write(f"**Correlation between {selected_factor} and Life Satisfaction:** {correlation:.3f}")


# Creating the final theme groupings based on the variables provided and earlier discussions

theme_groupings = {
    "subjective_wellbeing": [
        "happy", "wrhpp", "ctrlife", "enjlf"
    ],
    "mental_distress": [
        "fltdpr", "fltsd", "fltlnl", "flteeff", "cldgng", "slprl"
    ],
    "institutional_trust": [
        "trstplc", "trstlgl", "trstprl", "trstplt", "trstprt", "trstun", "trstep","stfhlth", "stfedu", "stfgov"
    ],
    "social_trust_support": [
        "ppltrst", "pplhlp", "pplfair", "inprdsc", "sclmeet"
    ],
    "health_limitations": [
        "hlthhmp", "health", "dsbld"
    ],

    "economic_status": [
        "hinctnta", "uempla", "fnsdfml", "wkhtot", "wkhct","stfeco"
    ],
    "civic_engagement": [
        "vote", "contplt", "actrolga", "cptppola", "iorgact", "psppipla"
    ],
    "values_identity": [
        "iplylfra", "ipudrsta", "ipcrtiva", "impfreea", "impsafea"
    ]
    "safety_security" : [
        "aesfdrk", 
    ]
}

import pandas as pd
theme_df = pd.DataFrame(
    [(theme, var) for theme, vars in theme_groupings.items() for var in vars],
    columns=["Theme", "Variable"]
)

import ace_tools as tools; tools.display_dataframe_to_user(name="Theme Groupings", dataframe=theme_df)

themes = {
    "subjective_wellbeing": ["happy", "wrhpp", "enjlf", "ctrlife"],
    "mental_distress": ["fltdpr", "fltsd", "fltlnl", "flteeff", "cldgng", "slprl"],
    "health_limitations": ["health", "hlthhmp"],
    "institutional_trust": ["trstplt", "trstprt", "trstprl", "trstlgl", "trstplc", "trstun", "trstep"],
    "institutional_satisfaction": ["stfgov", "stfdem", "stfhlth", "stfedu", "stfeco"],
    "social_trust": ["pplfair", "ppltrst", "pplhlp"],
    "economic_status": ["hinctnta", "fnsdfml", "wkhtot", "wkhct", "uempla", "wkdcorga", "pdwrk", "mainact"],
    "social_networks": ["inprdsc", "sclmeet", "sclact"],
    "civic_engagement": ["vote", "polintr", "actrolga", "iorgact", "contplt", "pstplonl", "sgnptit", "donprty", "pbldmna"],
    "safety_security": ["aesfdrk", "crmvct", "impsafea"],
    "political_efficacy": ["psppipla", "psppsgva", "cptppola"],
    "discrimination": ["dscrgrp", "dscrntn", "dscrrce", "dscrage", "dscrsex", "dscrgnd", "dscrref", "dscretn", "dscrnap", "dscrdk"],
    "education" : ["eduyrs", "eisced"],
    "demographics": ["agea", "gndr", "eduyrs", "eisced"],
    "values": ["ipgdtima", "iplylfra", "ipudrsta", "iphlppla", "ipcrtiva", "impfreea", "impfuna", "sothnds", "ipdiffa", "impenva", "ipeqopta", "ipbhprpa", "ipmodsta", "ipshabta", "imptrada", "ipfrulea", "ipstrgva", "iprspota"]

}