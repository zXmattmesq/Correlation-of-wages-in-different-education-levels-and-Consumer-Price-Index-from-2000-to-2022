import pandas as pd
import matplotlib.pyplot as plt


CPI = pd.read_csv("US_inflation_rates.csv")
wages = pd.read_csv("wages_by_education.csv")

#Clean Data
CPI = CPI.dropna()
wages = wages[::-1]
wages = wages.dropna()
wages = wages.drop_duplicates()

CPI = CPI[CPI['value'] > 169.3]
CPI = CPI[CPI['value'] < 298.99]
CPI['date'] = pd.to_datetime(CPI['date'])

wages = wages[wages['year'] > 1999]
wages = wages.iloc[:, :6]


wage_years = wages['year']
wages_noYear = wages.drop(columns='year') 


# Plotting line graph 1
plt.figure(figsize=(8, 6))
for column in wages.columns:
    plt.plot(wage_years, wages[column], label=column)

plt.xlabel('Year')
plt.ylabel('Wages')
plt.title('Wages over the Years (2000 - 2022)')
plt.legend()
plt.grid(True)
plt.xlim(2000, 2022)  
plt.ylim(0, 100)
plt.xticks(range(2000, 2022, 2))
#plt.show()

# Making Table
statistics_per_column = {}
for column in wages_noYear.columns:
    min_value = wages_noYear[column].min()
    max_value = wages_noYear[column].max()
    yearly_change = wages_noYear[column].diff().mean()
    wage_total_percent_increase = ((max_value - min_value) / min_value) * 100 if min_value != 0 else 0
    yearly_change_percent = ((yearly_change/min_value) * 100)

    statistics_per_column[column] = {
        'Min': round(min_value, 2),
        'Max': round(max_value, 2),
        'Average Change Over Year': round(yearly_change, 2),
        'Average Percent Change Over Year':f"{round(yearly_change_percent, 2)}%",
        'Total Percent Increase': f"{round(wage_total_percent_increase, 2)}%"
    }

statistics_df = pd.DataFrame.from_dict(statistics_per_column, orient='columns')
print(statistics_df)

# Plotting line graph 2 
CPI['date'] = pd.to_datetime(CPI['date'])

plt.figure(figsize=(10, 6))
plt.plot(CPI['date'], CPI['value'], marker='o', linestyle='-')

plt.xlabel('Date')
plt.ylabel('CPI Value')
plt.title('Changes in CPI over Time (January 2000 - December 2022)')
plt.grid(True)
plt.xticks(rotation=45)  # Rotate x axis
plt.grid(True)
plt.xlim(pd.Timestamp('2000-01-01'), pd.Timestamp('2022-12-31'))
plt.ylim(0, 400)
#plt.show()

# Calculate statistics
CPI['yearly_change'] = CPI['value'].diff() 
average_change = CPI['yearly_change'].mean() 
average_change = average_change * 12
min_value = CPI['value'].min()
max_value = CPI['value'].max()
total_change_percent = ((max_value - min_value) / min_value) * 100
CPI_yearly_change_percent = ((average_change/min_value) * 100)


statistics_table2 = {
    'Min': round(CPI['value'].min(), 2),
    'Max': round(CPI['value'].max(), 2),
    'Average Change Over Year': round(average_change, 2),
    'Average Percent Change Over Year':f"{round(CPI_yearly_change_percent, 2)}%",
    "Total Percent Increase" : f"{round(total_change_percent)}%"

}

# Table
table2 = pd.DataFrame.from_dict(statistics_table2, orient='index', columns=['Values'])
print(table2)


# Merging data
CPI['date'] = pd.to_datetime(CPI['date'])
CPI_yearly = CPI.groupby(CPI['date'].dt.year).first()
CPI_yearly.index.name = 'year'
CPI_yearly.reset_index(inplace=True)

CPI_values = CPI_yearly['value']
wages_with_CPI = wages.join(CPI_values, how='inner')
wages_with_CPI['value'] = wages_with_CPI['value'].iloc[::-1]

# Calculate the percentage diff
wages_with_CPI['value'] = wages_with_CPI['value'].values[::-1]
wages_with_CPI = wages_with_CPI.rename(columns={'value': 'CPI'})

# Calculate the percentage diff
percentage_diff = wages_with_CPI.drop('year', axis=1).apply(lambda x: ((x - x.min()) / x.min()) * 100)

plt.figure(figsize=(8, 6))

# Plotting the percentage difference for each column
for column in percentage_diff.columns:
    if column != 'year':  
        plt.plot(wages_with_CPI['year'], percentage_diff[column], label=column)

plt.xlabel('Year')
plt.ylabel('% Difference from Minimum')
plt.title('Percentage Difference from Minimum Value by Year')
plt.ylim(0, 100)
plt.xlim(2000, 2022)
plt.legend()
plt.grid(True)
#plt.show()


columns_to_multiply = ['less_than_hs', 'high_school', 'some_college', 'bachelors_degree', 'advanced_degree']

# Multiplying selected columns by 2000
wages_with_CPI[columns_to_multiply] *= 2000

wagesYear = wages_with_CPI.join(CPI_values, how='inner')

# Dividing wage columns by 'CPI'
wagesYear_normalized = wagesYear[columns_to_multiply].div(wagesYear['value'], axis=0)

plt.figure(figsize=(8, 6))

for column in wagesYear_normalized.columns:
    plt.plot(wagesYear.index, wagesYear_normalized[column], label=column)

plt.xlabel('Year')
plt.ylabel('Normalized Values')
plt.title('Normalized Wages Over Time')
plt.xlim(0, 22)
plt.legend()
plt.grid(True)
plt.show()

statistics_per_column = {}
for column in wagesYear_normalized.columns:
    min_value = wagesYear_normalized[column].min()
    max_value = wagesYear_normalized[column].max()
    yearly_change = wagesYear_normalized[column].diff().mean()
    wage_total_percent_increase = ((max_value - min_value) / min_value) * 100 if min_value != 0 else 0
    yearly_change_percent = ((yearly_change/min_value) * 100)

    statistics_per_column[column] = {
        'Min': round(min_value, 2),
        'Max': round(max_value, 2),
        'Average Change Over Year': round(yearly_change, 2),
        'Average Percent Change Over Year':f"{round(yearly_change_percent, 2)}%",
        'Total Percent Change': f"{round(wage_total_percent_increase, 2)}%"
    }

statistics_df = pd.DataFrame.from_dict(statistics_per_column, orient='columns')
print(statistics_df)
