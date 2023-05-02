#!/usr/bin/env python3

'''
ab -n 100 -c 100 -e data.csv -p payload.json -T "application/json" http://10.52.0.189:5000/serve
'''

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF

# Load the data from the CSV file into a NumPy array
data = np.genfromtxt('data.csv', delimiter=',', names=['percentage', 'time_ms'], skip_header=1)

# Sort the data by time in ascending order
data = np.sort(data, order='time_ms')

# Calculate the empirical CDF
ecdf = ECDF(data['time_ms'])

# Create the plot
fig, ax = plt.subplots()
ax.plot(ecdf.x, ecdf.y)

# Set the y-axis tick locations and labels
yticks = [0, 0.25, 0.5, 0.75, 1]
ax.set_yticks(yticks)
ax.set_yticklabels([str(ytick) for ytick in yticks])

# Set the plot title and axis labels
ax.set_title('CDF vs. Latency')
ax.set_xlabel('Latency (ms)')
ax.set_ylabel('Percentage (%)')

# Save the plot as a PNG file
plt.savefig('cdf_distribution.png')