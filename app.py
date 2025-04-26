# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import json

# ------------------ Data Loading ------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/year_2023_cleaned.csv")

df = load_data()
country_df = pd.read_csv("data/country_data.csv")
data = country_df.copy()
trans_df = pd.read_csv("data/trans_correlation_results.csv", index_col="Country")

with open('data/correlation_results.json', 'r') as f:
    correlations = json.load(f)

with open('data/column_descriptions.json', 'r') as f:
    column_to_description = json.load(f)

with open('data/explanation.json', 'r') as f:
    graph_explanations = json.load(f)

with open('data/country_correlation_results.json', 'r') as f:
    country_correlations = json.load(f)

# ------------------ App Starts ------------------

st.title("Life Satisfaction Across Europe: Analysis of the European Social Survey (2023)")

st.header("Introduction")

st.markdown("""
This dashboard explores factors influencing **life satisfaction across European countries**, based on data from the **2023 European Social Survey (ESS)**. 
The objective is to identify patterns, regional differences, and key correlates of well-being, helping to uncover broader social, economic, and psychological drivers of life satisfaction.
 
Using a combination of descriptive statistics, correlation analysis, and visualisation techniques, we investigate relationships between life satisfaction and variables such as **social trust**, **institutional trust**, **mental health**, and **economic status**.

All data used in this analysis is fully anonymised and adheres to ethical research guidelines.
""")


# ------------------ General Overview ------------------

variables = df.columns.tolist()
variable_mapping = {
    'agea': 'age_group',
    'eduyrs': 'education_group',
}

st.header("Life Satisfaction Overview")

country_life_sat = data.groupby('cntry')['stflife'].mean().sort_values()

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(country_life_sat.index, country_life_sat.values, color='royalblue')
ax.set_xlabel('Average Life Satisfaction')
ax.set_ylabel('Country')
ax.set_title('Life Satisfaction Across Countries')
ax.invert_yaxis()
st.pyplot(fig)

st.write("Most countries have a life satisfaction score between 6 and 8, slightly skewed to the right.")

fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(data['stflife'], bins=10, kde=True, color='royalblue', ax=ax)
ax.set_xlabel('Life Satisfaction Score')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Life Satisfaction Scores')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 5))
data['stflife'].hist(bins=11, edgecolor='black', ax=ax)
ax.set_title("Distribution of Life Satisfaction (0–10)")
ax.set_xlabel("Life Satisfaction")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# ------------------ Regional Analysis ------------------

st.header("Life Satisfaction by Region")

regions = {
    'Northern Europe': ['DK', 'EE', 'FI', 'IS', 'LT', 'LV', 'NO', 'SE'],
    'Western Europe': ['AT', 'BE', 'CH', 'DE', 'FR', 'GB', 'IE', 'LU', 'NL'],
    'Eastern Europe': ['BG', 'CZ', 'HR', 'HU', 'PL', 'RO', 'RS', 'RU', 'SI', 'SK', 'UA'],
    'Southern Europe': ['AL', 'CY', 'ES', 'GR', 'IT', 'ME', 'MK', 'PT', 'TR', 'XK']
}

# Map countries to regions
country_to_region = {country: region for region, countries in regions.items() for country in countries}
data['region'] = data['cntry'].map(country_to_region)

