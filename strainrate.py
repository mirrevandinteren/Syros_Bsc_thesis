import numpy as np
import matplotlib.pyplot as plt

# Define RGB triplets for custom colors
brown = [0.6, 0.3, 0]
gold = [1, 0.84, 0]
magenta = [1, 0, 1]
cyan = [0, 1, 1]

# Constants
R = 8.3144  # Universal gas constant [J/(mol*K)]
T = np.arange(200, 701, 50) + 273  # Temperature [K] from 200 to 650 degrees C
TC = T - 273  # Temperature [C]
geotherm = 10  # Geothermal gradient [degrees C/km]
rho = 2700  # Average crustal density [kg/m^3]
g = 9.8  # Acceleration due to gravity [m/s^2]

# Calculating depth and pressure
h = TC / geotherm * 1e3  # Depth [m]
P = rho * g * h / 1e9  # Pressure [GPa]

# Water fugacity data (FH2O) from UMN water fugacity calculator
FH2O = 1e3 * np.array([0.203, 0.469, 0.944, 1.758, 2.923, 4.545, 6.692, 9.627,
                       13.045, 17.134, 22.326, 27.902, 34.204, 41.233, 49.743])  # 10°C/km

# Fugacity interpolation
v = FH2O
xq = np.linspace(1, len(v), len(T))
fH2O = np.interp(xq, np.arange(1, len(v) + 1), v)

# Material constants for flow law calculation
n = 4  # Stress exponent
A = 10**-11.2  # Pre-exponential constant
Q = 1.35e5  # Activation energy [J/mol]
d = 10  # Grain size [microns]
m = 0  # Grain size exponent
fn = 1  # Water fugacity exponent

# Strain rates to be plotted
strain_rates = [1e-9, 1e-10, 1e-11, 1e-12, 1e-13, 1e-14, 1e-15]

# Plotting flow laws for different strain rates
plt.figure(1)

for E in strain_rates:
    flowcurve = (d**m * (E / (A * fH2O**fn * np.exp(-Q / (R * T))))**(1 / n))
    plt.plot(flowcurve, TC, 'k')


# Plot settings
plt.xlim([0, 100])
plt.ylim([650, 200])
plt.xlabel('Stress (MPa)', fontsize=14)
plt.ylabel('Temperature (°C)', fontsize=14)
plt.gca().xaxis.tick_top()
plt.gca().xaxis.set_label_position('top') 
plt.title('Quartz dislocation creep strain rates by Hirth et al. (2001) \nwith all samples plotted for their temperatures and stress estimates', fontsize=19, pad=20)

plt.tight_layout(rect=[0, 0, 1, 1])

# Datapoint coordinates
data_points = [
    (500, 36, 50, 26, gold, 'KCS74'),
    (450, 37, 50, 27, brown, 'KCS45A'),
    (420, 28, 50, 21, magenta, 'KCS23'),
    (400, 33, 50, 24, cyan, 'KCS3')
]

# Plotting the datapoints with error bars
for x, y, xerr, yerr, color, label in data_points:
    plt.errorbar(y, x, xerr=yerr, yerr=xerr, fmt='s', color=color, markersize=7, markerfacecolor=color, label=label)

# Show legend
plt.legend()

# Show the plot
plt.show()
