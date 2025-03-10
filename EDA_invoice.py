# %%
# loading libraries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os

#%% 
# load invoice raw table
invoice = pd.read_csv('data/raw/invoice_train.csv')
# remove rows double
invoice[invoice.duplicated(keep=False)]
invoice = invoice.drop_duplicates()
print("Don't mind the warning, reading_remaked is mixed string and integer")

#%% 
# correct column names
# 'counter_status' is 'counter_status'
invoice.rename(columns={'counter_statue': 'counter_status'}, inplace=True)
# reading_remarque is reading_remark
invoice.rename(columns={'reading_remarque': 'reading_remark'}, inplace=True)
# any column with "consommation is "consumption"
invoice.columns = invoice.columns.str.replace('consommation', 'consumption')
# tarif is tariff
invoice.columns = invoice.columns.str.replace('tarif', 'tariff')
# obviously, names made in french speaking african country...
invoice.columns

#%% 
# add traget and client_id to invoive data
client_info = pd.read_csv('data/raw/client_train.csv')
client_info = client_info[['client_id', 'target']]
invoice = invoice.merge(client_info, on='client_id', how='left')

#%%

# get unique combinations of counter_number and counter_code, per counter type
counter_combinations = invoice.groupby(['counter_number', 'counter_code', 'counter_type'])

# get unique client_id for counter_combinations
unique_clients = counter_combinations['client_id'].nunique()
unique_clients.sort_values(ascending=False)

#%%
# Rows with combination counter_number=0, counter_code = 5, target=1
invoice[(invoice['counter_number'] == 0) & (invoice['counter_code'] == 5) & (invoice['target'] == 1)]
# strange ~ 3500 fraud rows with same counter_number and counter_code combination

# how many cliends have this combination in total?
unique_clients[(unique_clients.index.get_level_values('counter_number') == 0) & (unique_clients.index.get_level_values('counter_code') == 5)]
# >5000 clients have this combination for Gas counters


#%% 
# get date, month and year right
invoice['invoice_date'] = pd.to_datetime(invoice['invoice_date']).dt.date
invoice['year'] = pd.to_datetime(invoice['invoice_date']).dt.year
invoice['month'] = pd.to_datetime(invoice['invoice_date']).dt.month

#%% print for each column with less than 30 unique values the unique values
for col in invoice.columns:
    if invoice[col].nunique() < 30:
        print(f'{col}: {invoice[col].unique()}')
    

#%%
# homogenize counter_status: [0 1 5 4 3 2 769 '0' '5' '1' '4' 'A' 618 269375 46 420]
# Create a dictionary for mapping counter_status values
counter_status_mapping = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5
}

# Map the values using the dictionary to replace them with integers
# rows counter_status unclear - can go Nan and be imputedn NO Frauds
print(invoice[invoice['counter_status'] == "A"]) # one client, no fraud
print(invoice[invoice['counter_status'] == "269375"]) # one row, no fraud
print(invoice[invoice['counter_status'] == "618"]) # one client, no fraud
print(invoice[invoice['counter_status'] == "46"]) # one client, no fraud
print(invoice[invoice['counter_status'] == "769"]) # one client, no fraud
print(invoice[invoice['counter_status'] == "420"]) # one row, no fraud

#%% Set unclear counter_status values to NaN
invoice['counter_status'] = invoice['counter_status'].replace(['A', 269375, 618, 46, 769, 420], np.nan)
invoice['counter_status'] = pd.to_numeric(invoice['counter_status'], errors='coerce').astype('Int64')

# %%
# [ 10  50 20  40  30 ]
# all rows of invoice with counter_coefficient >9
invoice[invoice['counter_coefficient'] > 9]
# how many clients have counter_coefficient >9 per target group?
clients_with_high_coefficient = invoice[invoice['counter_coefficient'] > 9].groupby('target')['client_id'].nunique()
print(clients_with_high_coefficient,"\n\n\n")
# show the client with counter_coefficient larger 9 and target=1
clients_with_high_coefficient = invoice[(invoice['counter_coefficient'] > 9) & (invoice['target'] == 1)]
print(clients_with_high_coefficient, "\n\n\n")

# show the client with counter_coefficient larger 9 and target=0
clients_with_high_coefficient = invoice[(invoice['counter_coefficient'] > 9) & (invoice['target'] == 0)]
print(clients_with_high_coefficient)

#%%
# Create a subset of the invoice data where counter_type is 'GAZ'
invoice_gaz = invoice[invoice['counter_type'] == 'GAZ']

