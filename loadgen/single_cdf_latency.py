#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
import os

concurrency_levels = [10, 50, 100, 200, 500, 1000]  # Adjust the concurrency levels as needed
line_styles = ['--', '-', ':', ':']
markers = ['P', 'd', '*', 'x'] 
# endpoints = ['cpu', 'infer']
endpoints = ['cpu']
max_value = 10000
directory = '/home/cc/anish/faas-inference/results/server'

# Create a single plot for all concurrency levels
fig, ax = plt.subplots()
ax.set_title('CDF vs. Latency')
ax.set_xlabel('Latency (ms)')
ax.set_ylabel('Percentage (%)')

# Loop over each concurrency level

for i, concurrency in enumerate(concurrency_levels):
    # Loop over each endpoint
    for endpoint in endpoints:
        # Load the data from the CSV file into a NumPy array
        filename = f'data_{endpoint}_concurrency_{concurrency}.csv'
        filename = os.path.join(directory, filename)
        data = np.genfromtxt(filename, delimiter=',', names=['percentage', 'time_ms'], skip_header=1)

        # Clean the data and convert abnormal values
        cleaned_data = np.copy(data)
        last_valid_value = data['time_ms'][0]
        for j in range(1, len(cleaned_data)):
            if cleaned_data['time_ms'][j] > max_value:
                cleaned_data['time_ms'][j] = last_valid_value
            else:
                last_valid_value = cleaned_data['time_ms'][j]

        # Sort the data by time in ascending order
        cleaned_data = np.sort(cleaned_data, order='time_ms')

        # Calculate the empirical CDF
        ecdf = ECDF(cleaned_data['time_ms'])

        # Set different line style and color for each concurrency level
        line_style = line_styles[i % len(line_styles)]
        line_color = 'g' if endpoint == 'cpu' else 'r'
        marker = markers[i % len(markers)]

        # Plot the ECDF with different line style and color
        ax.plot(ecdf.x, ecdf.y, label=f'{endpoint.upper()} (Concurrency: {concurrency})', linestyle=line_style, marker=marker, color=line_color,markevery=25)

# Set the y-axis tick locations and labels
yticks = [0, 0.25, 0.5, 0.75, 1]
ax.set_yticks(yticks)
ax.set_yticklabels([str(ytick) for ytick in yticks])

# Add a legend
ax.legend(fontsize="5", loc ="lower right")
save_file = 'cdf_distribution.png'
# Save the plot as a PNG file
plt.savefig(os.path.join(directory, save_file))

# Show the plot
plt.show()
