from math import pi, sqrt


def min_pin_diameter(F, FoS, Sy):
    '''
    function to determining the minimum viable pin diameter for a pin in double shear given the following, and assuming
    a nominal area, and that allowable shear ~= 0.5*yield strength: force, factor of safety, yield strength.
    F: force in N
    FoS: factor of safety
    Sy: yield strength in MPa
    returns: minimum pin diameter in mm
    '''
    d = sqrt((2 * F * FoS) / (pi * 0.5 * Sy))
    return d


# function to select from the library of available pin diameters
def select_pin_diameter(d, available_diameters):
    for ad in available_diameters:
        if ad >= d:
            return ad
    return


# tool function to wrap the pin diameter calculation and selection
def pin_diameter_tool(F, FoS, Sy, available_diameters):
    d = min_pin_diameter(F, FoS, Sy)
    d = select_pin_diameter(d, available_diameters)
    return d


if __name__ == '__main__':
    # test min_pin_diameter function with force = 100N, FoS = 2, Sy = 250MPa
    print("Test min_pin_diameter function with force = 100N, FoS = 2, Sy = 250MPa")
    print(f"min pin diameter: {min_pin_diameter(100, 2, 250)} mm = 1.01 mm")

    available_diameters = [1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 25]  # mm https://www.bonehamusa.com/wp-content/uploads/2017/10/Dowel-Pins-Metric-to-ASME.pdf
    forces = list(range(100, 30000, 10))  # N
    safety_factors = [1, 2, 3]
    yield_strengths = [415, 360, 215, 290, 275]  # MPa, 4140 alloy steel, 52100 alloy steel, 18-8 stainless steel, 316 stainless steel, 416 stainless steel https://www.mcmaster.com/products/pins/dowel-pins-2~/dowel-pins-1~~/

    # create the dataset based on a set of forces, safety factors, and yield strengths
    data = []
    for F in forces:
        for FoS in safety_factors:
            for Sy in yield_strengths:
                d = min_pin_diameter(F, FoS, Sy)

                # select the pin diameter from the available diameters
                d = select_pin_diameter(d, available_diameters)

                data.append([F, FoS, Sy, d])

    # save the data to a csv file
    with open('../pin_double_shear_dataset.csv', 'w') as f:
        f.write('F,FoS,Sy,d\n')
        for row in data:
            f.write(','.join(map(str, row)) + '\n')
