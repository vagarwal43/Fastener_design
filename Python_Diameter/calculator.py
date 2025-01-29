import math

def get_tensile_stress_area(d_major, d_minor, pitch=None, num_threads=None):
    """
    Returns the tensile stress area of the bolt rounded to 3 decimal places
    :param d_major: Major diameter of the bolt [mm or in]
    :param d_minor: Major diameter of the bolt [mm or in]
    :param pitch: Pitch of the bolt [mm or in]
    :param num_threads: Number of threads per inch [npi]
    :return: the tensile stress area of the bolt [mm^2}
    """

    # Reference eq 15.1 from Norton
    if pitch is not None:
        d_pitch = d_major - 0.649519 * pitch

    else:
        d_pitch = d_major - 0.649519 / num_threads

    return math.pi / 4 * ((d_pitch + d_minor) / 2) ** 2


def segregate_loads(c, load):
    """
    Identifies the quantity of a load carried by the bolt and by the members
    :param c: Joint stiffness [N/mm or lbf/in]
    :param load: Load applied to the bolt [N or lbf]
    :return: load borne by the bolt, load borne by the members [N or lbf]
    """

    p_b = c * load
    p_m = (1 - c) * load

    return p_b, p_m


def bolt_yield_safety_factor(c, load, preload, a_ts, b_ys):
    """
    Determines the factor of safety against yielding the bolt under statically applied tension load
    :param c: Joint constant [N/mm or lbf/in]
    :param load: Load applied to the joint [N or lbf]
    :param preload: Preload applied to the bolt [N or lbf]
    :param a_ts: Tensile stress area of the bolt [mm^2 or in^2]
    :param b_ys: Yield strength of the bolt [MPa or psi]
    :return:Factor of safety against yielding under statically applied tension load
    """
    # Portion of load carried by the bolt
    f_b = segregate_loads(c, load)[0] + preload

    # Stress in bolt
    sigma_b = f_b / a_ts

    # Factor of safety against yield
    n_y = b_ys / sigma_b

    return n_y


def main():
    d_mj = 11.3
    tensile_area = get_tensile_stress_area(d_major=d_mj,d_minor=9.5,pitch=0.75)
    fos = bolt_yield_safety_factor(c=0.8,load=10000,preload=5000,a_ts=tensile_area,b_ys = 400)

    print("d_ajor:", d_mj)
    print("Area: ", tensile_area)
    print("fos: ", fos)

if __name__ == "__main__":
    main()
