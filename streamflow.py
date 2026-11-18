# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def load_streamflow(filename):
    """Read the streamflow CSV. Return the dates and a 2D array of flows (cfs), one column per gauge."""
    streamflow_data = np.genfromtxt(
        filename, delimiter=',', dtype=None, encoding='utf-8', names=True
    )

    # Here, we inspect the columns to map the exact field names.
    cols = streamflow_data.dtype.names
    print("Detected column names:", cols)

    # Here, we map the columns to specified variables.
    x = np.arange(len(streamflow_data))  # x representing chronological intervals
    y_1 = streamflow_data[cols[1]]       # Site 10163000
    y_2 = streamflow_data[cols[2]]       # Site 10155200
    y_3 = streamflow_data[cols[3]]       # Site 10155500
    y_4 = streamflow_data[cols[4]]       # Site 10154200
    y_5 = streamflow_data[cols[5]]       # Site 10155000

    # Then, we extract the date strings for custom tick formatting
    date_col_name = cols[0]
    full_dates = [str(d) for d in streamflow_data[date_col_name]]
    dates_str = [d.split(' ')[0] for d in full_dates]

    # Next, we display the sample rows to confirm the data extracted correctly.
    print("First 5 elements of x:", x[:5])
    print(f"{cols[1]} (y_1):", y_1[:5])

    return x, y_1, y_2, y_3, y_4, y_5, dates_str, full_dates


def plot_streamflow(x, y_1, y_2, y_3, y_4, y_5, dates_str):
    """Plot the flow at each gauge, with the same title, labels, and formatting as the Matplotlib HW."""
    plt.figure(figsize=(10, 6))

    # This is where we actually plot the 5 sites with their respective labels and line (from previous homework).
    plt.plot(x, y_1, label='10163000', linewidth=1.5)
    plt.plot(x, y_2, label='10155200', linewidth=1.5)
    plt.plot(x, y_3, label='10155500', linewidth=1.5)
    plt.plot(x, y_4, label='10154200', linewidth=1.5)
    plt.plot(x, y_5, label='10155000', linewidth=1.5)

    # Then, we add graph titles and axis labels.
    plt.title('Provo River Streamflow Data (2021)')
    plt.xlabel('Date')
    plt.ylabel('Flowrate (cfs)')

    # Below, we make sure the each specific date is represented in the plot.
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

    # Next, just like in the last homework, we find the index in the dataset closest to each target date.
    for td in target_dates:
        for idx, d_str in enumerate(dates_str):
            if d_str == td:
                tick_indices.append(idx)
                tick_labels.append(td)
                break

    # Then, we set custom ticks with rotation and alignment (same as old homework).
    if len(tick_indices) > 0:
        plt.xticks(tick_indices, tick_labels, rotation=35, ha='right')

    # Finally, we finish our configuration with a styled legend, grid, and layout adjustment.
    # Additionally, we include the new "plt.savefig" command to save the figure as a PNG file.
    # We put the save BEFORE plt.show because plt.show clears and resets the displayed figure from memory once the window closes.
    # This means there's nothing to save after the window closes, so we put in plt.savefig first.
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Site Numbers', loc='best')
    plt.tight_layout()
    plt.savefig("provo_streamflow.png", dpi=150, bbox_inches="tight")
    plt.show()

# AI really helped me with this function. I got as far as I could get myself, but then I had it help me with some formatting and math.
def summarize(dates, flows, sites):
    """Summarize the streamflow data for each site."""
    # First, we will print the column headers for the summary table. 
    print()
    # The "<10", ">10", and "<18" are formatting specifiers to align the text in columns. These were an AI suggestion.
    print(f"{'Guage':<10} {'Max (cfs)':>10} {'Date of max':<18} {'Min (cfs)':>10} {'Avg (cfs)':>10}")

    # Next we will open a new CSV file and write the header row.
    file = open("streamflow_summary.csv", "w")
    file.write("Guage,Max (cfs),Date of max,Min (cfs),Avg (cfs)\n")

    # We are going to loop through each of the different 5 guages one by one.
    # The [i] will help us out with that, as it is the index of the current guage we are working with.
    # The index part was AI's idea.
    for i in range(len(sites)):
        site_name = sites[i]
        site_flow = flows[i]

        # This is where we have Numpy do the math for us.
        # The "argmax" (a suggestion givin by AI) is finding WHERE the max value is in the index rather than just what the max value is.
        max_flow = np.max(site_flow)
        max_row = np.argmax(site_flow)
        max_date = dates[max_row]
        min_flow = np.min(site_flow)
        avg_flow = np.mean(site_flow)

        # Now, we print the guage's row to the terminal, using the same formatting as we did before.
        print(f"{site_name:<10} {max_flow:>10.1f} {max_date:<18} {min_flow:>10.2f} {avg_flow:>10.1f}")

        # Finally, we write the gauge's row to the CSV file.
        file.write(f"{site_name},{max_flow:.1f},{max_date},{min_flow:.1f},{avg_flow:.1f}\n")

    # Always close the file.
    file.close()

# I was having trouble getting the figure to display, then I forgot that I needed to call the functions to load the data and plot it.
#  So, I had AI help me with the added lines below to call the functions and display the plot.
csv_file = 'June-2021-Provo-River-Streamflow-Rates.csv'
x, y_1, y_2, y_3, y_4, y_5, dates_str, full_dates = load_streamflow(csv_file)

sites = ['10163000', '10155200', '10155500', '10154200', '10155000']
flows = [y_1, y_2, y_3, y_4, y_5]
summarize(full_dates, flows, sites)

# This is where we ask the user for a flow threshold, as asked for in the HW.
# First, we make a simple input prompt that the user can use to give us a threshold value.
threshold = float(input("\nEnter a flow threshold (cfs): "))
print(f"\nHours above {threshold} cfs in June 2021:")

# Next, we loop through each site and calculate the number of hours above the threshold.
# AI suggested I use the "np.sum" function because it is a more efficient way to count the number of True values in a boolean array.
for i in range(len(sites)):
    site_name = sites[i]
    site_flow = flows[i]
    hours_above = np.sum(site_flow > threshold) * 0.25
    print(f"Gauge {site_name}: {hours_above:.2f} hours")

plot_streamflow(x, y_1, y_2, y_3, y_4, y_5, dates_str)

# READ BELOW FIRST:
# I forgot to commit when I organized everything into functions, so here is a comment saying that I committed the code.
# That's why the commits will be out of order. I will make sure to commit effectively in the future.