import numpy as np
import matplotlib.pyplot as plt

# Example Data (Simulated Iterative Results)
iterations = np.arange(1, 16)  # Iteration count
dia_0 = np.array([10,9.5,9.0,8.5,8.0,7.5,8.0,7.75,7.5,7.75,7.625,7.5625,7.5,7.5625,7.53125])
dia_1 = np.array([19,20,21,22,23,24,23.5])
dia_2 = np.array([18,17.5,17.3,17.2,17.1,17.0,16.9,16.8,16.7,16.6])
dia_3 = np.array([10,10.5,10.2,10.3,10.4,10.5,10.4,10.5,10.4,10.5,10.4,10.5,10.4,10.5,10.4,10.5,10.4,10.5,10.4,10.5])
dia_4 = np.array([18,19,20,21,22])

# Save the plot as an image file
plt.figure(figsize=(8,5))

# Plot Diameter Change over Iterations
plt.plot(iterations, dia_0, marker='o', linestyle='-', label="Diameter")
plt.axhline(y=7.53, color='r', linestyle='--', label="Final Diameter")

# Labels and Title
plt.xlabel("Iterations")
plt.ylabel("Diameter (mm)")
plt.title("Convergence of Diameter Over Iterations")
plt.legend()
plt.grid()

# Save the figure
plot_filename = "/home/dell/diameter/diameter_vs_iterations_Problem_1.png"
plt.savefig(plot_filename, dpi=300)

# Show Plot
plt.show()

# Provide the saved file
plot_filename
