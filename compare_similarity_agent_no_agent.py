import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# # Paths to the CSV files
# path1 = '/home/algo/code/alpha/gpt/agent/results/2024-01-07_12-38-06/results.csv'
# path2 = '/home/algo/code/alpha/gpt/agent/results/2024-01-12_13-36-13/results.csv'

#CoT results
#gpt-3.5 cot
path1 = '/home/algo/code/alpha/gpt/agent/results/2024-03-14_11-21-13/results.csv'

#gpt-4 cot
#path1 = '/home/algo/code/alpha/gpt/agent/results/2024-03-14_11-19-05/results.csv'

#ours
path2 = '/home/algo/code/alpha/gpt/results/2024-01-07_12-29-37/results.csv'

#turbo
#path2 = '/home/algo/code/alpha/gpt/results/2024-01-07_12-30-43/results.csv'


#gemini
#path2 = '/home/algo/code/alpha/gpt/results/2024-01-07_12-31-00/results.csv'


# Load the data from both files
df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)

# List of metrics
metrics = ['gleu_score', 'chrf_score', 'nist_score', 'codeBleu_score', 'meteor_score', 'bleu_score']

# Function to calculate mean and standard deviation
def calculate_stats(df):
    averages = []
    std_deviations = []
    for metric in metrics:
        entries_data = df.filter(like=metric)
        entry_averages = entries_data.mean(axis=0)
        entry_std = entries_data.std(axis=0)
        averages.append(entry_averages)
        std_deviations.append(entry_std)
    return averages, std_deviations

# Calculate stats for both datasets
averages1, std_deviations1 = calculate_stats(df1)
averages2, std_deviations2 = calculate_stats(df2)

# Entry labels (assuming they are the same for both datasets)
entry_labels = ['AB', 't1B', 't2B', 't3B', 't4B']

# Create line plots for each metric
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Comparison of Average Metric Scores with Std Deviation', fontsize=16)

for i, metric in enumerate(metrics):
    ax = axes[i // 3, i % 3]
    x = entry_labels

    ax.plot(x, averages1[i], marker='o', linestyle='-', label=r'gpt-3.5 + $\mathbf{CoT}$', color='blue')
    ax.fill_between(x, averages1[i] - std_deviations1[i], averages1[i] + std_deviations1[i], alpha=0.1, color='blue')

    # Plot for second dataset
    ax.plot(x, averages2[i], marker='s', linestyle='-', label=r'gpt-3.5 + $\mathbf{agent}$', color='green')
    ax.fill_between(x, averages2[i] - std_deviations2[i], averages2[i] + std_deviations2[i], alpha=0.1, color='green')

    # Plot for first dataset
    #r'$\mathbf{Bold\ Line\ Label}$'

    ax.set_title(f'Average {metric}')
    ax.set_ylabel('Average Score')
    ax.legend(loc='upper left')
    ax.grid(True)

# Adjust layout and spacing
#plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()
