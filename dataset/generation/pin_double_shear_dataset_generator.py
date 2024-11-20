from math import pi

# function to determing the mininum viable pin diameter for a pin in double shear given: force, factor of safety, yield strength

def min_pin_diameter(F, FoS, Sy):
    d = sqrt((2*F*Fos)/(pi*0.5*Sy))
    return d


if __name__ == 'main':
    # create the dataset based on a set of forces, safety factors, and yield strengths
    data = []
    for F in []:
        for FoS in []:
            for Sy in []:
                d = min_pin_diameter(F, FoS, Sy)

                #TODO: take the ceiling of d or base on available library

                data.append([F, FoS, Sy, d])
