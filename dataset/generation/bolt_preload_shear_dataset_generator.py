from math import pi


def minimum_bolt_diameter(F_s, sigma_y, FoS=1.0):
    """
    Calculate the minimum bolt diameter given the applied shear force, factor of safety, and yield strength.

    Parameters:
    F_s (float): Applied shear force (in N).
    sigma_y (float): Yield strength of the bolt material (in Pa).
    FoS (float): Factor of safety (default is 1).

    Returns:
    float: Minimum bolt diameter (in mm).
    """
    # Calculate the minimum bolt diameter using the derived formula
    d = ((192 * (FoS * F_s)**2) / (3 * pi**2 * sigma_y**2)) ** 0.25
    return d


# function to select from the library of available pin diameters
def select_bolt_diameter(d, available_diameters, FoS):
    if FoS >= 1:
        for ad in available_diameters:
            if ad >= d:
                return ad
    elif FoS < 1:
        # get the nearest available diameter:
        min_diff = float('inf')
        nearest_diameter = None
        for ad in available_diameters:
            if abs(ad - d) < min_diff:
                min_diff = abs(ad - d)
                nearest_diameter = ad
        return nearest_diameter
    return


# tool function to wrap the bolt diameter calculation and selection
def bolt_diameter_tool(F, FoS, Sy, available_diameters):
    d = minimum_bolt_diameter(F, Sy, FoS)
    d = select_bolt_diameter(d, available_diameters, FoS)
    return d


if __name__ == '__main__':
    # test minimum_bolt_diameter function with force = 100N, FoS = 2, Sy = 250MPa
    F_s = 5000  # Applied shear force in Newtons
    sigma_y = 250  # Yield strength in MegaPascals (e.g., 250 MPa)
    factor_of_safety = 2.0  # Factor of safety

    min_diameter = minimum_bolt_diameter(F_s, sigma_y, factor_of_safety)
    print(f"Minimum Bolt Diameter: {min_diameter:.4f} mm")

    available_diameters = [2, 2.5, 3, 3.5, 4, 5, 6, 8, 10, 12]  # M2 to M12 from ASME B18.6.7M, Table 14, "Dimensions of Hex Head Machine Screws."

    forces = list(range(100, 30000, 10))  # N
    safety_factors = [0.1, 0.5, 0.9, 1, 2, 3]
    yield_strengths = [450, 600, 650, 940, 1100]  # MPa, monsterbolts.com

    # create the dataset based on a set of forces, safety factors, and yield strengths
    data = []
    for F in forces:
        for FoS in safety_factors:
            for Sy in yield_strengths:
                d = minimum_bolt_diameter(F, Sy, FoS)

                # select the bolt diameter from the available diameters
                d = select_bolt_diameter(d, available_diameters, FoS)

                data.append([F, FoS, Sy, d])

    print(len(data))

    # save the data to a csv file
    with open('../bolt_single_shear_dataset.csv', 'w') as f:
        f.write('F,FoS,Sy,d\n')
        for row in data:
            f.write(','.join(map(str, row)) + '\n')
