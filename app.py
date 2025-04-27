# Final dashboard code is being prepared with polishing edits you asked.
# Due to the size, I'll break it into 2–3 parts for easier pasting.

# Part 1: Setup and Intro

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
# import matplotlib
# matplotlib.use("qt5Agg")
import matplotlib.pyplot as plt
import json
import os


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

causality_variable_descriptions = {
    "stfgov": "How satisfied with the national government",
    "eiscedp": "Partner's highest level of education, ES - ISCED",
    "sclmeet": "How often socially meet with friends, relatives or colleagues",
    "mainact": "Main activity last 7 days",
    "dscrdsb": "Discrimination of respondent's group: disability",
    "uemp5yr": "Any period of unemployment and work seeking within last 5 years",
    "stfedu": "State of education in country nowadays",
    "dscroth": "Discrimination of respondent's group: other grounds",
    "estsz": "Establishment size",
    "ctzcntr": "Citizen of country",
    "happy": "How happy are you",
    "uempla": "Doing last 7 days: unemployed, actively looking for job",
    "jbspv": "Responsible for supervising other employees",
    "emprelp": "Partner's employment relation",
    "eisced": "Highest level of education, ES - ISCED",
    "hswrkp": "Partner doing last 7 days: housework, looking after children, others",
    "hincfel": "Feeling about household's income nowadays",
    "iorgact": "Allowed to influence policy decisions about activities of organisation",
    "bctprd": "Boycotted certain products last 12 months",
    "uemp3m": "Ever unemployed and seeking work for a period more than three months",
    "wrkctra": "Employment contract unlimited or limited duration",
    "dscrrlg": "Discrimination of respondent's group: religion",
    "pplfair": "Most people try to take advantage of you, or try to be fair",
    "mnactp": "Partner's main activity last 7 days",
    "emplrel": "Employment relation",
    "stflife": "How satisfied with life as a whole",
    "wkdcorga": "Allowed to decide how daily work is organised",
    "dscrntn": "Discrimination of respondent's group: nationality",
    "trstplt": "Trust in politicians",
    "stfdem": "How satisfied with the way democracy works in country",
    "occm14b": "Mother's occupation when respondent 14",
    "stfhlth": "State of health services in country nowadays",
    "trstun": "Trust in the United Nations",
    "edctnp": "Partner doing last 7 days: education",
    "freehms": "Gays and lesbians free to live life as they wish",
    "dscrrce": "Discrimination of respondent's group: colour or race",
    "polintr": "How interested in politics",
    "hinctnta": "Household's total net income, all sources",
    "aesfdrk": "Feeling of safety of walking alone in local area after dark",
    "imueclt": "Country's cultural life undermined or enriched by immigrants",
    "imdfetn": "Allow many/few immigrants of different race/ethnic group from majority",
    "imwbcnt": "Immigrants make country worse or better place to live",
    "trstprl": "Trust in country's parliament",
    "edulvlpb": "Partner's highest level of education",
    "rtrdp": "Partner doing last 7 days: retired",
    "rlgdnm": "Religion or denomination belonging to at present",
    "dscrgrp": "Member of a group discriminated against in this country",
    "marsts": "Legal marital status",
    "trstprt": "Trust in political parties",
    "mnactic": "Main activity, last 7 days. All respondents. Post coded",
    "trstep": "Trust in the European Parliament",
    "chldhhe": "Ever had children living in household",
    "dngoth": "Doing last 7 days: other",
    "maritalb": "Legal marital status, post coded",
    "rshpsts": "Relationship with husband/wife/partner currently living with",
    "hswrk": "Doing last 7 days: housework, looking after children, others",
    "emprm14": "Mother's employment status when respondent 14",
    "mbtru": "Member of trade union or similar organisation",
    "domicil": "Domicile, respondent's description",
    "uemp12m": "Any period of unemployment and work seeking lasted 12 months or more",
    "trstlgl": "Trust in the legal system",
    "uemplip": "Partner doing last 7 days: unemployed, not actively looking for job",
    "uempli": "Doing last 7 days: unemployed, not actively looking for job",
    "hincsrca": "Main source of household income",
    "dscretn": "Discrimination of respondent's group: ethnic group",
    "uemplap": "Partner doing last 7 days: unemployed, actively looking for job",
    "nacer2": "Industry, NACE rev.2",
    "stfeco": "How satisfied with present state of economy in country",
    "tporgwk": "What type of organisation work/worked for",
    "occf14b": "Father's occupation when respondent 14",
    "impcntr": "Allow many/few immigrants from poorer countries outside Europe",
    "pplhlp": "Most of the time people helpful or mostly looking out for themselves",
    "trstplc": "Trust in the police",
    "emprf14": "Father's employment status when respondent 14",
    "dngnapp": "Partner doing last 7 days: not applicable",
    "dngothp": "Partner doing last 7 days: other",
    "facntr": "Father born in country",
    "crmvct": "Respondent or household member victim of burglary/assault last 5 years",
    "edctn": "Doing last 7 days: education",
    "wrkac6m": "Paid work in another country, period more than 6 months last 10 years",
    "dscrlng": "Discrimination of respondent's group: language",
    "dsbld": "Doing last 7 days: permanently sick or disabled",
    "edulvlb": "Highest level of education",
    "lrscale": "Placement on left right scale",
    "rtrd": "Doing last 7 days: retired",
    "dsbldp": "Partner doing last 7 days: permanently sick or disabled",
    "health": "Subjective general health",
    "crpdwk": "Control paid work last 7 days",
    "pdwrk": "Doing last 7 days: paid work",
    "imbgeco": "Immigration bad or good for country's economy",
    "lvgptnea": "Ever lived with a partner, without being married",
    "eiscedm": "Mother's highest level of education, ES - ISCED",
    "edulvlmb": "Mother's highest level of education",
    "sclact": "Take part in social activities compared to others of same age",
    "mocntr": "Mother born in country",
    "crpdwkp": "Partner, control paid work last 7 days",
    "dvrcdeva": "Ever been divorced/had civil union dissolved",
    "atncrse": "Improve knowledge/skills: course/lecture/conference, last 12 months",
    "pdwrkp": "Partner doing last 7 days: paid work",
    "clsprty": "Feel closer to a particular party than all other parties",
    "dscrsex": "Discrimination of respondent's group: sexuality",
    "eiscedf": "Father's highest level of education, ES - ISCED",
    "imsmetn": "Allow many/few immigrants of same race/ethnic group as majority",
    "pdjobev": "Ever had a paid job",
    "dscrgnd": "Discrimination of respondent's group: gender",
    "hlthhmp": "Hampered in daily activities by illness/disability/infirmity/mental problem",
    "dscrage": "Discrimination of respondent's group: age",
    "rlgblg": "Belonging to particular religion or denomination",
    "edulvlfb": "Father's highest level of education",
    "dngnap": "Partner doing last 7 days: no answer",
    "cmsrv": "Doing last 7 days: community or military service",
    "rlgdngb": "Religion or denomination belonging to at present, United Kingdom",
    "edlvmdie": "Mother's highest level of education, Ireland",
    "edlvpdie": "Partner's highest level of education, Ireland",
    "dngna": "Doing last 7 days: no answer",
    "edlvmdfi": "Mother's highest level of education, Finland",
    "edlvfdch": "Father's highest level of education, Switzerland",
    "edlvpdfi": "Partner's highest level of education, Finland",
    "rlgdnno": "Religion or denomination belonging to at present, Norway",
    "edlvfdfi": "Father's highest level of education, Finland",
    "edlvfdie": "Father's highest level of education, Ireland",
    "edlvmdch": "Mother's highest level of education, Switzerland",
    "edagegb": "Age when completed full time education, United Kingdom",
    "rlgdnach": "Religion or denomination belonging to at present, Switzerland",
    "edlvpdlt": "Partner's highest level of education, Lithuania",
    "rlgdnie": "Religion or denomination belonging to at present, Ireland",
    "rlgdnlt": "Religion or denomination belonging to at present, Lithuania",
    "dngdkp": "Partner doing last 7 days: don't know",
    "edlvdie": "Highest level of education, Ireland",
    "edlvdlt": "Highest level of education, Lithuania",
    "edlvfdlt": "Father's highest level of education, Lithuania",
    "edlvmdlt": "Mother's highest level of education, Lithuania",
    "edlvpdch": "Partner's highest level of education, Switzerland",
    "edlvdfi": "Highest level of education, Finland",
    "edlvdch": "Highest level of education, Switzerland",
    "njbspv": "Number of people responsible for in job",
    "wkhct": "Total contracted hours per week in main job overtime excluded",
    "wkhtotp": "Hours normally worked a week in main job overtime included, partner",
    "wkhtot": "Total hours normally worked per week in main job overtime included"
}

