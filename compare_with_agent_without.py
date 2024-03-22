import pandas as pd
import os

result_path = '/home/algo/code/alpha/gpt/agent/results'
file_paths = [ '2024-01-12_13-36-13/results.csv', '2024-01-12_14-10-43/results.csv', '2024-01-14_09-15-02/results.csv']
names = ['gpt-3.5 with agent', 'gpt-4 with agent', 'gpt-4-turbo with agent']

file_paths.append('2024-01-07_12-38-06/results.csv')
names.append('gpt-3.5')

file_paths.append('2024-01-07_12-38-28/results.csv')
names.append('gpt-4')

file_paths.append('2024-01-07_12-38-48/results.csv')
names.append('gpt-4-turbo')

file_paths.append('2024-01-07_12-39-12/results.csv')
names.append('Bard')

file_paths.append('2024-01-19_13-51-45/results.csv')
names.append('Bard with agent')

# Create an empty DataFrame to store the combined data.
combined_df = pd.DataFrame()

for i, file_path in enumerate(file_paths):
    # Read the CSV file into a DataFrame.
    df = pd.read_csv(os.path.join(result_path, file_path))
    
    # Add a 'name' column to identify which file the data belongs to.
    df['name'] = names[i]
    
    # Concatenate the current DataFrame with the combined DataFrame.
    combined_df = pd.concat([combined_df, df], ignore_index=True)


# Generate a mock dataframe with the structure provided by the user
column_names = [
    'sequence', 'a_gleu_score', 'a_chrf_score', 'a_nist_score', 'a_codeBleu_score', 
    'a_meteor_score', 'a_bleu_score', 'b_gleu_score', 'b_chrf_score', 'b_nist_score', 
    'b_codeBleu_score', 'b_meteor_score', 'b_bleu_score', 'c_gleu_score', 'c_chrf_score', 
    'c_nist_score', 'c_codeBleu_score', 'c_meteor_score', 'c_bleu_score', 'd_gleu_score', 
    'd_chrf_score', 'd_nist_score', 'd_codeBleu_score', 'd_meteor_score', 'd_bleu_score', 
    'e_gleu_score', 'e_chrf_score', 'e_nist_score', 'e_codeBleu_score', 'e_meteor_score', 
    'e_bleu_score', 't1_valid', 't2_valid', 't3_valid', 't4_valid', 't1_ged', 't2_ged', 
    't3_ged', 't4_ged', 't5_ged', 't1_unit', 't2_unit', 't3_unit', 't4_unit'
]

# Function to calculate the average for columns ending with a certain suffix
def calculate_average(df, suffix):
    cols = [col for col in df if col.endswith(suffix)]
    return df[cols].mean(axis=1).mean()

# Calculate the averages and store them in a dictionary
evaluation_averages = {
    name: {
        'average_valid': calculate_average(group, '_valid'),
        'average_ged': calculate_average(group, '_ged'),
        'average_unit': calculate_average(group, '_unit'),
        'average_e_codeBleu_score': group['e_codeBleu_score'].mean()
    }
    for name, group in combined_df.groupby('name')
}

print(evaluation_averages)
