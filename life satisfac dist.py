import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("qt5Agg")
import matplotlib.pyplot as plt

# Load data (use your path to the dataset)
data = pd.read_csv("data/year_2023_cleaned.csv")

# Plot 2: Histogram with Density Curve
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data["stflife"], bins=11, kde=True, color='royalblue', edgecolor='black', ax=ax)
ax.set_title("Distribution of Life Satisfaction Scores with Density Curve", fontsize=12, weight='bold')
ax.set_xlabel("Life Satisfaction Score", fontsize=12, weight='bold')
ax.set_ylabel("Frequency",fontsize=12, weight='bold')

# Show the plot
plt.show()
