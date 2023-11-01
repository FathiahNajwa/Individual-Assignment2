import requests
import json
import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from pprint import pprint
from matplotlib.ticker import FuncFormatter



# Define the base URL and headers if needed
base_url = 'https://api.bnm.gov.my/public/payment-statistic/03-cards/year/'
headers = {
    "Accept": "application/vnd.BNM.API.v1+json"  # Replace with your access token or API key if required
}

# Define the range of years you want to extract data for
current_date = datetime.now()
start_year = 2021
end_year = 2022  # Replace with the desired end year
data_list = []

# Iterate through the range of years
for year in range(start_year, end_year + 1):
    api_url = f'{base_url}{year}'

    # Make the GET request
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        data_list.append(data)
    else:
        print(f'Error for {year}: {response.status_code} - {response.text}')

pprint(data_list)

json_data = data_list

# Extract the 'data' part for time series
data_list = [item['data'] for item in json_data]

# Flatten the list of dictionaries
flat_data_list = [entry for sublist in data_list for entry in sublist]

# Create a DataFrame
df = pd.DataFrame(flat_data_list)

# Convert 'month_dt' column to datetime type
#df['month_dt'] = pd.to_datetime(df['month_dt'], format='%m')

# Sort the DataFrame by 'month_dt' in ascending order
df.sort_values(by='month_dt', inplace=True)

# Set 'month_dt' column as the index
df.set_index('month_dt', inplace=True)

# Print multiple columns
print(df[['cre_crd_tot', 'deb_crd_tot', 'emon_tot']])

# Extract relevant data for plotting
months = df.index
values1 = df['cre_crd_tot']
values2 = df['deb_crd_tot']
values3 = df['emon_tot']

# Create subplots
fig, ax = plt.subplots()

# Set the bar width
bar_width = 0.2

# Create horizontal bars for the first set of data (Total Card Credit)
bar1 = ax.barh(np.arange(len(months)), values1, bar_width, label='Total Card Credit', color='b')

# Create horizontal bars for the second set of data (Total Debit Card)
bar2 = ax.barh(np.arange(len(months)) + bar_width, values2, bar_width, label='Total Debit Card', color='g')

# Create horizontal bars for the third set of data (Total E-Money)
bar3 = ax.barh(np.arange(len(months)) + 2 * bar_width, values3, bar_width, label='Total E-Money', color='r')

# Set labels for the x and y axes
ax.set_yticks(np.arange(len(months)))
ax.set_yticklabels(months)

# Add a legend
ax.legend()

# Format the values on the horizontal bars to display two decimal points
#ax.xaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))

# Define a custom formatter function
#def thousands_formatter(x, pos):
 #   if x < 1e3:
    #      return int(x)
  #  elif x < 1e6:
#     return f'{int(x / 1e3)}k'
 #   else:
  #      return f'{int(x / 1e6)}M'


# Set the custom formatter for the x-axis
#ax.xaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Set a title for the chart
plt.title('Type of Payment Methods by Month')

# Save the chart to an image file (e.g., PNG)
plt.savefig('type_of_payment_methods_by_month.png')

# Display the horizontal bar chart
plt.show()
