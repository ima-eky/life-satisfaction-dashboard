
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv("../data/year_2023_cleaned.csv")
    return df


df = load_data()
# st.write(df.head())
country_df = pd.read_csv("country_data.csv")
data = country_df.copy()
trans_df = pd.read_csv("trans_correlation_results.csv", index_col="Country")

with open('correlation_results.json', 'r') as f:
    correlations = json.load(f)

with open('column_descriptions.json', 'r') as f:
    column_to_description = json.load(f)

with open('explanation.json', 'r') as f:
    graph_explanations = json.load(f)

with open('country_correlation_results.json', 'r') as f:
    country_correlations = json.load(f)
## Dashboard
st.markdown("""
The European Social Survey (ESS) is a biennial survey that collects data on a variety of social, political, and economic issues across different European countries. The survey includes questions on topics like:

- Political participation
- Social trust
- Demographics (age, gender, education)
- Health and well-being
- Social inequalities
- Work, family, and personal life

This dashboard is designed to .......
""")
# List of variables to correlate
variables = df.columns.tolist()
variable_mapping = {
    'agea': 'age_group',
    'eduyrs': 'education_group',
}

st.markdown("Starting with life satisfaction as well-being indicator")

country_life_sat = data.groupby('cntry')['stflife'].mean()
country_life_sat_sorted = country_life_sat.sort_values()

# Create the Matplotlib plot
plt.figure(figsize=(12, 6))
plt.barh(country_life_sat_sorted.index, country_life_sat_sorted, color='royalblue')
plt.xlabel('Average Life Satisfaction')
plt.ylabel('Country')
plt.title('Life Satisfaction Across Countries')
plt.gca().invert_yaxis()
st.pyplot(plt)

st.write("seems to be skewed to the right, with most countries having a life satisfaction score between 6 and 8.")


plt.figure(figsize=(8, 5))
sns.histplot(data['stflife'], bins=10, kde=True, color='royalblue')
plt.xlabel('Life Satisfaction Score')
plt.ylabel('Frequency')
plt.title('Distribution of Life Satisfaction Scores')
st.pyplot(plt)


plt.figure(figsize=(8, 5))
data["stflife"].hist(bins=11, edgecolor='black')
plt.title("Distribution of Life Satisfaction (0–10)")
plt.xlabel("Life Satisfaction")
plt.ylabel("Frequency")
st.pyplot(plt)
st.write("it means if we can identify what causes/ is associated with low life satisfaction, then")
          


northern_europe = ['DK', 'EE', 'FI', 'IS', 'LT', 'LV', 'NO', 'SE']
western_europe = ['AT', 'BE', 'CH', 'DE', 'FR', 'GB', 'IE', 'LU', 'NL']
eastern_europe = ['BG', 'CZ', 'HR', 'HU', 'PL', 'RO', 'RS', 'RU', 'SI', 'SK', 'UA']
southern_europe = ['AL', 'CY', 'ES', 'GR', 'IT', 'ME', 'MK', 'PT', 'TR', 'XK']

# Create a dictionary mapping country codes to regions
country_to_region = {}

for country in northern_europe:
    country_to_region[country] = 'Northern Europe'
for country in western_europe:
    country_to_region[country] = 'Western Europe'
for country in eastern_europe:
    country_to_region[country] = 'Eastern Europe'
for country in southern_europe:
    country_to_region[country] = 'Southern Europe'