# plot invoice_gaz consumption columns over time
consumption_columns = [col for col in invoice_gaz.columns if 'consumption' in col]

# Plot each consumption column over time side by side for each target
fig, axes = plt.subplots(len(consumption_columns), 2, figsize=(24, 8 * len(consumption_columns)), sharey=True)

for i, column in enumerate(consumption_columns):
    for j, target in enumerate(invoice_gaz['target'].unique()):
        ax = axes[i, j]
        invoice_gaz[invoice_gaz['target'] == target].groupby('invoice_date')[column].sum().plot(ax=ax)
        ax.set_title(f'{column} Over Time for Target {target}')
        ax.set_xlabel('Invoice Date')
        ax.set_ylabel(column)
        ax.legend([column])

plt.tight_layout()
plt.show()


#%%
invoice_elec = invoice[invoice['counter_type'] == 'ELEC']

# plot invoice_elec consumption columns over time
consumption_columns = [col for col in invoice_elec.columns if 'consumption' in col]

# Plot each consumption column over time side by side for each target
fig, axes = plt.subplots(len(consumption_columns), 2, figsize=(24, 8 * len(consumption_columns)), sharey=True)

for i, column in enumerate(consumption_columns):
    for j, target in enumerate(invoice_elec['target'].unique()):
        ax = axes[i, j]
        invoice_elec[invoice_elec['target'] == target].groupby('invoice_date')[column].sum().plot(ax=ax)
        ax.set_title(f'{column} Over Time for Target {target}')
        ax.set_xlabel('Invoice Date')
        ax.set_ylabel(column)
        ax.legend([column])

plt.tight_layout()
plt.show()
# dont kno what to make from this....


#%% print for each column with less than 30 unique values the unique values separately for each counter type
for counter_type in invoice['counter_type'].unique():
    print(f'\nCounter Type: {counter_type}')
    subset = invoice[invoice['counter_type'] == counter_type]
    for col in subset.columns:
        if subset[col].nunique() < 35:
            print(f'{col}: {subset[col].unique()}')

#%%
# show rows where reading_remarque 207, 413, 203
invoice[invoice['reading_remark'] == 207] # one client, no fraud
invoice[invoice['reading_remark'] == 413] # one client, no fraud
invoice[invoice['reading_remark'] == 203] # 2 clients, no fraud
# Dont think we should set them to Nan, maybe the model needs shitty data to learn from
        

#%%
# make new data frame "Gaz",which is invoice counter_type = Gaz
Gaz = invoice[invoice['counter_type'] == 'GAZ']
# get column names where all values are 0 in Gaz
all_zero_columns = Gaz.columns[(Gaz == 0).all()]

# %%
# how many counter numbers per client?
counter_number_per_client = invoice.groupby(['client_id',"year", 'counter_type'])['counter_number'].nunique()
counter_number_per_client.sort_values(ascending=False)

#%%
# how many invoice_dates per client per year per counter_number
invoice_dates_per_year = invoice.groupby(['client_id',"counter_type", 'counter_number', 'year'])['invoice_date'].nunique()
invoice_dates_per_year.sort_values(ascending=False)


#%%
# old_idex and new_index: what they do not have in common
# Find the differences between old_index and new_index columns
old_index = invoice['old_index'].dropna().unique()
new_index = invoice['new_index'].dropna().unique()

# Elements in old_index but not in new_index
old_not_in_new = np.setdiff1d(old_index, new_index)
print("Elements in old_index but not in new_index:", len(old_not_in_new))

# Elements in new_index but not in old_index
new_not_in_old = np.setdiff1d(new_index, old_index)
print("Elements in new_index but not in old_index:", len(new_not_in_old))

# Elements in both old_index and new_index
common_elements = np.intersect1d(old_index, new_index)
print("Elements in both old_index and new_index:", len(common_elements))




# delete columns containing index in column name
#invoice = invoice.loc[:, ~invoice.columns.str.contains('index')]


#%%
# Calculate the number of unique invoice dates per counter_type and client
unique_invoice_dates = invoice.groupby(['counter_type', 'client_id'])['invoice_date'].nunique()

# Calculate the number of invoice dates per year per client and counter type
invoice['invoice_year'] = pd.to_datetime(invoice['invoice_date']).dt.year
invoice_dates_per_year = invoice.groupby(['counter_type', 'client_id', 'invoice_year'])['invoice_date'].nunique()