# ------------------ Variable Mapping ------------------

variable_mapping = {
    'agea': 'age_group',
    'eduyrs': 'education_group',
}


# ------------------ App Starts ------------------

st.title("Understanding Life Satisfaction Across Europe: Insights from the 2023 European Social Survey")
st.subheader("Executive Summary")

st.markdown("""
This dashboard explores key factors influencing life satisfaction across Europe using data from the 2023 European Social Survey (ESS). 

Our analysis reveals several consistent patterns:
- Life satisfaction is highest in Northern and Western Europe, and lower in Southern and Eastern Europe.
- Emotional well-being and mental health indicators show the strongest relationships with life satisfaction, reinforcing the central role of psychological factors in subjective well-being.
- Higher social trust and greater trust in institutions are moderately associated with higher life satisfaction.
- Economic factors, such as household income, and subjective health status, also play important roles but with smaller effect sizes.
- Variables such as education and age show weaker or inconsistent associations with life satisfaction across countries.

Overall, the findings highlight that life satisfaction is a multidimensional outcome shaped by emotional health, trust, economic security, and broader social factors.
""")


st.header("Introduction")

st.markdown("""

The objective is to identify patterns, regional differences, and key correlates of well-being, helping to uncover broader social, economic, and psychological drivers of life satisfaction.

There are two section for this dashboard. The first section is the result of initial exploration of correlation. The second section, is the result of causation analysis.
Using a combination of descriptive statistics, correlation analysis, and visualisation techniques, we investigate relationships between life satisfaction and variables such as **social trust**, **institutional trust**, **mental health**, and **economic status**.

All data used in this analysis is fully anonymised and adheres to ethical research guidelines.
""")

