
#%%
import numpy as np 
import pandas as pd
from fuzzywuzzy import process
import re

#%%
supplier_data = pd.read_json("./florAccess.jl", lines=True)
crocus_data = pd.read_json("./crocus_post.jl", lines=True)

#%%
def get_data():
    for i, plant in supplier_data.iterrows():
        plant_name = plant["name"]
        print("Searching for... {}".format(plant_name))
        result = process.extractOne(plant_name, crocus_data["name"])
        
        print("Best Match... {} at {}%".format(result[0], result[1]))
        matching_plant = crocus_data.iloc[result[2], :]
        yield {
            "supplier_id" : i,
            "supplier_name" : plant["name"],
            "supplier_price" : plant["price"],
            "supplier_potSize" : plant["potSize"],
            "supplier_height" : plant["height"],
            "crocus_id": result[2],
            "crocus_name" : matching_plant["name"],
            "crocus_price" : matching_plant["price"],
            "crocus_potSize" : matching_plant["potSize"],
            "crocus_height" : matching_plant["height"],
            "perc_match" : result[1] / 100
        }

out = get_data()
print("Done")

#%%
df = pd.DataFrame(get_data())

#%%
df[(df["perc_match"] > 0.88)] \
    .assign(price_diff = df["crocus_price"] - df["supplier_price"]) \
    .assign(margin = (df["crocus_price"] - df["supplier_price"]) / df["crocus_price"] ) \
    .sort_values(["perc_match", "margin"], ascending=False) \
        [["supplier_name", "crocus_name", "perc_match", "price_diff", "supplier_potSize", "supplier_height", "crocus_potSize", "crocus_height", "supplier_price", "margin"]]