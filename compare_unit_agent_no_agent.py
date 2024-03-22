import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# path1 = '/home/algo/code/alpha/gpt/agent/results/2024-01-07_12-38-48/results.csv'
# path2 = '/home/algo/code/alpha/gpt/agent/results/2024-01-14_09-15-02/results.csv'

path1 = '/home/algo/code/alpha/gpt/agent/results/2024-01-07_12-38-06/results.csv'
path2 = '/home/algo/code/alpha/gpt/agent/results/2024-01-12_13-36-13/results.csv'

# Load the data from both files
df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)

# Columns to visualize
columns = ['t1_unit', 't2_unit', 't3_unit', 't4_unit']

# Function to calculate mean and standard deviation for specified columns
def calculate_stats(df, columns):
    averages = []
    std_deviations = []
    for col in columns:
        averages.append(df[col].mean())
        std_deviations.append(df[col].std())
    return averages, std_deviations

# Calculate stats for both datasets
averages1, std_deviations1 = calculate_stats(df1, columns)
averages2, std_deviations2 = calculate_stats(df2, columns)

# Create a single line plot
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Comparison of Unit Metrics with Std Deviation', fontsize=16)

# X-axis labels
x_labels = ['t1', 't2', 't3', 't4']

# Plot for first dataset
ax.plot(x_labels, averages1, marker='o', linestyle='-', label=f'Without Agent', color='blue')
ax.fill_between(x_labels, np.array(averages1) - np.array(std_deviations1), np.array(averages1) + np.array(std_deviations1), alpha=0.1, color='blue')

# Plot for second dataset
ax.plot(x_labels, averages2, marker='s', linestyle='-', label=f'With Agent', color='green')
ax.fill_between(x_labels, np.array(averages2) - np.array(std_deviations2), np.array(averages2) + np.array(std_deviations2), alpha=0.1, color='green')

ax.set_title('Average Unit Metrics Comparison')
ax.set_ylabel('Average Score')
ax.set_xlabel('Unit')
ax.legend(loc='upper left')
ax.grid(True)

# Show the plot
plt.show()

