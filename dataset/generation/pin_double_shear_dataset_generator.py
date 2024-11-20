from math import pi, sqrt


# function to determing the mininum viable pin diameter for a pin in double shear giventhe following, and assuming a nominal area:
# force, factor of safety, yield strength
def min_pin_diameter(F, FoS, Sy):
    d = sqrt((2 * F * FoS) / (pi * 0.5 * Sy))
    return d


if __name__ == '__main__':
    # create the dataset based on a set of forces, safety factors, and yield strengths
    data = []
    for F in [1]:
        for FoS in [1]:
            for Sy in [1]:
                d = min_pin_diameter(F, FoS, Sy)

                # TODO: take the ceiling of d or base on available library

                data.append([F, FoS, Sy, d])

    # save the data to a csv file
    with open('../pin_double_shear_dataset.csv', 'w') as f:
        f.write('F,FoS,Sy,d\n')
        for row in data:
            f.write(','.join(map(str, row)) + '\n')
