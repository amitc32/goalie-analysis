import pandas as pd
import os

dir = "add dir here"

# List to hold individual DataFrames
dataframes = []

for file in os.listdir(dir):
    if file.endswith(".csv"):
        filepath = os.path.join(dir, file)
        print("Joined ", file, " with csv.")
        df = pd.read_csv(filepath)
        dataframes.append(df)

# concatenate all DataFrames
combined_df = pd.concat(dataframes, ignore_index=True)

# save the combined DataFrame to a new CSV file
combined_df.to_csv("C:/Users/aidan/Desktop/GoaliePredictions/goaliecsv.csv", index=False)

print("Success! On to step 2.")
