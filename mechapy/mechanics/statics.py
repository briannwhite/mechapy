"""Contains functions for basic stress computation"""

import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from mechapy.units import ureg
from mechapy.mechanics.mass_props import iyiz_rod, mass_rod
from mechapy.mechanics.materials import Metal


@ureg.check('[force]', '[area]')
def stress_eng(load, area):
    """Engineering stress for uniaxial case, sigma = P/A

    For engineering stress, the effective area represents the *initial* cross-sectional area.

    Parameters
    ----------
    load : Quantity
        [force]
        Uniaxial load on body
    area : Quantity
        [area]
        Cross-sectional area, across which force is applied

    Returns
    -------
    Quantity
        [pressure]

    Raises
    ------
    AttributeError
        If arguments are not passed as appropriate pint unit Quantity type

    Examples
    --------
    >>> from mechapy.units import lbf, sq_in
    >>> stress_eng(1000 * lbf, 100 * sq_in)
    <Quantity(10.0, 'force_pound / square_inch')>
    """
    stress = load / area
    return stress


@ureg.check('[length]', '[length]')
def strain_eng(dlength, length):
    """Engineering strain. The ratio of delta-length over original length.

    Parameters
    ----------
    dlength : Quantity
        [length]
    length : Quantity
        [length]

    Returns
    -------
    Quantity
        [dimensionless]

    Raises
    ------
    AttributeError
        If arguments are not passed as appropriate pint unit Quantity type

    Examples
    --------
    >>> from mechapy.units import inch
    >>> strain_eng(0.02 * inch, 2.0 * inch)
    <Quantity(0.01, 'dimensionless')>
    """
    strain = dlength / length
    return strain


@ureg.check('[force]', '[area]', None)
def stress_true(load, area_actual, strain):
    """True stress, which accounts for reduction in cross-sectional area under stress

    Parameters
    ----------
    load : Quantity
        [force]
    area_actual : Quantity
        [area]
    strain : float
        Dimensionless

    Raises
    ------
    AttributeError
        If arguments are not passed as appropriate pint unit Quantity type
    TypeError
        If 'strain' argument is passed as non-float or non-integer

    Examples
    --------
    >>> from mechapy.units import lbf, sq_in
    >>> stress_true(100 * lbf, 1 * sq_in, 0.01)
    <Quantity(101.0, 'force_pound / square_inch')>
    """
    if not isinstance(strain, (float, int)):
        raise TypeError("'strain' must be dimensionless numerical value")
    true_stress = (load / area_actual) * (1 + strain)
    return true_stress


@ureg.check('[pressure]', None)
def uts_from_brinell(h_b, k_b=500):
    """Calculate ultimate tensile strength from brinell hardness

    Parameters
    ----------
    h_b : Quantity
        [pressure]
        Brinell Hardness value
    k_b : float or int, optional
        Constant. Default = 500, which generally applies for steels categorically

    Returns
    -------
    Quantity
        [pressure]
        Ultimate tensile strength

    Raises
    ------
    AttributeError
        If arguments are not passed as appropriate pint unit Quantity type

    Examples
    --------
    >>> from mechapy.units import lbf, sq_in
    >>> stress_true(100 * lbf, 1 * sq_in, 0.01)
    <Quantity(101.0, 'force_pound / square_inch')>
    """
    if not isinstance(k_b, (float, int)):
        raise TypeError("'k_b' is a constant that must be int or float")
    uts = k_b * h_b
    return uts


@ureg.wraps(ureg.psi, ureg.psi)
def ys_from_uts(uts):
    """Yield strength as a function of ultimate tensile strength

    Parameters
    ----------
    uts : Quantity
        [pressure]
        Must be 'psi'

    Returns
    -------
    Quantity
        [pressure]

    Raises
    ------
    AttributeError
        If arguments are not passed as appropriate pint unit Quantity type

    Examples
    --------
    >>> from mechapy.units import psi
    >>> ys_from_uts(100000 * psi)
    <Quantity(75000.0, 'pound_force_per_square_inch')>
    """
    ys = 1.05 * uts - 30000
    return ys


@ureg.check('[pressure]', None)
def shear_modulus(modulus_elasticity, poisson_ratio):
    """Shear modulus as a function modulus of elasticity and poisson's ratio

    Parameters
    ----------
    modulus_elasticity : Quantity
        [pressure]
        Conventionally represented as 'E'.
    poisson_ratio : float
        For isotropic materials, typically between 0.2 and 0.5. Conventionally represented as 'nu'.

    Returns
    -------
    Quantity
        [pressure]

    Raises
    ------
    AttributeError
        If arguments are not passed as appropriate pint unit Quantity type

    Examples
    --------
    >>> from mechapy.units import psi
    >>> shear_modulus(100000 * psi, 0.25)
    <Quantity(40000.0, 'pound_force_per_square_inch')>
    """
    shear_mod = modulus_elasticity / (2 * (1 + poisson_ratio))
    return shear_mod

