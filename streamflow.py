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
    dates_str = [str(d).split(' ')[0] for d in streamflow_data[date_col_name]]

    # Display sample rows to confirm correctly parsed arrays
    print("First 5 elements of x:", x[:5])
    print(f"{cols[1]} (y_1):", y_1[:5])

    return x, y_1, y_2, y_3, y_4, y_5, dates_str


def plot_streamflow(x, y_1, y_2, y_3, y_4, y_5, dates_str):
    """Plot the flow at each gauge, with the same title, labels, and formatting as the Matplotlib HW."""
    plt.figure(figsize=(10, 6))

    # Plot the 5 sites with their raw numeric labels
    plt.plot(x, y_1, label='10163000', linewidth=1.5)
    plt.plot(x, y_2, label='10155200', linewidth=1.5)
    plt.plot(x, y_3, label='10155500', linewidth=1.5)
    plt.plot(x, y_4, label='10154200', linewidth=1.5)
    plt.plot(x, y_5, label='10155000', linewidth=1.5)

    # Add graph titles and axis labels
    plt.title('Provo River Streamflow Data (2021)')
    plt.xlabel('Date')
    plt.ylabel('Flowrate (cfs)')

    # Configure custom ticks representing specific target dates
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

    # Find the index in the dataset closest to each target date
    for td in target_dates:
        for idx, d_str in enumerate(dates_str):
            if d_str == td:
                tick_indices.append(idx)
                tick_labels.append(td)
                break

    # Set custom ticks with rotation and alignment
    if len(tick_indices) > 0:
        plt.xticks(tick_indices, tick_labels, rotation=35, ha='right')

    # Finish configuration with a styled legend, grid, and layout adjustment
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Site Numbers', loc='best')
    plt.tight_layout()
    plt.savefig("provo_streamflow.png", dpi=150, bbox_inches="tight")
    plt.show()


# Main section
if __name__ == "__main__":
    csv_file = 'June-2021-Provo-River-Streamflow-Rates.csv'
    x, y_1, y_2, y_3, y_4, y_5, dates_str = load_streamflow(csv_file)
    plot_streamflow(x, y_1, y_2, y_3, y_4, y_5, dates_str)