# Map regions to the dataset
data['region'] = data['cntry'].map(country_to_region)
region_life_sat = data.groupby('region')['stflife'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
plt.barh(region_life_sat.index, region_life_sat, color=['royalblue', 'darkorange', 'seagreen', 'crimson'])

plt.xlabel('Average Life Satisfaction')
plt.ylabel('Region')
plt.title('Life Satisfaction Across European Regions')

# Display the plot
st.pyplot(plt)

import streamlit as st
import pandas as pd

# Define ANOVA results
anova_result = pd.DataFrame({
    "Statistic": ["F-statistic"],
    "Value": [508.728]
})

# Define Tukey HSD results
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

# Streamlit Display
st.title("ANOVA & Tukey HSD Test Results")

# Show ANOVA result
st.subheader("ANOVA Test Result")
st.table(anova_result)

# Show Tukey HSD result
st.subheader("Tukey HSD Test - Multiple Comparisons")
st.dataframe(tukey_df)


selected_column = st.selectbox(
    'Select a variable to correlate with life satisfaction(sorted by correlation to life satisfaction (high - low)):',
    list(column_to_description.values())  # Using descriptions here
)

selected_variable = [col for col, desc in column_to_description.items() if desc == selected_column][0]

# Get the correlation value for the selected variable
selected_correlation = correlations[selected_variable]

# Display the correlation value
st.write(f"Correlation between 'Life Satisfaction' and {selected_variable}: {selected_correlation:.2f}")



# Your data, now named theme_data
theme_data = {
    "subjective_wellbeing": [
        ("How happy are you", 0.680),
        ("Were happy, how often past week", 0.407),
        ("How much control over life in general nowadays", 0.402),
        ("Enjoyed life, how often past week", 0.392),
    ],
    "institutional_trust": [
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
    "social_trust": [
        ("Most people try to take advantage of you, or try to be fair", 0.264),
        ("Most people can be trusted or you can't be too careful", 0.248),
        ("Most of the time people helpful or mostly looking out for themselves", 0.243),
        ("How many people with whom you can discuss intimate and personal matters", 0.215),
        ("How often socially meet with friends, relatives or colleagues", 0.196),
    ],
    "mental_distress": [
        ("Felt depressed, how often past week", -0.355),
        ("Felt sad, how often past week", -0.346),
        ("Felt lonely, how often past week", -0.327),
        ("Felt everything did as effort, how often past week", -0.307),
        ("Could not get going, how often past week", -0.292),
        ("Sleep was restless, how often past week", -0.200),
    ],
    "health_limitations": [
        ("Subjective general health", -0.282),
        ("Hampered in daily activities by illness/disability/infirmity/mental problem", 0.202),
        ("State of health services in country nowadays", 0.258),
    ],
    "economic_status": [
        ("Household's total net income, all sources", 0.220),
        ("Severe financial difficulties in family when growing up, how often", 0.198),
        ("Doing last 7 days: unemployed, actively looking for job", -0.077),
    ],
}

# Streamlit app
st.title("Themes")

# Display themes as expanders
for theme in theme_data:
    with st.expander(theme.replace("_", " ").title()):  # Create expander for each theme
        for question, correlation in theme_data[theme]:
            st.write(f"- {question}: {correlation}")  # Display question and correlation inside expander


with st.expander("What Does the Graph Show...?"):
    st.markdown("""
    **X-axis (Horizontal):** Variable in question
                
    **Y-axis (Vertical):** Life Satisfaction. This shows how satisfied people are with their lives, measured on a scale from 0 to 10.
    
    **The Boxes (Box Plots):** Each box represents the distribution of life satisfaction scores for a specific variable. Here's what the parts of the box tell us:
    - **The line inside the box:** This is the median (the middle value). It tells us the typical life satisfaction score for that variable level.
    - **The box itself:** This shows the middle 50% of the data. A taller box means the life satisfaction scores are more spread out for that variable.
    - **The lines (whiskers) extending from the box:** These show the range of typical scores, excluding outliers (those dots you see).
    - **The dots (outliers):** These are individual data points that are unusually far from the rest of the data.
    """)

# Plot boxplot for the selected variable
df['strlife'] = df['stflife'].dropna()
fig, ax = plt.subplots()
if selected_variable in variable_mapping:
    group_column = variable_mapping[selected_variable]
    sns.boxplot(x=df[group_column], y=df['stflife'])
else:
    sns.boxplot(x=df[selected_variable], y=df['stflife'])
ax.set_title(f'Box plot for {selected_variable}')
st.pyplot(fig)
st.write(f"Box plot showing the distribution of life satisfaction scores for different levels of {selected_variable}.")
if selected_variable in graph_explanations:
    graph_explanation = graph_explanations[selected_variable]['explanation']
    title = graph_explanations[selected_variable].get('title', 'No title available.')
    # graph_title = graph_explanation[selected_variable]['title']
    # st.markdown(f"### Explanation for {graph_title}")
    st.expander("Graph Interpretation").markdown(graph_explanation)
else:
    st.markdown("No explanation available for this variable.")



# Assuming 'trans_df' is your DataFrame
fig = px.imshow(
    trans_df,
    labels=dict(x="Variables", y="Countries", color="Correlation"),
    x=trans_df.columns,
    y=trans_df.index,
    aspect="auto",  # This ensures that the aspect ratio adjusts to data dimensions
    color_continuous_scale='RdBu_r'
)

# fig.update_layout(
#     autosize=False,
#     width=800,  # Adjust width as necessary
#     height=600,  # Adjust height as necessary
#     title='Correlation of Various Factors with Life Satisfaction Across Countries',
#     xaxis_title='Variables',
#     yaxis_title='Countries'
# )

# Adjust the color bar position and size
fig.update_layout(
    coloraxis_colorbar=dict(
        title='Correlation Coefficient',
        len=0.75,  # Adjust the length of the color bar
        thickness=20,  # Adjust the thickness of the color bar
        x=1.01,  # Position the color bar outside the main plot
        xanchor="left",
        y=0.5,  # Center the color bar in the middle of the plot vertically
        yanchor="middle"
    )
)

# Display the figure
# fig.show()


# Use Streamlit to display the figure
st.title('Interactive Heatmap of Life Satisfaction Correlations')
st.plotly_chart(fig, use_container_width=True)
st.write(trans_df.head())

st.header("Correlations by Country")
##Low risk
low_sat = df[df['stflife'] <= 3]
low_sat_gender = low_sat['gndr'].value_counts(normalize=True) * 100
low_sat_age = low_sat['age_group'].value_counts(normalize=True) * 100
low_sat_edu = low_sat['education_group'].value_counts(normalize=True) * 100
low_sat_income = low_sat['hinctnta'].value_counts(normalize=True) * 100
low_sat_unemp = low_sat['uempli'].value_counts(normalize=True) * 100

plt.figure(figsize=(6, 4))
sns.barplot(x=low_sat_edu.index, y=low_sat_edu.values, palette='coolwarm')
plt.xlabel("Unemployment Status")
plt.ylabel("Percentage with Low Life Satisfaction")
plt.title("Distribution of Low Life Satisfaction")
st.pyplot(plt)

plt.figure(figsize=(6, 4))
sns.barplot(x=low_sat_income.index, y=low_sat_income.values, palette='coolwarm')
plt.xlabel("Income Group")
plt.ylabel("Percentage with Low Life Satisfaction")
plt.title("Distribution of Low Life Satisfaction")
st.pyplot(plt)

plt.figure(figsize=(6, 4))
sns.barplot(x=low_sat_gender.index, y=low_sat_gender.values, palette='coolwarm')
plt.xlabel("Gender")
plt.ylabel("Percentage with Low Life Satisfaction")
plt.title("Distribution of Low Life Satisfaction")
st.pyplot(plt)

plt.figure(figsize=(6, 4))
sns.barplot(x=low_sat_age.index, y=low_sat_age.values, palette='coolwarm')
plt.xlabel("Age Group")
plt.ylabel("Percentage with Low Life Satisfaction")
plt.title("Distribution of Low Life Satisfaction by Age Group")

# Display the plot
st.pyplot(plt)


# Get list of countries
countries = list(country_correlations.keys())
selected_country = st.selectbox("Select a Country:", countries)
country_corr = country_correlations[selected_country]

country_selected_column = st.selectbox(
    'Select a variable to correlate with life satisfaction (high - low):',
    list(column_to_description.values()),
    key='country_selected_column'
)

country_selected_variable = [col for col, desc in column_to_description.items() if desc == country_selected_column][0]
selected_country_correlation = country_corr[country_selected_variable]

st.write(f"Correlation between 'Life Satisfaction' and {country_selected_variable}: {selected_country_correlation:.2f}")

fig, ax = plt.subplots()
sns.boxplot(x=country_df.loc[country_df['cntry'] == selected_country, country_selected_variable], y=country_df.loc[country_df['cntry'] == selected_country, 'stflife'], ax=ax)
ax.set_title(f"Boxplot for {selected_country}")
st.pyplot(fig)