st.subheader("What is Life Satisfaction?")

st.markdown("""
**Life satisfaction** refers to a person’s overall assessment of their quality of life according to their chosen criteria.

It is a key component of subjective well-being and captures a broad evaluation of how individuals feel about their lives as a whole, rather than moment-to-moment emotional states.

In the ESS, life satisfaction is measured on a scale from 0 (extremely dissatisfied) to 10 (extremely satisfied) using the question:

> \"All things considered, how satisfied are you with your life as a whole nowadays?\"
""")

st.subheader("About the Data")

st.markdown("""
Data was sourced from the 2023 European Social Survey (ESS), covering over 20 countries.

Variables include subjective well-being indicators, mental health metrics, institutional trust levels, economic status, and demographic factors.
""")
# ------------------ Distribution of Life Satisfaction Scores ------------------

st.header("Section 1: Life satisfaction and Correlation")
st.header("Distribution of Life Satisfaction Scores")

st.markdown("""
Before exploring regional and individual differences, it is important to understand the overall distribution of life satisfaction scores in the dataset.
""")

# Plot 1: Simple Histogram
st.subheader("Histogram of Life Satisfaction Scores")
fig, ax = plt.subplots(figsize=(8, 5))
data["stflife"].hist(bins=11, edgecolor='black', ax=ax)
ax.set_title("Distribution of Life Satisfaction (0–10)")
ax.set_xlabel("Life Satisfaction Score")
ax.set_ylabel("Frequency")
st.pyplot(fig)

st.markdown("""
The histogram shows that life satisfaction scores are not evenly distributed.  
Most individuals report scores between **6 and 8**, indicating a positive skew toward higher satisfaction levels.
""")

# Plot 2: Histogram + Smoothed Density
st.subheader("Histogram with Density Curve")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data["stflife"], bins=11, kde=True, color='royalblue', edgecolor='black', ax=ax)
ax.set_title("Distribution of Life Satisfaction Scores with Density Curve")
ax.set_xlabel("Life Satisfaction Score")
ax.set_ylabel("Frequency")
st.pyplot(fig)

