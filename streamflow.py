# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

import numpy as np
import matplotlib.pyplot as plt

# Below is the same step from before, the one AI helped me with.
streamflow_data = np.genfromtxt('June-2021-Provo-River-Streamflow-Rates.csv', delimiter=',', dtype=None, encoding='utf-8', names=True)

# Next, we will inspect columns to map the exact field names.
print("Detected column names:", streamflow_data.dtype.names)

# Then, we will map columns to specified variables.
cols = streamflow_data.dtype.names
x = np.arange(len(streamflow_data))  # x representing chronological intervals/days
y_1 = streamflow_data[cols[1]]       # Site 10163000
y_2 = streamflow_data[cols[2]]       # Site 10155200
y_3 = streamflow_data[cols[3]]       # Site 10155500
y_4 = streamflow_data[cols[4]]       # Site 10154200
y_5 = streamflow_data[cols[5]]       # Site 10155000

# Finally, we will display sample rows to confirm correctly parsed arrays.
print("First 5 elements of x:", x[:5])
print(f"{cols[1]} (y_1):", y_1[:5])

# Below we will graph the Provo River Streamflow Data.
plt.figure(figsize=(10, 6))

# We will then plot the 5 sites with their raw numeric labels.
plt.plot(x, y_1, label='10163000', linewidth=1.5)
plt.plot(x, y_2, label='10155200', linewidth=1.5)
plt.plot(x, y_3, label='10155500', linewidth=1.5)
plt.plot(x, y_4, label='10154200', linewidth=1.5)
plt.plot(x, y_5, label='10155000', linewidth=1.5)

# Below we will add graph titles and axis labels.
plt.title('Provo River Streamflow Data (2021)')
plt.xlabel('Date')
plt.ylabel('Flowrate (cfs)')

# After that, we will configure custom ticks representing specific dates requested by the user.
date_col_name = streamflow_data.dtype.names[0]
dates_str = [str(d).split(' ')[0] for d in streamflow_data[date_col_name]]

target_dates = [
    '2021-06-01',
    '2021-06-05',
    '2021-06-09',
    '2021-06-13',
    '2021-06-17',
    '2021-06-21',
    '2021-06-25',
    '2021-06-29',
    '2021-07-01'
]

tick_indices = []
tick_labels = []

# This is how we will find the index in our dataset closest to each of the target dates.
for td in target_dates:
    for idx, d_str in enumerate(dates_str):
        if d_str == td:
            tick_indices.append(idx)
            tick_labels.append(td)
            break

# Next, we will set the custom ticks with rotation and alignment.
if len(tick_indices) > 0:
    plt.xticks(tick_indices, tick_labels, rotation=35, ha='right')

# Finally, we will finish configuration with a styled legend, grid, and layout adjustment.
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Site Numbers', loc='best')
plt.tight_layout()
plt.show()