region_life_sat = data.groupby('region')['stflife'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(region_life_sat.index, region_life_sat.values, color=['royalblue', 'darkorange', 'seagreen', 'crimson'])
ax.set_xlabel('Average Life Satisfaction')
ax.set_ylabel('Region')
ax.set_title('Life Satisfaction Across European Regions')
st.pyplot(fig)

# ------------------ Statistical Tests ------------------

st.header("Statistical Test Results")

anova_result = pd.DataFrame({
    "Statistic": ["F-statistic"],
    "Value": [508.728]
})

tukey_data = {
    "Group 1": ["Eastern Europe", "Eastern Europe", "Eastern Europe", 
                "Northern Europe", "Northern Europe", "Southern Europe"],
    "Group 2": ["Northern Europe", "Southern Europe", "Western Europe", 
                "Southern Europe", "Western Europe", "Western Europe"],
    "Mean Difference": [0.7527, -0.2242, 0.5882, -0.9769, -0.1646, 0.8123],
    "p-value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Lower Bound": [0.67, -0.2982, 0.5211, -1.0594, -0.2408, 0.7456],
    "Upper Bound": [0.8355, -0.1501, 0.6552, -0.8944, -0.0883, 0.8791],
    "Significant?": [True, True, True, True, True, True]
}
tukey_df = pd.DataFrame(tukey_data)

st.subheader("ANOVA Test Result")
st.table(anova_result)

st.subheader("Tukey HSD Test Results")
st.dataframe(tukey_df)

# ------------------ Correlations ------------------

st.header("Correlations with Life Satisfaction")

selected_column = st.selectbox(
    'Select a variable to explore:',
    list(column_to_description.values())
)
selected_variable = [col for col, desc in column_to_description.items() if desc == selected_column][0]
selected_correlation = correlations[selected_variable]

st.write(f"Correlation between 'Life Satisfaction' and {selected_variable}: {selected_correlation:.2f}")

df['strlife'] = df['stflife'].dropna()

fig, ax = plt.subplots()
if selected_variable in variable_mapping:
    group_column = variable_mapping[selected_variable]
    sns.boxplot(x=df[group_column], y=df['stflife'], ax=ax)
else:
    sns.boxplot(x=df[selected_variable], y=df['stflife'], ax=ax)
ax.set_title(f'Life Satisfaction by {selected_column}')
st.pyplot(fig)

if selected_variable in graph_explanations:
    with st.expander("Graph Interpretation"):
        st.markdown(graph_explanations[selected_variable]['explanation'])

# ------------------ Thematic Overview ------------------

st.header("Themes Overview")

theme_data = {
    "Subjective Wellbeing": [
        ("How happy are you", 0.680),
        ("Were happy, how often past week", 0.407),
        ("How much control over life in general nowadays", 0.402),
        ("Enjoyed life, how often past week", 0.392),
    ],
    "Institutional Trust": [
        ("How satisfied with present state of economy in country", 0.356),
        ("How satisfied with the way democracy works in country", 0.302),
        ("Trust in the police", 0.278),
        ("Trust in the legal system", 0.263),
        ("Trust in country's parliament", 0.240),
        ("State of education in country nowadays", 0.237),
        ("How satisfied with the national government", 0.237),
        ("Trust in politicians", 0.223),
        ("Trust in political parties", 0.214),
    ],
    "Social Trust": [
        ("Most people try to take advantage of you, or try to be fair", 0.264),
        ("Most people can be trusted or you can't be too careful", 0.248),
        ("Most of the time people helpful or mostly looking out for themselves", 0.243),
        ("How many people with whom you can discuss intimate and personal matters", 0.215),
        ("How often socially meet with friends, relatives or colleagues", 0.196),
    ],
    "Mental Distress": [
        ("Felt depressed, how often past week", -0.355),
        ("Felt sad, how often past week", -0.346),
        ("Felt lonely, how often past week", -0.327),
        ("Felt everything did as effort, how often past week", -0.307),
        ("Could not get going, how often past week", -0.292),
        ("Sleep was restless, how often past week", -0.200),
    ],
    "Health Limitations": [
        ("Subjective general health", -0.282),
        ("Hampered in daily activities by illness/disability/infirmity/mental problem", 0.202),
        ("State of health services in country nowadays", 0.258),
    ],
    "Economic Status": [
        ("Household's total net income, all sources", 0.220),
        ("Severe financial difficulties in family when growing up, how often", 0.198),
        ("Doing last 7 days: unemployed, actively looking for job", -0.077),
    ],
}


for theme, questions in theme_data.items():
    with st.expander(theme):
        for question, corr in questions:
            st.write(f"- {question}: {corr}")

# ------------------ Heatmap ------------------

st.header("Correlation Heatmap Across Countries")

fig = px.imshow(
    trans_df,
    labels=dict(x="Variables", y="Countries", color="Correlation"),
    aspect="auto",
    color_continuous_scale='RdBu_r'
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title='Correlation Coefficient',
        len=0.75,
        thickness=20,
        x=1.01,
        xanchor="left",
        y=0.5,
        yanchor="middle"
    )
)

st.plotly_chart(fig, use_container_width=True)

# ------------------ Country-Level Exploration ------------------

st.header("Country Specific Analysis")

countries = list(country_correlations.keys())
selected_country = st.selectbox("Select a Country:", countries)
country_corr = country_correlations[selected_country]

country_selected_column = st.selectbox(
    'Select a variable:',
    list(column_to_description.values()),
    key='country_selected_column'
)

country_selected_variable = [col for col, desc in column_to_description.items() if desc == country_selected_column][0]
selected_country_correlation = country_corr[country_selected_variable]

st.write(f"Correlation between 'Life Satisfaction' and {country_selected_variable} in {selected_country}: {selected_country_correlation:.2f}")

fig, ax = plt.subplots()
sns.boxplot(
    x=country_df.loc[country_df['cntry'] == selected_country, country_selected_variable],
    y=country_df.loc[country_df['cntry'] == selected_country, 'stflife'],
    ax=ax
)
ax.set_title(f"Life Satisfaction by {country_selected_column} in {selected_country}")
st.pyplot(fig)

