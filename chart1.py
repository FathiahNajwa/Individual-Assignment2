import requests
import json
import numpy as np
from datetime import datetime
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt

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
        #data = response.json()
        # Process and print the data for the current year
         # Parse the JSON response
        data = json.loads(response.text)

        # Append the data to the list
        data_list.append(data)
        
        
    else:
        print(f'Error for {year}: {response.status_code} - {response.text}')

pprint(data_list)

json_data=data_list

# Extract the 'data' part for time series
data_list = [item['data'] for item in json_data]

# Flatten the list of dictionaries
flat_data_list = [entry for sublist in data_list for entry in sublist]

# Create a DataFrame
df = pd.DataFrame(flat_data_list)


# Sort the DataFrame by 'date' in ascending order
df.sort_values(by='year_dt', inplace=True)

# Set 'date' column as the index
df.set_index('month_dt', inplace=True)
# Print multiple columns
print(df[[ 'cre_crd_crds_appl', 'cre_crd_crds_appr']])


applications = df['cre_crd_crds_appl']
approved = df ['cre_crd_crds_appr']
month = df.index

bar_width = 0.35

# Create an array of positions for the bars
x = np.arange(len(month))


plt.figure(figsize=(12, 6))



# Create the figure and axis
fig, ax = plt.subplots()

# Create the bar chart for applications
bar1 = ax.bar(x - bar_width/2, applications, bar_width, label='Applications')

# Create the bar chart for approvals
bar2 = ax.bar(x + bar_width/2, approved, bar_width, label='Approvals')
# Customize the plot

ax.set_xlabel('Month')
ax.set_ylabel('Count')
ax.set_title('Credit Card Applications vs. Approvals by Month')
ax.set_xticks(x)
ax.set_xticklabels(month)
ax.legend()

# Save the chart to an image file (e.g., PNG)
plt.savefig('Credit_Card_Applications-Approvals_by_Month.png')

plt.show()