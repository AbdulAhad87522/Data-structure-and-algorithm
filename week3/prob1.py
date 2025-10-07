# !pip install matplotlib #if already not installed 
import matplotlib.pyplot as plt  
import pandas as pd 
# df = pd.read_csv('population_by_country_2020.csv' )  
# print(df.dtypes) 
# list1 = df['Country (or dependency)'].values.tolist()  
# list2 = df['Population (2020)'].values.tolist()  
# plt.bar(list1, list2,width = 1, color = ['red', 'green']) 
# plt.show()

# # #1
# # import matplotlib.pyplot as plt  
# # import pandas as pd 

# df = pd.read_csv('dailyActivity_merged.csv')  
# print(df.dtypes) 

# # Convert ActivityDate to datetime for better plotting
# df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])

# lis1 = df['ActivityDate'].values.tolist()  
# lis2 = df['TotalSteps'].values.tolist()  

# # Create line chart instead of bar chart
# plt.figure(figsize=(12, 6))
# plt.plot(lis1, lis2, marker='o', linewidth=2, markersize=4, color='blue')
# plt.title('Total Number of Steps on Daily Basis', fontsize=14)
# plt.xlabel('Date', fontsize=12)
# plt.ylabel('Total Steps', fontsize=12)
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()

# # #3
# # # import matplotlib.pyplot as plt  
# # # import pandas as pd 

# # Load the data
# df = pd.read_csv('dailyActivity_merged.csv')  
# print(df.dtypes) 

# # Convert ActivityDate to datetime for better plotting
# df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])

# # Extract the data for plotting
# dates = df['ActivityDate'].values.tolist()  
# distances = df['TotalDistance'].values.tolist()  

# # Create BAR CHART for daily distance covered
# plt.figure(figsize=(14, 7))
# plt.bar(dates, distances, color='skyblue', edgecolor='navy', alpha=1)
# plt.title('Daily Distance Covered', fontsize=16, fontweight='bold')
# plt.xlabel('Date', fontsize=12)
# plt.ylabel('Total Distance (miles/km)', fontsize=12)
# plt.grid(True, linestyle='--', alpha=1, axis='y' )
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()


# # #4

# # import matplotlib.pyplot as plt  
# # import pandas as pd 

# # Load the data
# df = pd.read_csv('sleepDay_merged.csv')  
# print(df.dtypes) 

# # Convert SleepDay to datetime for better plotting
# df['SleepDay'] = pd.to_datetime(df['SleepDay'])

# # Extract the data for plotting - Use TotalTimeInBed instead of TotalSleepRecords
# dates = df['SleepDay'].values.tolist()  
# total_time_in_bed = df['TotalTimeInBed'].values.tolist()  

# # Create SCATTER CHART for total time in bed
# plt.figure(figsize=(14, 7))
# plt.scatter(dates, total_time_in_bed, color='red', alpha=0.7, s=50)  # s=50 controls point size
# plt.title('Total Time in Bed - Scatter Chart', fontsize=16, fontweight='bold')
# plt.xlabel('Date', fontsize=12)
# plt.ylabel('Total Time in Bed (minutes)', fontsize=12)
# plt.grid(True, linestyle='--', alpha=0.7, axis='y')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# #5

df = pd.read_csv('hourlySteps_merged.csv')
print(df.dtypes)

df['ActivityHour'] = pd.to_datetime(df['ActivityHour'])
april_12 = pd.to_datetime('2016-04-12').date() in df['ActivityHour'].dt.date.values

print(df['ActivityHour'].dt.date.unique())
print("does exite {april_12}")

filtered_df = df[df['ActivityHour'].dt.date == pd.to_datetime('2016-04-12').date()]

hours = filtered_df['ActivityHour'].dt.hour.values
step_total = filtered_df['StepTotal'].values

# print(f"\n total {len(hours)} found")
    
# print("total hours ", hours)
# print("total steps" , step_total)

plt.pie(hours , labels = step_total , autopct='%1.0f%%')
plt.title(' pie chart')
plt.show()

# import matplotlib.pyplot as plt

# Quick test
# data = [25, 35, 20, 20]
# labels = ['A', 'B', 'C', 'D']

# plt.pie(data, labels=labels, autopct='%1.0f%%')
# plt.title('Simple Pie Chart')
# plt.show()