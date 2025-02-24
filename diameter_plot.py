import numpy as np
import matplotlib.pyplot as plt

# Example Data (Simulated Iterative Results)
iterations = np.arange(1, 7)  # Iteration count
dia_0 = np.array([10,9.5,9.0,8.5,8.0,7.5,7.0])
fos_0 = np.array([2.34,2.08,1.84,1.62,1.41,1.21,1.03])

dia_1 = np.array([10.5,11.0,11.5,11.25,11.3,11.35,11.4,11.45])
fos_1 = np.array([2.04,2.28,2.52,2.40,2.42,2.45,2.47,2.50])

dia_2 = np.array([10.5,11,12,13.25,14,15,16,15.5,15.25,15.15,15.10,15.05,15,14.95,14.90,14.85,14.80,14.75,14.70,14.65,14.60,14.55])
fos_2 = np.array([1.04,1.31,1.60,1.93,2.29,2.67,3.09,2.88,2.78,2.73,2.71,2.69,2.67,2.65,2.63,2.61,2.59,2.57,2.55,2.53,2.52,2.50])

dia_3 = np.array([10,9.5,9.0,8.5])
fos_3 = np.array([5.28,4.66,4.08,3.54])

dia_4 = np.array([18,20,22,24,26,28])
fos_4 = np.array([1.85,2.36,2.93,3.56,4.25,5.00])


# Save the plot as an image file
fig, ax1 = plt.subplots(figsize=(8,5))

# Plot Diameter vs Iterations
ax1.plot(iterations, dia_4, marker='o', linestyle='-', label="Diameter", color='b')
ax1.axhline(y=28, color='r', linestyle='--', label="Calculated Diameter")

# Labels and Title
ax1.set_xlabel("Iterations")
ax1.set_ylabel("Diameter (mm)", color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.legend(loc='lower right')
ax1.grid()

# Create second axis for Factor of Safety (FOS)
ax2 = ax1.twinx()
ax2.plot(iterations, fos_4, marker='s', linestyle='--', label="FOS", color='r')
ax2.set_ylabel("Factor of Safety (FOS)", color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.legend(loc='center right')

# Save the figure
plot_filename = "/storage/vasvia/Fastener_design/diameter_vs_iterations_Problem_5.png"
plt.savefig(plot_filename, dpi=300)

# Show Plot
plt.show()

# Provide the saved file
plot_filename