# Calculate the number of customers per year per counter type
customers_per_year = invoice.groupby(['counter_type', 'invoice_year'])['client_id'].nunique().reset_index()
customers_per_year.rename(columns={'client_id': 'num_customers'}, inplace=True)

# Calculate the number of bills per year divided by the number of customers per year
invoice_counts = invoice.groupby(['counter_type', 'invoice_year'])['invoice_date'].nunique().reset_index()
invoice_counts = invoice_counts.merge(customers_per_year, on=['counter_type', 'invoice_year'])
invoice_counts['bills_per_customer'] = invoice_counts['invoice_date'] / invoice_counts['num_customers']

# Plot the number of bills per year divided by the number of customers per year
invoice_counts_pivot = invoice_counts.pivot(index='invoice_year', columns='counter_type', values='bills_per_customer')
invoice_counts_pivot.plot(kind='bar', figsize=(12, 8), colormap='viridis')
plt.title('Number of Bills per Year per Customer per Counter Type')
plt.xlabel('Year')
plt.ylabel('Number of Bills per Customer')
plt.xticks(rotation=45)
plt.legend(title='Counter Type')
plt.show()

# %%
# which customer with 3.5 invoices in counter_type= Gaz in 1985
invoice.counter_type.unique()
invoice.columns
# get number of invoive_dates per year and client_id
invoice_dates_per_year = invoice.groupby(['counter_type', 'client_id', 'invoice_year'])['invoice_date'].nunique().reset_index()

# %%
# aggregate (sum) the number of invoice_date per client per year per counter
# Aggregate data by counter_type, invoice_year, and client_id to get the sum of invoice_date
invoice_dates_per_year_counter = invoice_dates_per_year[invoice_dates_per_year['invoice_date'] > 0].groupby(['counter_type', 'invoice_year', 'client_id'])['invoice_date'].sum().reset_index()
# Remove rows where the count is zero
invoice_dates_per_year_counter = invoice_dates_per_year_counter[invoice_dates_per_year_counter['invoice_date'] > 0]

# %%
# mean number of invoice_date per customer per year per counter type, counter types as categoty
# Aggregate data by counter_type, invoice_year, and client_id to get the mean of invoice_date
invoice_dates_per_year_counter_mean = invoice_dates_per_year_counter.groupby(['counter_type', 'invoice_year'])['invoice_date'].mean().reset_index()
invoice_dates_per_year_counter_mean['counter_type'] = invoice_dates_per_year_counter_mean['counter_type'].astype('category')

# Plot the mean number of invoice dates per customer per year per counter type
invoice_dates_per_year_counter_mean_pivot = invoice_dates_per_year_counter_mean.pivot(index='invoice_year', columns='counter_type', values='invoice_date')
invoice_dates_per_year_counter_mean_pivot.plot(kind='bar', figsize=(12, 8), colormap='viridis')
plt.title('Mean Number of Invoice Dates per Customer per Year per Counter Type')
plt.xlabel('Year')
plt.ylabel('Mean Number of Invoice Dates')
plt.xticks(rotation=45)
plt.legend(title='Counter Type')
plt.show()


# %%
# how many invoive dates each client has per year on average
invoice_dates_per_year_counter_mean_client = invoice_dates_per_year_counter.groupby(['counter_type', 'invoice_year', 'client_id'])['invoice_date'].mean().reset_index()
invoice_dates_per_year_counter_mean_client['counter_type'] = invoice_dates_per_year_counter_mean_client['counter_type'].astype('category')

# how many invoice_dates larger than 1 per clients_id and year and counter type
invoice_dates_per_year_counter_mean_client = invoice_dates_per_year_counter_mean_client[invoice_dates_per_year_counter_mean_client['invoice_date'] > 1]
# extract client names from invoice_dates_per_year_counter_mean_client
client_names = invoice_dates_per_year_counter_mean_client['client_id'].unique()
# get all rows from invoice with client_id in client_names
invoice_clients = invoice[invoice['client_id'].isin(client_names)]
# get month of invoice_date
invoice_clients['month'] = pd.to_datetime(invoice_clients['invoice_date']).dt.month
invoice_clients['month'].unique()

# get from invoice df on ly those cliend_id where, where invoice was sent in every month of a year
invoice_clients['year'] = pd.to_datetime(invoice_clients['invoice_date']).dt.year
invoice_clients['month'] = pd.to_datetime(invoice_clients['invoice_date']).dt.month


