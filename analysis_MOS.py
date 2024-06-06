import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def find_elbow(data, theta):
    # make rotation matrix
    co = np.cos(theta)
    si = np.sin(theta)
    rotation_matrix = np.array(((co, -si), (si, co)))

    # rotate data vector
    rotated_vector = np.dot(data, rotation_matrix)

    # return index of elbow, which is the minimum of the y-values in rotated data
    return np.argmin(rotated_vector[:, 1])

def get_data_radiant(data):
    # Calculate the radiant for data rotation based on the data's bounding box diagonal
    return np.arctan2(data[:, 1].max() - data[:, 1].min(), 
                      data[:, 0].max() - data[:, 0].min())

# Load the CSV file
data_path = 'KCS74_Grainlist.csv'
data = pd.read_csv(data_path)

# Sort the data by Mean_Orientation_Spread and convert to numpy array for processing
data_sorted = np.column_stack((np.arange(len(data)), data['Mean Orientation Spread'].sort_values()))

# Get the radiant for rotation
theta = get_data_radiant(data_sorted)

# Get the point of maximum curvature (elbow)
elbow_index = find_elbow(data_sorted, theta)

# Plotting
plt.figure(figsize=(10, 6))
plt.xlim(0,16000)
plt.ylim(0,15)
plt.plot(data_sorted[:, 0], data_sorted[:, 1], marker='o', markersize=2, color='cyan')
plt.plot([data_sorted[0, 0], data_sorted[-1, 0]], [data_sorted[0, 1], data_sorted[-1, 1]], 'k-', linewidth=0.5, label='Line from first to last')
plt.scatter(data_sorted[elbow_index, 0], data_sorted[elbow_index, 1], marker='x', color='red', zorder=3)  # Mark the elbow point

# Annotate the MOS value at the elbow point
mos_value = data_sorted[elbow_index, 1]
plt.annotate(f'threshold: {mos_value:.2f}°', (data_sorted[elbow_index, 0], mos_value),
             textcoords="offset points", xytext=(0,10), ha='left', color='red')
# Add a horizontal line through the elbow point
plt.plot([data_sorted[:, 0].min(), data_sorted[elbow_index, 0]], [mos_value, mos_value], 
         color='green', linestyle='--', label='Horizontal at Elbow')

plt.title('Cumulative Grains vs Mean Orientation Spread KCS74')
plt.xlabel('Cumulative Number of Grains')
plt.ylabel('Mean Orientation Spread (°)')
plt.grid(True)
plt.show()

# Calculating the average grainsize by AZtecCrystal
data_KCS23 = pd.read_csv('KCS23_Grainlist.csv')
average_grainsize_KCS23 = data_KCS23['Equivalent Circle Diameter'].mean()
data_KCS45A = pd.read_csv('KCS45A_Grainlist.csv')
average_grainsize_KCS45A = data_KCS45A['Equivalent Circle Diameter'].mean()
data_KCS74 = pd.read_csv('KCS74_Grainlist.csv')
average_grainsize_KCS74 = data_KCS74['Equivalent Circle Diameter'].mean()
data_KCS3 = pd.read_csv('KCS3_Grainlist2.csv')
average_grainsize_KCS3 = data_KCS3['Equivalent Circle Diameter'].mean()

print(f"Average grainsizes; KCS3: {average_grainsize_KCS3}, KCS23: {average_grainsize_KCS23}, KCS45A: {average_grainsize_KCS45A}, KCS74: {average_grainsize_KCS74}.")