st.markdown("""
Overlaying a smoothed density curve (Kernel Density Estimation) helps visualise the pattern more clearly.  
The right-skewed distribution with a peak around **7–8** aligns with general well-being trends observed in Europe.
""")

# ------------------ General Overview by Country ------------------

st.header("Life Satisfaction Across Countries")

st.markdown("""
We now explore how life satisfaction scores vary across different European countries, helping to reveal broader patterns.
""")

country_life_sat = data.groupby('cntry')['stflife'].mean().sort_values()

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(country_life_sat.index, country_life_sat.values, color='royalblue')
ax.set_xlabel('Average Life Satisfaction')
ax.set_ylabel('Country')
ax.set_title('Life Satisfaction Across Countries')
ax.invert_yaxis()
st.pyplot(fig)

st.subheader("Interpretation")

st.markdown("""
- Switzerland, Finland, Netherlands, and Sweden report the **highest** average life satisfaction.
- Slovakia, Cyprus, Greece, and Portugal report the **lowest** average scores.
- Most countries cluster between **6 and 8**, suggesting generally high satisfaction levels across Europe.
- The slightly right-skewed distribution suggests more countries with higher life satisfaction than lower.

These patterns hint at deeper **economic**, **social**, and **institutional** differences between regions.
""")


# ------------------ Regional Analysis ------------------

st.header("Life Satisfaction by Region")

regions = {
    'Northern Europe': ['DK', 'EE', 'FI', 'IS', 'LT', 'LV', 'NO', 'SE'],
    'Western Europe': ['AT', 'BE', 'CH', 'DE', 'FR', 'GB', 'IE', 'LU', 'NL'],
    'Eastern Europe': ['BG', 'CZ', 'HR', 'HU', 'PL', 'RO', 'RS', 'RU', 'SI', 'SK', 'UA'],
    'Southern Europe': ['AL', 'CY', 'ES', 'GR', 'IT', 'ME', 'MK', 'PT', 'TR', 'XK']
}

# Map country codes to region names
country_to_region = {country: region for region, countries in regions.items() for country in countries}
data['region'] = data['cntry'].map(country_to_region)

