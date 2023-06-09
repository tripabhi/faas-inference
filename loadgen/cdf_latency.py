#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF

concurrency_levels = [5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Adjust the concurrency levels as needed
endpoints = ['cpu', 'infer']
max_value = 10000

# Loop over each concurrency level
for concurrency in concurrency_levels:
    # Create a subplot for the current concurrency level
    fig, ax = plt.subplots()
    ax.set_title(f'CDF vs. Latency (Concurrency: {concurrency})')
    ax.set_xlabel('Latency (ms)')
    ax.set_ylabel('Percentage (%)')

    # Loop over each endpoint
    for endpoint in endpoints:
        # Load the data from the CSV file into a NumPy array
        filename = f'data_{endpoint}_concurrency_{concurrency}.csv'
        data = np.genfromtxt(filename, delimiter=',', names=['percentage', 'time_ms'], skip_header=1)

        # Clean the data and convert abnormal values
        cleaned_data = np.copy(data)
        last_valid_value = data['time_ms'][0]
        for i in range(1, len(cleaned_data)):
            if cleaned_data['time_ms'][i] > max_value:
                cleaned_data['time_ms'][i] = last_valid_value
            else:
                last_valid_value = cleaned_data['time_ms'][i]

        # Sort the data by time in ascending order
        cleaned_data = np.sort(cleaned_data, order='time_ms')

        # Calculate the empirical CDF
        ecdf = ECDF(cleaned_data['time_ms'])

        # Plot the ECDF
        ax.plot(ecdf.x, ecdf.y, label=endpoint.upper())

    # Set the y-axis tick locations and labels
    yticks = [0, 0.25, 0.5, 0.75, 1]
    ax.set_yticks(yticks)
    ax.set_yticklabels([str(ytick) for ytick in yticks])

    # Add a legend
    ax.legend()

    # Save the plot as a PNG file
    plt.savefig(f'cdf_distribution_concurrency_{concurrency}.png')

    # Show the plot (optional)
    plt.show()
