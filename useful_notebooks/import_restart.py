# %%
### Import Script ####

# Run to Import and process data from CSV file in raw folder 
# def import_script():

# %%
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter('ignore')

# %%
client_train_import = pd.read_csv('data/raw/client_train.csv', low_memory=False)
invoice_train_import = pd.read_csv('data/raw/invoice_updated.csv', low_memory=False)

client_test_import = pd.read_csv('data/raw/client_test.csv', low_memory=False)
invoice_test_import = pd.read_csv('data/raw/invoice_test.csv', low_memory=False)

invoice_test_import.columns

col_names =['client_id',
       'invoice_date',
       'tariff_type', 
       'counter_number',
       'counter_status',
       'counter_code',
       'reading_remark',
       'counter_coefficient',
       'consumption_level_1',
       'consumption_level_2',
       'consumption_level_3',
       'consumption_level_4', 'old_index',
       'new_index',
       'months_number',
       'counter_type']

# assign col_names to invoice_test_import
invoice_test_import.columns = col_names

#%%
invoice_train_import[invoice_train_import['invoice_date'] >= '2005-01-01']

# %%
client_train = client_train_import.copy()
invoice_train = invoice_train_import.copy()

client_test = client_test_import.copy() 
invoice_test = invoice_test_import.copy()


# NEW: thereare 11 duplicated rows in invoice! dropped here
# get all rows from invoice that are double
invoice_test[invoice_test.duplicated(keep=False)]
#remove duplicated rows
invoice_test = invoice_test.drop_duplicates()

# %%
#changing dates to datetime format
for df in [invoice_train,invoice_test]:
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
df.head()

# %%
counter_info_train = invoice_train['counter_type']
counter_info_test = invoice_test['counter_type']

invoice_train = pd.get_dummies(invoice_train, columns=['counter_type'], dtype=int)
invoice_test = pd.get_dummies(invoice_test, columns=['counter_type'], dtype=int)

invoice_train = pd.concat([invoice_train, counter_info_train], axis=1)
invoice_test = pd.concat([invoice_test, counter_info_test], axis=1)  

d={"ELEC":0,"GAZ":1}
invoice_train['counter_type']=invoice_train['counter_type'].map(d)
invoice_test['counter_type']=invoice_test['counter_type'].map(d)


# %%
invoice_train.head()

# %%
client_train['client_catg'] = client_train['client_catg'].astype(int)
client_train['disrict'] = client_train['disrict'].astype(int)

client_test['client_catg'] = client_test['client_catg'].astype(int)
client_test['disrict'] = client_test['disrict'].astype(int)

def aggregate_by_client_id(invoice_data):
    aggs  = {
        'consumption_level_1': ['mean'],
        'consumption_level_2': ['mean'],
        'consumption_level_3': ['mean'],
        'consumption_level_4': ['mean'],
        'counter_type_ELEC': ['mean'],
        'counter_type_GAZ': ['mean'],
      #  'counter_type': ['mean']            
    }

    agg_trans = invoice_train.groupby(['client_id']).agg(aggs)
    agg_trans.columns = ['_'.join(col).strip() for col in agg_trans.columns.values]
    agg_trans.reset_index(inplace=True)

    df = (invoice_data.groupby('client_id')
            .size()
            .reset_index(name='{}transactions_count'.format('1')))
    
    dfreturn = pd.merge(df, agg_trans, on='client_id', how='left')

    return dfreturn

# %%
# def aggregate_by_client_id(invoice_data):
#     aggs = {
#         'consumption_level_1': ['mean'],
#         'consumption_level_2': ['mean'],
#         'consumption_level_3': ['mean'],
#         'consumption_level_4': ['mean'],
#         'counter_type_ELEC': ['mean'],
#         'counter_type_GAZ': ['mean'],
#         'counter_type': ['mean']            
#     }

#     agg_trans = invoice_data.groupby(['client_id']).agg(aggs)
#     agg_trans.columns = ['_'.join(col).strip() for col in agg_trans.columns.values]
#     agg_trans.reset_index(inplace=True)

#     df = (invoice_data.groupby(['client_id'])
#             .size()
#             .reset_index(name='transactions_count'))

#     # Count transactions grouped by counter_type
#     counter_type_counts = invoice_data.groupby(['client_id', 'counter_type']).size().unstack(fill_value=0)
#     counter_type_counts.columns = [f'transactions_count_{col}' for col in counter_type_counts.columns]
#     counter_type_counts.reset_index(inplace=True)

#     dfreturn = pd.merge(df, agg_trans, on='client_id', how='left')
#     dfreturn = pd.merge(dfreturn, counter_type_counts, on='client_id', how='left')

#     return dfreturn

# %%
agg_train = aggregate_by_client_id(invoice_train)

train = pd.merge(client_train,agg_train, on='client_id', how='left')

agg_test = aggregate_by_client_id(invoice_test)
test = pd.merge(client_test,agg_test, on='client_id', how='left')

drop_columns = ['client_id', 'creation_date']

# %%
train.sort_values(by='counter_type_ELEC_mean', ascending=True).head(10)

# %%
drop_columns = ['client_id', 'counter_type_ELEC_mean', 'counter_type_GAZ_mean', 'counter_type_mean']

for col in drop_columns:
    if col in train.columns:
        train.drop([col], axis=1, inplace=True)
    if col in test.columns:
        test.drop([col], axis=1, inplace=True)


# %%
train.head()

# %%
train.to_csv('data/data_processed/client_data.csv', index=False)
test.to_csv('data/data_processed/validation.csv', index=False)


