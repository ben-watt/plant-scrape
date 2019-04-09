
#%%
import pandas as pd
import matplotlib.pyplot as plt
import re

df = pd.read_json("./florAccess.jl", lines=True)
df["price"] = pd.to_numeric(df["price"].apply(lambda x : re.search(r"\d.+", x)[0]))
df.columns

#%%
df["layer_cost"] = df['price'] * df['per_trolley'] # ToDo: This should be per layer but the scraper was wrong

#%%
df.describe()

#%%
cheapest_products = df[df["layer_cost"].notna()].sort_values("layer_cost").head(12)
cheapest_products
#%%
cheapest_products.sum(numeric_only=True)

#%%
df["height"].describe()

#%%
