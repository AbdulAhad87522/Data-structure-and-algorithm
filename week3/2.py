# !pip install matplotlib #if already not installed 
import matplotlib.pyplot as plt  
import pandas as pd 
df = pd.read_csv('dailyActivity_merged.csv' )  
print(df.dtypes) 
list1 = df['ActivityDate'].values.tolist()  
list2 = df['TotalSteps'].values.tolist()  
plt.bar(list1, list2,width = 1, color = ['red', 'green']) 
plt.show()
