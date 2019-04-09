import pandas as pd
import re

crocus_data = pd.read_json("./crocus.jl", lines=True)

newColumns = crocus_data["height"].apply(lambda x: re.findall(r"\d+", x))
nd = []
for i,r in newColumns.iteritems():
    if(len(r) == 2):
        nd.append({
            "index": i,
            "potSize": r[0],
            "height": r[1]
        })
    else:
        nd.append({
            "index": i,
            "potSize": None,
            "height": None
        })

crocus_data.update(nd)
print(crocus_data.to_json("./crocus_post.jl", orient="records", lines=True))