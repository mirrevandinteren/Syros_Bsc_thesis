import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your dataset
data = pd.read_csv('stress_table_complete.csv')

# Define colors for samples
color_dict = {
    'KCS3': 'cyan', 
    'KCS23': 'magenta', 
    'KCS45A': 'brown', 
    'KCS74': 'gold'
}

# Define a marker dictionary for the equations
marker_dict = {
    'Stipp&Tullis': 'o',  
    'Cross (sliding res.)': '^',
    'Cross (micrometer res.)': 'v'      
}

# Define color for error bars
error_color_dict = {
    'Manual':'black',
    'Automated':'grey'
}

plt.figure(figsize=(10, 8))

# Initialize a list for legend handles, ensuring order by first adding samples
legend = [mpatches.Patch(color=color, label=sample) for sample, color in color_dict.items()]

# Collect equations for legend after samples to ensure correct order
equations_added = set()
for (method, equation, sample), group_data in data.groupby(['Method', 'Equation', 'Sample']):
    if equation not in equations_added:
        legend.append(plt.Line2D([0], [0], color='black', marker=marker_dict[equation], label=equation, markersize=10, linestyle='None'))
        equations_added.add(equation)

# Scatter plot generation with error bars for grain size and stress
for (method, equation, sample), group_data in data.groupby(['Method', 'Equation', 'Sample']):
    edge_color = color_dict[sample]
    face_color = 'none' if method == 'Automated' else color_dict[sample]
    ecolor =  error_color_dict[method] if method in error_color_dict else 'gray' 
    # Plot the points
    plt.errorbar(group_data['GrainSize'], group_data['Stress_cor'],
                 fmt=marker_dict[equation],
                 markersize=10,
                 markerfacecolor=face_color,
                 markeredgecolor=edge_color,
                 markeredgewidth=2,
                 linestyle='None')  # Only markers, no line

    # Plot the error bars
    plt.errorbar(group_data['GrainSize'], group_data['Stress_cor'],
                 xerr=group_data['Std_GrainSize'],
                 yerr=group_data['Std_Stress_cor'],
                 fmt='None',  # No markers, only error bars
                 ecolor=ecolor,
                 elinewidth=0.5,
                 capsize=4) 


# Adding MLI and GOS method explanations to legend
legend.append(plt.Line2D([0], [0], color='grey', marker='s', markersize=10, linestyle='None', markerfacecolor='grey', label='MLI method'))
legend.append(plt.Line2D([0], [0], color='grey', marker='s', markersize=10, linestyle='None', markerfacecolor='none', label='GOS method'))
legend.append(plt.Line2D([0], [0], color='grey', linestyle='solid', label='Half of the RMS'))
legend.append(plt.Line2D([0], [0], color='black', linestyle='solid', label='Standard deviation'))

# Adding titles and labels
plt.title('Stress vs GrainSize \nby multiple measurement methods and piezometers', fontsize=19)
plt.xlabel('GrainSize (μm)', fontsize=14)
plt.ylabel('Stress (MPa)', fontsize=14)
plt.xlim(0,180)
plt.ylim(0,80)

# Create the legend with the handles
plt.legend(handles=legend, loc='best', fontsize=10)

# Show the plot
plt.show()