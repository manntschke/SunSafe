#%%
#!pip install matplotlib
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os

#%% only execute once to get files
# from import_script import import_script
# import_script()


#%%
# Load data
df = pd.read_csv('data/data_processed/client_data.csv')

# %%
# Check data
print(df.head())
print(df.info())
print(df.describe())

# %%
# Check missing values
print(df.isnull().sum())

# %%
# Check unique values
print(df.nunique())

# %%
# Check distribution of target variable
sns.countplot(data=df, x='target', palette='viridis')
plt.title('Distribution of target variable')
plt.show()
plt.clf()


#%%
# histogram of numerical variables
numerical_columns = df.select_dtypes(include=[np.number]).columns
num_plots = len(numerical_columns)
num_cols = 3  # Number of subplots per row
num_rows = (num_plots + num_cols - 1) // num_cols  # Calculate number of rows needed
fig, axes = plt.subplots(num_rows, num_cols, figsize=(5 * num_cols, 5 * num_rows))

# Flatten axes array if there are multiple rows
if num_rows > 1:
    axes = axes.flatten()
else:
    axes = [axes]  # Ensure axes is always a list

colors = sns.color_palette('viridis', len(df['target'].unique()))

for ax, column in zip(axes, numerical_columns):
    for target_level, color in zip(df['target'].unique(), colors):
        subset = df[df['target'] == target_level]
        subset[column].hist(ax=ax, bins=30, alpha=0.8, edgecolor='black', label=f'Target {target_level}', color=color)
    ax.set_title(f'{column}', fontsize=20)
    ax.legend(fontsize=14)
    ax.tick_params(axis='x', rotation=90, labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.grid(False)  # Disable gridlines inside the plot
    for spine in ax.spines.values():
        spine.set_edgecolor('#d3d3d3')  # Set color of the subplot borders
# Remove any unused subplots
if num_plots < len(axes):
    for i in range(num_plots, len(axes)):
        fig.delaxes(axes[i])

plt.tight_layout()
plt.show()
    
# %%
# Check distribution of numerical variables colored by target level
numerical_columns = df.select_dtypes(include=[np.number]).columns

for column in numerical_columns:
    g = sns.FacetGrid(df, col='target', hue='target', sharey=False, height=4, aspect=1.5, palette='viridis', legend_out=False)
    g.map(sns.histplot, column, bins=30, edgecolor='black')
    g.add_legend()
    g.figure.suptitle(f'Distribution of {column} by Target Level', y=1.05)
    plt.show()
    plt.clf()
    plt.close('all')
    del g

# %%
# boxplot of numerical variables with log scale for y-axis
numerical_columns = [col for col in numerical_columns if col not in ['client_cat', 'target']]
for column in numerical_columns:
    sns.boxplot(data=df, x='target', y=column, palette='viridis')
    plt.yscale('log')  # Set y-axis to log scale
    plt.title(f'Log {column} by Target')
    plt.show()
    
# %%
# categorical variables
# Plot for client_cat
sns.countplot(data=df, x='client_catg', hue='target', palette='viridis')
plt.title('client_cat by Target')
plt.xticks(rotation=90)
plt.show()

# %%
# Convert categorical columns to type 'category'
categorical_columns = ['disrict', 'client_catg', 'region', 'target']
for column in categorical_columns:
    df[column] = df[column].astype('category')

print(df.dtypes)

# %%
# Count unique values for float and integer data types
numerical_columns = df.select_dtypes(include=[np.number]).columns

for column in numerical_columns:
    unique_values = df[column].nunique()
    print(f'Column {column} has {unique_values} unique values')

# %%
# Copy data and set 0 to NaN in all columns containing "consum" in the column name
df_copy = df.copy()
consum_columns = [col for col in df_copy.columns if 'consum' in col]

for column in consum_columns:
    df_copy[column] = df_copy[column].replace(0, np.nan)

#print(df_copy.head())
#print(df_copy.describe())

# %%
numerical_columns = df_copy.select_dtypes(include=[np.number]).columns

for column in numerical_columns:
    g = sns.FacetGrid(df_copy, col='target', hue='target', sharey=False, height=4, aspect=1.5, palette='viridis', legend_out=False)
    g.map(sns.histplot, column, bins=30, edgecolor='black')
    g.add_legend()
    g.figure.suptitle(f'Distribution of {column} by Target Level', y=1.05)
    plt.show()
    plt.clf()
    plt.close('all')
    del g
  # %%
