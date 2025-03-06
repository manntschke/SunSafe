### Import Script ####

# Run to Import and process data from CSV file in raw folder 

import pandas as pd

import warnings
warnings.simplefilter('ignore')

client_train = pd.read_csv('data/raw/client_train.csv', low_memory=False)
invoice_train = pd.read_csv('data/raw/invoice_train.csv', low_memory=False)

client_test = pd.read_csv('data/raw/client_test.csv', low_memory=False)
invoice_test = pd.read_csv('data/raw/invoice_test.csv', low_memory=False)
sample_submission = pd.read_csv('data/raw/SampleSubmission.csv', low_memory=False)

for df in [invoice_train,invoice_test]:
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])

d={"ELEC":0,"GAZ":1}
invoice_train['counter_type']=invoice_train['counter_type'].map(d)
invoice_test['counter_type']=invoice_test['counter_type'].map(d)

client_train['client_catg'] = client_train['client_catg'].astype(int)
client_train['disrict'] = client_train['disrict'].astype(int)

client_test['client_catg'] = client_test['client_catg'].astype(int)
client_test['disrict'] = client_test['disrict'].astype(int)

def aggregate_by_client_id(invoice_data):
    aggs = {}
    aggs['consommation_level_1'] = ['mean']
    aggs['consommation_level_2'] = ['mean']
    aggs['consommation_level_3'] = ['mean']
    aggs['consommation_level_4'] = ['mean']

    agg_trans = invoice_data.groupby(['client_id']).agg(aggs)
    agg_trans.columns = ['_'.join(col).strip() for col in agg_trans.columns.values]
    agg_trans.reset_index(inplace=True)

    df = (invoice_data.groupby('client_id')
            .size()
            .reset_index(name='{}transactions_count'.format('1')))
    return pd.merge(df, agg_trans, on='client_id', how='left')

agg_train = aggregate_by_client_id(invoice_train)

train = pd.merge(client_train,agg_train, on='client_id', how='left')

agg_test = aggregate_by_client_id(invoice_test)
test = pd.merge(client_test,agg_test, on='client_id', how='left')

sub_client_id = test['client_id']
drop_columns = ['client_id', 'creation_date']

for col in drop_columns:
    if col in train.columns:
        train.drop([col], axis=1, inplace=True)
    if col in test.columns:
        test.drop([col], axis=1, inplace=True)

train.to_csv('data/data_processed/client_data.csv', index=False)
test.to_csv('data/data_processed/validation.csv', index=False)