class StressTensor(object):
    def __init__(self, sigma_x, sigma_y, tau_xy, theta=0, sigma_z=None, tau_yz=None, tau_zx=None):
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
        self.sigma_z = sigma_z
        self.tau_xy = self.tau_yx = tau_xy
        self.tau_yz = self.tau_zy = tau_yz
        self.tau_zx = self.tau_xz = tau_zx
        self.theta = theta
        if not sigma_z:
            self.dims = 2
        else:
            self.dims = 3
        self.tensor = self.matrix()

    def matrix(self):
        if self.dims == 2:
            matrix = np.matrix([[self.sigma_x, self.tau_xy], [self.tau_yz, self.sigma_y]])
        elif self.dims == 3:
            matrix = np.matrix([[self.sigma_x, self.tau_xy, self.tau_xz],
                                [self.tau_yx, self.sigma_y, self.tau_yz],
                                [self.tau_zx, self.tau_zy, self.sigma_z]])
        else:
            raise ValueError("Tensor matrix may only be 2 or 3 dimensional")

    def sigma_1(self):
        sigma_1 = (((self.sigma_x + self.sigma_y) / 2) +
                   math.sqrt(((self.sigma_x - self.sigma_y) / 2) ** 2 + self.tau_xy ** 2))
        return sigma_1

    def sigma_2(self):
        sigma_2 = (((self.sigma_x + self.sigma_y) / 2) -
                   math.sqrt(((self.sigma_x - self.sigma_y) / 2) ** 2 + self.tau_xy ** 2))
        return sigma_2

    def tau_max(self):
        tau_max = (self.sigma_1() - self.sigma_2()) / 2
        return tau_max

    def sigma_n(self):
        sigma_n = (0.5 * (self.sigma_x + self.sigma_y) +
                   0.5 * (self.sigma_x - self.sigma_y) * math.cos(2 * self.theta) +
                   self.tau_xy * math.sin(2 *self.theta))
        return sigma_n

    def tau_n(self):
        tau_n = -0.5 * (self.sigma_x - self.sigma_y) * math.sin(2 * self.theta) + self.tau_xy * math.cos(2 * self.theta)
        return tau_n

    def plot_mohrs_circle(self):
        fig, ax = plt.subplots()
        if self.dims == 2:
            labels = [r'($\sigma_1$, 0)', r'($\sigma_2$, 0)', r'($\sigma_{avg}$, $\tau_{max}$)', r'($\sigma_{avg}$, $\tau_{max}$)']
            labels_x = [self.sigma_1(), self.sigma_2(), (self.sigma_1() + self.sigma_2()) / 2, (self.sigma_1() + self.sigma_2()) / 2]
            labels_y = [0, 0, self.tau_max(), -self.tau_max()]
            center_x = (self.sigma_1() + self.sigma_2()) / 2
            center_y = 0
            diameter = (self.sigma_1() - self.sigma_2())
            print('Diameter = ' + str(diameter))
            print('Center X = ' + str(center_x))
            circ = Circle(xy=(center_x, center_y), radius=diameter/2, fill=False, edgecolor='blue')
            ax.add_patch(circ)
            xmin = min(0, 1.25 * (center_x - diameter/2))
            xmax = max(0, 1.25 * (center_x + diameter/2))
            ymin = -1.25 * (diameter / 2)
            ymax = 1.25 * (diameter / 2)
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
            plt.grid(which='both')
            plt.title("Mohr's Circle for 2D Tensor")
            for label, x, y in zip (labels, labels_x, labels_y):
                plt.annotate(
                    label, xy=(x, y), xytext=(-40, 0), textcoords='offset points', ha='right', va='bottom',
                    bbox=dict(boxstyle='round', pad=0.5, fc='yellow', alpha=1),
                    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0')
                )
            plt.show()

class Shaft(object):
    def __init__(self, diameter, length, material):
        self.diameter = diameter
        self.length = length
        self.material = material

    def mass(self):
        density = self.material.density
        mass = mass_rod(self.diameter, self.length, density)

    def mass_moment_inertiz_iyiz(self):
        pass

    def apply_transverse_end_load(self, magnitude):
        pass

    def apply_axial_load(self, magnitude):
        pass

    def apply_torsion_load(self, magniude):
        pass

    def remove_transverse_load(self):
        pass

    def remove_axial_load(self):
        pass

    def remove_torsion(self):
        pass

    def sigma_max(self):
        pass

    def tau_max(self):
        pass

    def tau_avg(self):
        pass

class RectangleBeam(object):
    pass

class ThinWallCylinder(object):
    pass

class ThickWallCylinder(object):
    pass



if __name__ == '__main__':
    st = StressTensor(100, 50, 10)
    print('Principal Stress 1 = ' + str(st.sigma_1()))
    print('Principal Stress 2 = ' + str(st.sigma_2()))
    print('Max Shear Stress = ' + str(st.tau_max()))
    st.plot_mohrs_circle()