# Group by region and plot
region_life_sat = data.groupby('region')['stflife'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(region_life_sat.index, region_life_sat.values, color=['royalblue', 'darkorange', 'seagreen', 'crimson'])
ax.set_xlabel('Average Life Satisfaction')
ax.set_ylabel('Region')
ax.set_title('Life Satisfaction Across European Regions')
st.pyplot(fig)

st.subheader("Interpretation")

st.markdown("""
- **Northern Europe** reports the highest life satisfaction, followed by **Western Europe**.
- **Southern** and **Eastern Europe** report the lowest average scores.
- This mirrors patterns in wealth, social support systems, and institutional trust found in the literature.
""")

st.markdown("""
Higher life satisfaction in Northern and Western Europe aligns with previous research findings:  
these regions tend to have **stronger welfare states**, **better healthcare systems**, and **higher levels of social trust**.
""")

# ------------------ Statistical Testing ------------------

st.header("Statistical Test Results: Differences Across Regions")

st.markdown("""
Formal statistical tests were conducted to assess whether the observed differences between regions are statistically significant.
""")

# ANOVA
anova_result = pd.DataFrame({
    "Statistic": ["F-statistic"],
    "Value": [508.728]
})

st.subheader("ANOVA Test Result")
st.table(anova_result)

st.markdown("""
The **ANOVA test** shows that differences between regions are **highly significant** (F = 508.728, p < 0.001).
""")

# Tukey HSD Test
tukey_data = {
    "Group 1": ["Eastern Europe", "Eastern Europe", "Eastern Europe",
                "Northern Europe", "Northern Europe", "Southern Europe"],
    "Group 2": ["Northern Europe", "Southern Europe", "Western Europe",
                "Southern Europe", "Western Europe", "Western Europe"],
    "Mean Difference": [0.7527, -0.2242, 0.5882, -0.9769, -0.1646, 0.8123],
    "p-value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Lower Bound": [0.67, -0.2982, 0.5211, -1.0594, -0.2408, 0.7456],
    "Upper Bound": [0.8355, -0.1501, 0.6552, -0.8944, -0.0883, 0.8791],
    "Significant?": ["Yes", "Yes", "Yes", "Yes", "Yes", "Yes"]
}

tukey_df = pd.DataFrame(tukey_data)

st.subheader("Tukey HSD Test Results")
st.dataframe(tukey_df.style.format({
    "Mean Difference": "{:.3f}",
    "p-value": "{:.3f}",
    "Lower Bound": "{:.3f}",
    "Upper Bound": "{:.3f}"
}))

st.subheader("Interpretation of Results")

st.markdown("""
- **Northern Europe** has significantly higher life satisfaction than all other regions.
- **Western Europe** also scores significantly higher than Eastern and Southern Europe.
- **Southern Europe** reports the **lowest life satisfaction**, even lower than Eastern Europe.
- All pairwise regional differences are statistically significant (**p < 0.001**).
""")


# ------------------ Exploring Individual Factors ------------------

st.header("Exploring Individual-Level Factors")

st.markdown("""
We now explore how **individual characteristics and experiences** relate to life satisfaction.

Select a variable to view its relationship with life satisfaction.
""")

# Dropdown
selected_column = st.selectbox(
    'Select a variable to explore:',
    list(column_to_description.values())
)

selected_variable = [col for col, desc in column_to_description.items() if desc == selected_column][0]

# Correlation Value
selected_correlation = correlations.get(selected_variable, None)
if selected_correlation is not None:
    st.write(f"Correlation between Life Satisfaction and **{selected_column}**: {selected_correlation:.2f}")
else:
    st.write(f"No correlation value available for **{selected_column}**.")

# Disclaimer
st.info("""
Not every variable has a written interpretation.  
Please rely on the graph to interpret relationships where no explanation is available.
""")

# Small guide for interpreting boxplots
with st.expander("How to Interpret the Boxplot"):
    st.markdown("""
- **Boxplots** show the distribution of life satisfaction scores across different groups.
- **The middle line** inside the box = the **median** life satisfaction score.
- **The height of the box** shows variability — taller boxes mean greater variability.
- **Whiskers** extend to typical scores; **dots** represent outliers.
- A higher box means generally higher life satisfaction.
""")

# Boxplot
df['strlife'] = df['stflife'].dropna()

fig, ax = plt.subplots(figsize=(10, 6))
if selected_variable in variable_mapping:
    group_column = variable_mapping[selected_variable]
    sns.boxplot(x=df[group_column], y=df['stflife'], ax=ax)
else:
    sns.boxplot(x=df[selected_variable], y=df['stflife'], ax=ax)

ax.set_title(f'Life Satisfaction by {selected_column}')
ax.set_xlabel(selected_column)
ax.set_ylabel('Life Satisfaction')
st.pyplot(fig)

# Optional Graph Interpretation
if selected_variable in graph_explanations:
    with st.expander("Graph Interpretation"):
        st.markdown(graph_explanations[selected_variable]['explanation'])
else:
    st.info("No specific graph interpretation available for this variable.")


# ------------------ Grouped Themes ------------------

st.header("Thematic Overview of Key Factors")

st.markdown("""
Factors have been grouped into **six main themes** based on their content and measured correlations with life satisfaction.
""")

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

# Show expandable theme areas
for theme, questions in theme_data.items():
    with st.expander(theme):
        for question, corr in questions:
            st.write(f"- **{question}**: {corr:.3f}")

# Interpretation of Themes
st.subheader("Key Patterns Observed")

st.markdown("""
- **Subjective Wellbeing** factors have the strongest positive relationships with life satisfaction (happiness, control, enjoyment).
- **Institutional Trust** and **Social Trust** are moderately positively correlated.
- **Mental Distress** variables are negatively correlated — higher distress predicts lower life satisfaction.
- **Economic Status** and **Health Limitations** also matter, though slightly less strongly.

These findings are consistent with existing research which shows emotional, financial, and social resources are important to subjective well-being.
""")

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

st.markdown("""
**Key Findings from the Heatmap:**

- Across most European countries, higher household income (`hinctnta`) is positively associated with higher life satisfaction, in line with existing research linking financial security to subjective well-being.
- Higher social trust (`ppltrst`) also shows moderate positive correlations with life satisfaction across many countries, supporting theories that strong social capital enhances quality of life.
- Health problems (`health`) show strong negative correlations almost everywhere, confirming previous findings that physical health is a major predictor of subjective well-being.

**Variation Across Countries:**

- Education (`eduyrs`) shows weaker and more inconsistent correlations with life satisfaction, suggesting that while education may confer economic advantages, it does not universally translate to higher subjective well-being.
- Unemployment (`uempla`) is negatively correlated with life satisfaction, but the strength of this relationship varies by country, potentially reflecting differences in social welfare systems across Europe.

**Other Observations:**

- Trust in institutions such as the police (`trstplc`) and national parliament (`trstprl`) tends to correlate positively with life satisfaction, particularly in Northern and Western Europe — regions generally characterised by higher institutional trust and stronger welfare systems.
- Age (`agea`) shows very weak or near-zero correlations overall; however, prior literature suggests a non-linear U-shaped relationship between age and life satisfaction, which a simple correlation may not fully capture.
- Variables reflecting feelings of belonging or personal responsibility (`ipadvnta`, `iprspota`) are generally weakly correlated, indicating these factors might influence life satisfaction more indirectly or in interaction with other variables.

Overall, the heatmap reveals general European patterns (GEA) where income, health, and social trust consistently emerge as key correlates of life satisfaction, while other factors such as education, unemployment, and institutional trust exhibit more regional variation.
""")


# ------------------ Country-Level Exploration ------------------

# ------------------ Country-Level Exploration ------------------

st.header("Country-Specific Analysis")

st.markdown("""
You can explore how different factors correlate with life satisfaction in specific countries.
Select a country and a variable from the dropdowns below to view the correlation and distribution.

Please note: correlations can vary considerably between countries, and not every pattern will be strong or linear.
""")

# Country selection
countries = list(country_correlations.keys())
selected_country = st.selectbox("Select a Country:", countries)

country_corr = country_correlations[selected_country]

# Variable selection
country_selected_column = st.selectbox(
    'Select a variable:',
    list(column_to_description.values()),
    key='country_selected_column'
)

# Get internal variable name
country_selected_variable = [col for col, desc in column_to_description.items() if desc == country_selected_column][0]
selected_country_correlation = country_corr.get(country_selected_variable, None)

# Display correlation
if selected_country_correlation is not None:
    st.write(f"Correlation between Life Satisfaction and **{country_selected_column}** in {selected_country}: {selected_country_correlation:.2f}")
else:
    st.write(f"No correlation data available for **{country_selected_column}** in {selected_country}.")

st.info("""
Please note: No variables have written interpretation at the country level.  
""")

# Boxplot for country-specific variable
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(
    x=country_df.loc[country_df['cntry'] == selected_country, country_selected_variable],
    y=country_df.loc[country_df['cntry'] == selected_country, 'stflife'],
    ax=ax
)
ax.set_title(f"Life Satisfaction by {country_selected_column} in {selected_country}")
ax.set_xlabel(country_selected_column)
ax.set_ylabel('Life Satisfaction Score')
st.pyplot(fig)

# Add small interpretation guidance
with st.expander("How to Interpret the Boxplot"):
    st.markdown("""
- Each **box** shows the distribution of life satisfaction scores for different groups or values.
- The **middle line** is the **median** life satisfaction score.
- The **height of the box** represents the spread (variability) within each group.
- **Whiskers** extend to typical ranges, and **dots** are outliers.
  
If the box for a group is positioned higher, it suggests a higher average life satisfaction score.

Caution: With some variables or in smaller countries, patterns might be weak or noisy.
""")


# ------------------ Conclusion ------------------

st.header("Conclusion for correlation exploration")

st.markdown("""
This dashboard has explored variations in life satisfaction across Europe, using regional, demographic, and individual-level factors.

Our findings align with several key insights from existing research:

- **Regional differences**: Life satisfaction is higher in Northern and Western Europe, consistent with research linking stronger social policies, better institutional trust, and economic stability to greater well-being.
- **Subjective well-being** indicators, such as happiness and perceived control, show the strongest positive correlations with life satisfaction. This supports the view that psychological factors are central to overall well-being.
- **Mental distress** factors, such as depression and loneliness, are strongly negatively associated with life satisfaction, consistent with research emphasising the importance of emotional health.
- **Social trust** and **institutional trust** are moderately associated with higher life satisfaction, echoing findings that good community ties and trust in public institutions enhance well-being.
- **Economic factors**, including income and employment, are positively associated with life satisfaction, although with smaller effect sizes, consistent with the Easterlin Paradox which suggests that income boosts happiness only to a point.
- **Health status** and perceptions of public services, such as education and healthcare quality, are also relevant, aligning with literature highlighting the role of health and social services in promoting well-being.

Overall, our findings reinforce the idea that well-being should be understood as a unified construct, encompassing emotional, social, institutional, and economic dimensions.

Future research could further investigate differences across gender, demographics, and environmental quality, as highlighted in previous studies.

""")


#_____________________plot the casuality weigth value----------------------

st.markdown("""
# Advanced Causal Analysis: Key Drivers of Life Satisfaction

While earlier sections focused on descriptive and correlational insights, this section goes further by applying **advanced causal analysis** across multiple countries.

Using Granger causality testing, we identify variables that not only correlate with life satisfaction but also **predict changes over time**.  
The causal weights shown below represent how strongly each variable influences life satisfaction in a predictive sense.
""")

st.markdown("""
---
🔎 **Disclaimer: Exploratory Nature of This Section**

This section is intended for light exploration rather than deep causal explanation.  
It helps you visually browse which factors appear to have the strongest causal relationship with your selected outcome.

- If you already have a hypothesis (e.g., "I think income affects life satisfaction"), this section can help confirm or challenge your intuition.
- If you're curious, it can help spot unexpected patterns worth deeper investigation later.

For example, in the chart above, when exploring **Feeling of safety when walking alone at night** (`aesfdrk`), we see that:
- Living situation (whether someone has ever lived with a partner) and
- Trust in national government
are among the top 10 factors influencing how safe people feel.  
This suggests that both personal and institutional support structures may play an important role in people's sense of safety.
---
""")



st.header("Causality Results(weights) Across Europe")
# Step 1: Load Causal Data
try:
    df = pd.read_csv("data/causality_global_map.csv")
    st.success("Begin your exploration!")

    if df.shape[1] < 3:
        st.error("Oops! The file seems incomplete. It must have at least 3 columns: causality_from, causality_to, and weight.")
    else:
        causality_from_col = df.columns[0]
        causality_to_col = df.columns[1]
        weight_col = df.columns[2]

        # Create display labels
        available_targets = sorted(df[causality_to_col].unique())
        target_options = [
            f"{causality_variable_descriptions.get(code, code)} ({code})"
            for code in available_targets
        ]

        selected_option = st.selectbox(
            "Select the outcome you want to explore (description shown):",
            target_options
        )

        # Extract true variable name
        target_variable = selected_option.split('(')[-1].replace(')', '')

        # Filter based on target
        df_filtered = df[df[causality_to_col] == target_variable].sort_values(weight_col, ascending=False)

        # Select how many to display
        percentage = st.slider(
            "Select the percentage of top causal variables to display:",
            min_value=1,
            max_value=20,
            value=10
        )

        top_n = int(len(df_filtered) * (percentage / 100))
        df_top = df_filtered.head(top_n)

        st.write(f"Displaying the top {top_n} variables ({percentage}% of total) causally influencing **{target_variable}**.")

        # --- Plot ---
        st.subheader("Top Causal Drivers")

        # Map readable names to y-axis
        df_top[causality_from_col] = df_top[causality_from_col].apply(
            lambda code: causality_variable_descriptions.get(code, code)
        )

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(
            x=df_top[weight_col],
            y=df_top[causality_from_col],
            palette="coolwarm",
            ax=ax
        )
        ax.set_xlabel("Causal Weight", fontsize=12)
        ax.set_ylabel("Predictor Variable", fontsize=12)
        ax.set_title(f"Top Causal Drivers of {causality_variable_descriptions.get(target_variable, target_variable)}", fontsize=14, fontweight='bold')

        st.pyplot(fig)

except FileNotFoundError:
    st.error("⚠️ Error: Could not find the file 'causality_global_map.csv'. Please check if it's placed correctly inside the data folder.")

# Small professional note at the end:
st.markdown("""
---
**Note:**  
The causal weight reflects the strength of each variable’s predictive impact on the selected outcome.  
Higher weights indicate stronger and more consistent causal effects across countries.
""")
#----------------------Causality weights cross country----------

st.header("Granger Causality Across Countries")

# Set correct data folder
data_folder = "data/causality"

# Load all CSVs
all_data = []
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        country_code = filename.split("_")[0]
        df = pd.read_csv(os.path.join(data_folder, filename))
        df['Country'] = country_code
        all_data.append(df)

# Combine all into one dataframe
full_df = pd.concat(all_data, ignore_index=True)

# Load global causality map
granger_causality_map = pd.read_csv("data/causality_global_map.csv")

# Mapping target → factors
granger_target_options = granger_causality_map['causality_to'].dropna().unique()
available_factors_for_target = {}
for target in granger_target_options:
    available_factors_for_target[target] = granger_causality_map[
        granger_causality_map['causality_to'] == target]['causality_from'].tolist()

# Sidebar selection
st.subheader("Causality Selection")

# Create description-labeled options
target_options = sorted(full_df['causality_to'].dropna().unique())
target_labels = {code: causality_variable_descriptions.get(code, code) for code in target_options}
target_display = [f"{target_labels[code]} ({code})" for code in target_options]

# Target dropdown
selected_target_display = st.selectbox(
    "Select the Target Variable (outcome):",
    [""] + target_display
)

# Extract back the code
selected_target = selected_target_display.split("(")[-1].replace(")", "") if selected_target_display else ""

# Filter factor options
if selected_target:
    factor_options = available_factors_for_target.get(selected_target, [])
else:
    factor_options = []

factor_labels = {code: causality_variable_descriptions.get(code, code) for code in factor_options}
factor_display = [f"{factor_labels[code]} ({code})" for code in factor_options]

# Factor dropdown
selected_factor_display = st.selectbox(
    "Select the Factor Variable (cause):",
    [""] + factor_display
)

# Extract back code
selected_factor = selected_factor_display.split("(")[-1].replace(")", "") if selected_factor_display else ""

# Proceed if selections made
if selected_target and selected_factor:
    filtered_df = full_df[
        (full_df['causality_to'] == selected_target) &
        (full_df['causality_from'] == selected_factor)
    ]

    filtered_df = filtered_df[filtered_df['p_value'] <= 0.05]
    
    all_countries = full_df['Country'].unique()
    country_weights = {country: 0 for country in all_countries}
    
    for index, row in filtered_df.iterrows():
        country_weights[row['Country']] = row['p_value']
    
    plot_data = pd.DataFrame(list(country_weights.items()), columns=['Country', 'p_value'])

    if plot_data.empty:
        st.warning("No countries found with a significant causal relationship (p ≤ 0.05).")
    else:
        st.success(f"Plotting Granger causality results for **{selected_factor} → {selected_target}** across countries.")
        
        st.subheader("Granger Causality p-values Across Countries")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(
            x="Country",
            y="p_value",
            data=plot_data,
            palette="mako",
            ax=ax
        )
        ax.set_xlabel("Country", fontsize=12)
        ax.set_ylabel("Granger Causality p-value", fontsize=12)
        ax.set_title(f"{factor_labels[selected_factor]} → {target_labels[selected_target]}", fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        st.pyplot(fig)

else:
    st.info("Please select both a Target and a Factor to generate the plot.")

st.markdown("""
**Interpretation Tip:**  
- A country with **no bar** means the causal relationship was *not significant* (p > 0.05).  
- A **lower p-value** means a **stronger** causal relationship.  
- Analysing these results helps identify **which factors are most influential in different countries**.
""")