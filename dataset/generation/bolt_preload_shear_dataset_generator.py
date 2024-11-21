from math import pi


def minimum_bolt_diameter(F_s, sigma_y):  # TODO: add factor of safety
    """
    Calculate the minimum bolt diameter given the applied shear force and yield strength.

    Parameters:
    F_s (float): Applied shear force (in N).
    sigma_y (float): Yield strength of the bolt material (in Pa).

    Returns:
    float: Minimum bolt diameter (in meters).
    """
    # Calculate the minimum bolt diameter using the derived formula
    d = ((192 * F_s**2) / (3 * pi**2 * sigma_y**2)) ** 0.25
    return d


# function to select from the library of available pin diameters
def select_bolt_diameter(d, available_diameters):
    for ad in available_diameters:
        if ad >= d:
            return ad
    return


# tool function to wrap the bolt diameter calculation and selection
def bolt_diameter_tool(F, FoS, Sy, available_diameters):
    d = minimum_bolt_diameter(F, Sy)
    d = select_bolt_diameter(d, available_diameters)
    return d


if __name__ == '__main__':
    # TODO: fix the test case
    # test minimum_bolt_diameter function with force = 100N, FoS = 2, Sy = 250MPa
    F_s = 5000  # Applied shear force in Newtons
    sigma_y = 250e6  # Yield strength in Pascals (e.g., 250 MPa)

    min_diameter = minimum_bolt_diameter(F_s, sigma_y)
    print(f"Minimum Bolt Diameter: {min_diameter:.4f} meters")

    available_diameters = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 25, 30, 40, 50]  # mm
    forces = [1]  # N
    safety_factors = [1]
    yield_strengths = [1]  # MPa

    # create the dataset based on a set of forces, safety factors, and yield strengths
    data = []
    for F in forces:
        for FoS in safety_factors:
            for Sy in yield_strengths:
                d = minimum_bolt_diameter(F, Sy)

                # select the bolt diameter from the available diameters
                d = select_bolt_diameter(d, available_diameters)

                data.append([F, FoS, Sy, d])

    # save the data to a csv file
    with open('../bolt_single_shear_dataset.csv', 'w') as f:
        f.write('F,FoS,Sy,d\n')
        for row in data:
            f.write(','.join(map(str, row)) + '\n')
