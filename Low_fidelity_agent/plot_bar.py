import matplotlib.pyplot as plt

# Manually collected data from your iterations
iterations = [
    {"diameter": 12.0, "bolt_fos": 3.80, "plate_fos": 6.00, "num_bolts": 4},
    {"diameter": 12.5, "bolt_fos": 4.17, "plate_fos": 6.25, "num_bolts": 4},
    {"diameter": 12.5, "bolt_fos": 3.13, "plate_fos": 4.69, "num_bolts": 3},
    {"diameter": 13.0, "bolt_fos": 3.42, "plate_fos": 4.88, "num_bolts": 3},
    {"diameter": 13.5, "bolt_fos": 3.72, "plate_fos": 5.06, "num_bolts": 3},
    {"diameter": 14.0, "bolt_fos": 4.03, "plate_fos": 5.25, "num_bolts": 3},
    {"diameter": 14.0, "bolt_fos": 2.69, "plate_fos": 3.50, "num_bolts": 2},
    {"diameter": 14.5, "bolt_fos": 2.91, "plate_fos": 3.62, "num_bolts": 2},
    {"diameter": 15.0, "bolt_fos": 3.13, "plate_fos": 3.75, "num_bolts": 2},
    {"diameter": 15.5, "bolt_fos": 3.37, "plate_fos": 3.87, "num_bolts": 2},
    {"diameter": 16.0, "bolt_fos": 3.62, "plate_fos": 4.00, "num_bolts": 2},
    {"diameter": 16.5, "bolt_fos": 3.87, "plate_fos": 4.12, "num_bolts": 2},
    {"diameter": 17.0, "bolt_fos": 4.13, "plate_fos": 4.25, "num_bolts": 2}
]

# Extract values
iters = list(range(1, len(iterations) + 1))
bolt_fos = [step["bolt_fos"] for step in iterations]
plate_fos = [step["plate_fos"] for step in iterations]
diameters = [step["diameter"] for step in iterations]
bolt_counts = [step["num_bolts"] for step in iterations]

# --------------------
# Plot 1: FOS vs Iteration
# --------------------
plt.figure(figsize=(10, 5))
plt.plot(iters, bolt_fos, marker='o', label='Bolt FOS')
plt.plot(iters, plate_fos, marker='s', label='Plate FOS')
plt.axhline(4.0, color='gray', linestyle='--', label='Desired FOS')
plt.axhline(4.5, color='lightgray', linestyle=':', linewidth=1)
plt.axhline(3.5, color='lightgray', linestyle=':', linewidth=1)
plt.xlabel("Iteration")
plt.ylabel("Factor of Safety")
plt.title("FOS vs Iteration")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("fos_vs_iteration.png")
plt.close()

# --------------------
# Plot 2: Diameter and Number of Bolts vs Iteration
# --------------------
plt.figure(figsize=(10, 5))
plt.plot(iters, diameters, marker='^', label='Major Diameter (mm)')
plt.plot(iters, bolt_counts, marker='D', label='Number of Bolts')
plt.xlabel("Iteration")
plt.ylabel("Design Parameters")
plt.title("Bolt Diameter and Count vs Iteration")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("params_vs_iteration.png")
plt.close()
