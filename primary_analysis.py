import pandas as pd
import matplotlib.pyplot as plt

def preloading(csvfile):
    # Load your CSV file
    df = pd.read_csv(csvfile)

    # Filter rows where 'situation' contains 'all'
    parsed_df = df[df['situation'].astype(str).str.contains("all", case=False, na=False)]

    # Remove rows where values are zero
    parsed_df = parsed_df[parsed_df!= 0]

    # New column creation
    parsed_df = parsed_df.sort_values(by='season', ascending=True)
    parsed_df['icetime_per_xGoals'] = parsed_df['icetime'] / parsed_df['xGoals']
    parsed_df['icetime_per_xRebounds'] = parsed_df['icetime'] / parsed_df['xRebounds']
    parsed_df['icetime_per_xFreeze'] = parsed_df['icetime'] / parsed_df['xFreeze']
    parsed_df['icetime_per_xOnGoal'] = parsed_df['icetime'] / parsed_df['xOnGoal']
    parsed_df['icetime_per_xLowDangerGoals'] = parsed_df['icetime'] / parsed_df['lowDangerxGoals']
    parsed_df['icetime_per_xMedDangerGoals'] = parsed_df['icetime'] / parsed_df['mediumDangerxGoals']
    parsed_df['icetime_per_xHighDangerGoals'] = parsed_df['icetime'] / parsed_df['highDangerxGoals']
    return parsed_df

# Function to calculate weighted average
def calculate_weighted_average(df, metric, weight_column, group_column):
    return df.groupby(group_column).apply(
        lambda x: (x[metric] * x[weight_column]).sum() / x[weight_column].sum()
    ).reset_index(name=f'weighted_avg_{metric}')


# Define a function to remove outliers using IQR
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]


parsed_df = preloading("enter path here")


# Prepare the data for plotting
metrics = [
    'icetime_per_xGoals', 'icetime_per_xRebounds', 'icetime_per_xFreeze',
    'icetime_per_xOnGoal', 'icetime_per_xLowDangerGoals', 
    'icetime_per_xMedDangerGoals', 'icetime_per_xHighDangerGoals'
]

for metric in metrics:
    parsed_df = remove_outliers_iqr(parsed_df, metric)

weighted_averages = []

#weighted average for each metric grouped by season
for metric in metrics:
    weighted_avg = calculate_weighted_average(parsed_df, metric, 'icetime', 'season')
    weighted_averages.append(weighted_avg)

#combine all weighted averages
weighted_avg_df = pd.concat(weighted_averages, axis=1)

#remove duplicate columns
weighted_avg_df = weighted_avg_df.loc[:, ~weighted_avg_df.columns.duplicated()]
print(weighted_avg_df)

# Plot
fig, axes = plt.subplots(len(metrics), 1, figsize=(12, 20), sharex=True)
for i, metric in enumerate(metrics):
    weighted_metric = f'weighted_avg_{metric}'
    axes[i].plot(weighted_avg_df['season'], weighted_avg_df[weighted_metric], marker='o', label=weighted_metric, color='g')
    axes[i].set_title(weighted_metric, fontsize=14)
    axes[i].set_ylabel('Weighted Average', fontsize=10)
    axes[i].grid(visible=True, linestyle='--', alpha=0.6)
    axes[i].legend()
plt.xlabel('Season', fontsize=12)
plt.tight_layout()
plt.show()
