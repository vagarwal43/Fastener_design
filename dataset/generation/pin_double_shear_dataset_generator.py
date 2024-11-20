from math import pi, sqrt


# function to determing the mininum viable pin diameter for a pin in double shear giventhe following, and assuming a
# nominal area: force, factor of safety, yield strength
def min_pin_diameter(F, FoS, Sy):
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
    available_diameters = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 25, 30, 40, 50]


    # create the dataset based on a set of forces, safety factors, and yield strengths
    data = []
    for F in [1]:
        for FoS in [1]:
            for Sy in [1]:
                d = min_pin_diameter(F, FoS, Sy)

                # select the pin diameter from the available diameters
                d = select_pin_diameter(d, available_diameters)

                data.append([F, FoS, Sy, d])

    # save the data to a csv file
    with open('../pin_double_shear_dataset.csv', 'w') as f:
        f.write('F,FoS,Sy,d\n')
        for row in data:
            f.write(','.join(map(str, row)) + '\n')
