import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load Data
main_df = pd.read_csv('Train.csv')
test_df = pd.read_csv('Test.csv')
print(main_df.head())
print(main_df.columns)  

# Step 2: Scatter Graph
disease_map = {'ALLERGY': 1, 'COVID': 2, 'COLD': 3, 'FLU': 4}
main_df['LabelNum'] = main_df['TYPE'].map(disease_map)

for col in main_df.columns[:-2]:
    plt.scatter(main_df[col], main_df['LabelNum'])
    plt.title(f"{col} vs Disease")
    plt.xlabel(col)
    plt.ylabel("Disease Category")
    plt.show()

# Step 3: Distance Function
def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))

predicted_labels = []

# Step 4: Predict Labels for Test Data
for i, test_row in test_df.iterrows():
    distances = []
    for j, train_row in main_df.iloc[:, :-2].iterrows():
        dist = euclidean_distance(test_row, train_row)
        distances.append(dist)
    min_index = np.argmin(distances)
    predicted_labels.append(main_df.loc[min_index, 'TYPE'])

test_df['Predicted_Label'] = predicted_labels
print(test_df)