#%%
# remove old index and new index
invoice = invoice.drop(columns=['old_index', 'new_index'], axis=1)
# count counter_coefficient per counter_type

#%%
# table with counts of counter_type per target and counter coefficient for target=1
counter_coefficient_counts = invoice[invoice['target'] == 1].groupby(['target', 'counter_type', 'counter_coefficient']).size().reset_index(name='count')
counter_coefficient_pivot = counter_coefficient_counts.pivot_table(index=['target', 'counter_type'], columns='counter_coefficient', values='count', fill_value=0)
print(counter_coefficient_pivot)

#%%
# table with counts of counter_type per target and counter_status for target=1
counter_status_counts = invoice[invoice['target'] == 1].groupby(['target', 'counter_type', 'counter_status']).size().reset_index(name='count')
counter_status_pivot = counter_status_counts.pivot_table(index=['target', 'counter_type'], columns='counter_status', values='count', fill_value=0)
print(counter_status_pivot)
invoice.counter_status.unique()

#%%
# Count unique values of counter_status for target=1 grouped by counter_type
counter_status_unique_counts = invoice[invoice['target'] == 1].groupby(['target', 'counter_type'])['counter_status'].nunique().reset_index(name='unique_counter_status_count')
print(counter_status_unique_counts)

# Count occurrences of each counter_status for target=1 grouped by counter_type
counter_status_counts_per_target = invoice[invoice['target'] == 1].groupby(['target', 'counter_type', 'counter_status']).size().reset_index(name='count')
print(counter_status_counts_per_target)

# Plot occurrences of each counter_status for target=1 grouped by counter_type
plt.figure(figsize=(12, 8))
sns.barplot(data=counter_status_counts_per_target, x='counter_status', y='count', hue='counter_type', palette='viridis')
plt.title('Occurrences of Each Counter status for Target=1 Grouped by Counter Type')
plt.xlabel('Counter status')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.legend(title='Counter Type')
plt.show()
# note: the fraudulent people have 0 mostly as counter_status



# %%
# Count unique values of reading_remarque for target=1 grouped by counter_type
reading_remarque_unique_counts = invoice[invoice['target'] == 1].groupby(['target', 'counter_type'])['reading_remark'].nunique().reset_index(name='unique_reading_remarque_count')
print(reading_remarque_unique_counts)

# Count occurrences of each reading_remarque for target=1 grouped by counter_type
reading_remarque_counts_per_target = invoice[invoice['target'] == 1].groupby(['target', 'counter_type', 'reading_remark']).size().reset_index(name='count')
print(reading_remarque_counts_per_target)

# Plot occurrences of each reading_remarque for target=1 grouped by counter_type
plt.figure(figsize=(12, 8))
sns.barplot(data=reading_remarque_counts_per_target, x='reading_remark', y='count', hue='counter_type', palette='viridis')
plt.title('Occurrences of Each Reading Remark for Target=1 Grouped by Counter Type')
plt.xlabel('Reading Remarque')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.legend(title='Counter Type')
plt.show()
# note: the fraudulent people have mostly 6,8,9 as reading_remarque


# %%
# Count unique values of tarif_type for target=1 grouped by counter_type
tarif_type_unique_counts = invoice[invoice['target'] == 1].groupby(['target', 'counter_type'])['tariff_type'].nunique().reset_index(name='unique_tarif_type_count')
print(tarif_type_unique_counts)

# Count occurrences of each tarif_type for target=1 grouped by counter_type
tarif_type_counts_per_target = invoice[invoice['target'] == 1].groupby(['target', 'counter_type', 'tariff_type']).size().reset_index(name='count')
print(tarif_type_counts_per_target)

# Plot occurrences of each tarif_type for target=1 grouped by counter_type
plt.figure(figsize=(12, 8))
sns.barplot(data=tarif_type_counts_per_target, x='tariff_type', y='count', hue='counter_type', palette='viridis')
plt.title('Occurrences of Each Tarif Type for Target=1 Grouped by Counter Type')
plt.xlabel('Tarif Type')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.legend(title='Counter Type')
plt.show()
# note: the fraudulent people have mostly specific tarif types 11, 10, 40 and a few others


# %%
# Count unique values of counter_coefficient for target=1 grouped by counter_type
counter_coefficient_unique_counts = invoice[invoice['target'] == 1].groupby(['target', 'counter_type'])['counter_coefficient'].nunique().reset_index(name='unique_counter_coefficient_count')
print(counter_coefficient_unique_counts)

