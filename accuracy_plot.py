import matplotlib.pyplot as plt
import numpy as np

# Given data
fos_values = np.array([1.0, 2.0, 2.5, 4.0, 5.0])  # Factor of Safety (x-axis)
agent_diameters = np.array([8.625, 23.5, 10.5, 22, 16.6])  # Agent generated diameters (y-axis)
calculated_diameters = np.array([8.6, 23.5, 10.8, 22.02, 16.6])  # Your calculated diameters (y-axis)

# Compute the absolute difference for error bars
diff = np.abs(agent_diameters - calculated_diameters)

# --- ERROR BAR PLOT ---
plt.figure(figsize=(8, 6))

plt.errorbar(fos_values, calculated_diameters, yerr=diff, fmt='s', capsize=5, color='red', alpha=0.7, label='Calculated Diameter (Error Bars)')
plt.plot(fos_values, agent_diameters, marker='o', linestyle='-', label='Agent Generated Diameter', color='blue')
plt.plot(fos_values, calculated_diameters, marker='s', linestyle='--', label='Calculated Diameter', color='red')

# Labels and title
plt.xlabel('Factor of Safety')
plt.ylabel('Diameter')
plt.title('Comparison of Agent vs. Calculated Diameters (Error Bars)')

# Show legend
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig("diameter_vs_fos_errorbars_precise.png", dpi=300, bbox_inches='tight')

# Show plot
plt.show()

# --- SIDE-BY-SIDE BAR CHART ---
bar_width = 0.3
x_indices = np.arange(len(fos_values))

plt.figure(figsize=(8, 6))

# Bar chart for comparison
bars1 = plt.bar(x_indices - bar_width / 2, agent_diameters, bar_width, label='Agent Generated Diameter', color='blue', alpha=0.7)
bars2 = plt.bar(x_indices + bar_width / 2, calculated_diameters, bar_width, label='Calculated Diameter', color='red', alpha=0.7)

# Annotate differences on bars
for i in range(len(fos_values)):
    diff_value = round(agent_diameters[i] - calculated_diameters[i], 3)
    plt.text(x_indices[i], max(agent_diameters[i], calculated_diameters[i]) + 0.5, f"Δ={diff_value}", ha='center', fontsize=10, fontweight='bold')

# Labels and title
plt.xlabel('Factor of Safety')
plt.ylabel('Diameter')
plt.title('Bar Chart Comparison of Diameters with Differences')
plt.xticks(x_indices, fos_values)  # Set x-axis labels to fos_values

# Show legend
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Save the plot
plt.savefig("diameter_vs_fos_barplot_precise.png", dpi=300, bbox_inches='tight')

# Show plot
plt.show()
