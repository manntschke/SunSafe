#%%
# Libraries
import pandas as pd
import numpy as np

import sklearn
import matplotlib.pyplot as plt
import seaborn as sns

import warnings




# %%
# load raw data client
df = pd.read_csv("data/raw/client_train.csv")
df.columns

# %%
# scatterplot disrict over region
sns.scatterplot(data=df, x="disrict", y="region")

# how many unique disrict-region pairs?
df[["disrict", "region"]].drop_duplicates()


# count client_id per unique district-region pairs 
print(df.groupby(["disrict", "region"])["client_id"].nunique().sort_values().head(30))

# count unique district-region pairs for each client_id
len(df.groupby("client_id"))