# Count occurrences of each counter_coefficient for target=1 grouped by counter_type
counter_coefficient_counts_per_target = invoice[invoice['target'] == 1].groupby(['target', 'counter_type', 'counter_coefficient']).size().reset_index(name='count')
print(counter_coefficient_counts_per_target)

# Plot occurrences of each counter_coefficient for target=1 grouped by counter_type
plt.figure(figsize=(12, 8))
sns.barplot(data=counter_coefficient_counts_per_target, x='counter_coefficient', y='count', hue='counter_type', palette='viridis')
plt.title('Occurrences of Each Counter Coefficient for Target=1 Grouped by Counter Type')
plt.xlabel('Counter Coefficient')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.legend(title='Counter Type')
plt.show()
# note: the fraudulent people have counter coefficients 1

# %%
# Count unique values of counter_coefficient for target=1 grouped by counter_type
consumption_level_1_unique_counts = invoice[invoice['target'] == 1].groupby(['target', 'counter_type'])['consumption_level_1'].nunique().reset_index(name='unique_consumption_level_1_count')
print(consumption_level_1_unique_counts)

# Count occurrences of each consommation_level_1 for target=1 grouped by counter_type
consumption_level_1_counts_per_target = invoice[invoice['target'] == 1].groupby(['target', 'counter_type', 'consumption_level_1']).size().reset_index(name='count')
print(consumption_level_1_counts_per_target)

# Plot occurrences of each consommation_level_1 for target=1 grouped by counter_type
plt.figure(figsize=(12, 8))
sns.barplot(data=consumption_level_1_counts_per_target, x='consommation_level_1', y='count', hue='counter_type', palette='viridis')
plt.title('Occurrences of Each Consommation Level 1 for Target=1 Grouped by Counter Type')
plt.xlabel('Consommation Level 1')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.legend(title='Counter Type')
plt.show()
# note: the fraudulent people have specific comsommation levels

# %%
len(invoice.consumption_level_1.unique())
# unique sorted ascending values from consumption_level_1
unique_sorted_values = sorted(invoice['consumption_level_1'].unique())
print(unique_sorted_values)
# consumption_level_1 per target = 1
consumption_level_1_target_1 = invoice[invoice['target'] == 1]['consumption_level_1']
# sort ascending and check if sequence is continuously +1
unique_sorted_values_target_1 = sorted(consumption_level_1_target_1.unique())
# scatterplot consumption_level_1(x) over target count(y) side by side for each target
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

for target, ax in zip(invoice['target'].unique(), axes):
    consumption_level_1_target = invoice[invoice['target'] == target]['consumption_level_1']
    unique_sorted_values_target = sorted(consumption_level_1_target.unique())
    ax.scatter(unique_sorted_values_target, consumption_level_1_target.value_counts().sort_index())
    ax.set_xlabel('Consumption Level 1')
    ax.set_ylabel('Count')
    ax.set_title(f'Consumption Level 1 vs. Count for Target {target}')
    ax.set_ylim(bottom=0)  # Free y-axis

plt.tight_layout()
plt.show()


# %%
# Boxplot for all columns containing "consumption" in the column name
consumption_columns = [col for col in invoice.columns if 'consumption' in col]
# pivot: one consumption level with consumption columns values

# for each consumption_columns, aggregate mean per client_id and counter_type
consumption_columns_agg = invoice.groupby(['client_id', 'counter_type'])[consumption_columns].mean().reset_index()
# pivot to long format consumption_columns

#%%
consumption_columns_long = pd.melt(consumption_columns_agg, id_vars=['client_id', 'counter_type'], value_vars=consumption_columns, var_name='consumption_level', value_name='consumption_value')
# merge target from invoice to consumption_columns_long
consumption_columns_long = consumption_columns_long.merge(invoice[['client_id', 'target']].drop_duplicates(), on='client_id', how='left')

# plot consumption_columns_long side by side for target=1 and target=0
fig, axes = plt.subplots(1, 2, figsize=(24, 8), sharey=True)

for target, ax in zip([0, 1], axes):
    sns.boxplot(data=consumption_columns_long[consumption_columns_long['target'] == target], x='consumption_level', y='consumption_value', hue='counter_type', palette='viridis', ax=ax)
    ax.set_title(f'Consumption Level Boxplot by Counter Type for Target {target}')
    ax.set_xlabel('Consumption Level')
    ax.set_ylabel('Consumption Value')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.legend(title='Counter Type')

plt.tight_layout()
plt.show()

