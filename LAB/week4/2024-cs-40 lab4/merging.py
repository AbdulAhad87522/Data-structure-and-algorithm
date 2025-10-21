import pandas as pd

df = pd.read_csv("mobile.csv")
df1 = pd.read_csv("product.csv")
merged_df = pd.concat([df,df1], ignore_index=True)

merged_df.to_csv("merged_csv.csv")
