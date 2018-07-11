"""Mass and moments of inertia calculations of homogeneous solids"""

import math

import pint

from mechapy.units import ureg, inch

class Rectangle(object):
    """2D rectangle section with attributes for common area properties

    Attributes
    ----------
    area : Quantity
        [area]
    moment_intertia : Quantity
        [length ** 4]
    section_modulus : Quantity
        [length ** 3]
    radius_gyration : Quantity
        [length]
    centroidal_dist : Quantity
        [length]

    Parameters
    ----------
    height : Quantity
        [length]
    base : Quantity
        [length]

    Examples
    --------
    >>> from mechapy.units import meter
    >>> rect = Rectangle(0.5 * meter, 0.25 * meter)
    >>> moment = rect.moment_inertia
    >>> modulus = rect.section_modulus
    """
    def __init__(self, height, base):
        height_dim = dict(ureg.get_dimensionality(height))
        base_dim = dict(ureg.get_dimensionality(base))

        if ('[length]' not in height_dim) or ('[length]' not in base_dim):
            raise AttributeError("Args 'height' and 'base' must be passed with [length] dimensionality")

        self.area = base * height
        self.moment_inertia = (base * height ** 3) / 12
        self.section_modulus = (base * height ** 2) / 6
        self.radius_gyration = (0.289 * height)
        self.centroidal_dist = height / 2



class Circle(object):
    """2D circle section with attributes for common area properties

    Attributes
    ----------
    area : Quantity
        [area]
    moment_intertia : Quantity
        [length ** 4]
    section_modulus : Quantity
        [length ** 3]
    polar_moment_inertia : Quantity
        [length ** 4]
    radius_gyration : Quantity
        [length]

    Parameters
    ----------
    diameter : diameter
        [length]

    Examples
    --------
    >>> from mechapy.units import meter
    >>> circ = Circle(0.5 * meter)
    >>> moment = circ.moment_inertia
    >>> modulus = circ.section_modulus
    """
    def __init__(self, diameter):
        dia_dim = dict(ureg.get_dimensionality(diameter))
        if '[length]' not in dia_dim:
            raise AttributeError("Arg 'diameter' and 'base' must be passed with [length] dimensionality")
        self.area = math.pi * diameter
        self.moment_inertia = (math.pi * diameter ** 4) / 64
        self.section_modulus = (math.pi * diameter ** 3) / 32
        self.polar_moment_inertia = (math.pi * diameter ** 4) / 32
        self.radius_gyration = diameter / 4

class WideFlangeImperial:
    PASS