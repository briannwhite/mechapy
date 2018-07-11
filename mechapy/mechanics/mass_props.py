"""Mass and moments of inertia calculations of homogeneous solids"""

import math

from mechapy.units import ureg, inch


@ureg.check('[length]', '[length]', '[mass]/[volume]')
def mass_rod(diameter, length, density):
    """Mass of a rod. Args require units.

    Parameters
    ----------
    diameter : Quantity
        [length]
    length : Quantity
        [length]
    density : Quantity
        [mass]/[volume]

    Returns
    -------
    Quantity
        [mass]

    Notes
    -----
    mass = (math.pi * diameter ** 2 * length * density) / 4
    """
    mass = (math.pi * diameter ** 2 * length * density) / 4
    return mass


@ureg.check('[mass]', '[length]')
def iyiz_rod(mass, length):
    """Iy and Iz mass moments of inertia for rod. Args require units.

    Parameters
    ----------
    mass : Quantity
        [mass]
    length : Quantity
        [length]

    Returns
    -------
    """

    moment = (mass * length ** 2) / 12
    return moment


@ureg.check('[length]', '[length]', '[mass]/[volume]')
def mass_disk(diameter, thickness, density):
    mass = (math.pi * diameter ** 2 * thickness * density) / 4
    return mass


@ureg.check('[mass]', '[length]')
def ix_disk(mass, diameter):
    moment = (mass * diameter ** 2) / 8
    return moment


@ureg.check('[mass]', '[length]')
def iyiz_disk(mass, diameter):
    moment = (mass * diameter ** 2) / 16
    return moment


@ureg.check('[length]', '[length]', '[length]', '[mass]/[volume]')
def mass_rect_prism(length, width, height, density):
    mass = length * width * height * density
    return mass


@ureg.check('[mass]', '[length]', '[length]')
def ix_rect_prism(mass, length, width):
    moment = (mass / 12) * (length ** 2 + width ** 2)
    return moment


@ureg.check('[mass]', '[length]', '[length]')
def iy_rect_prism(mass, length, height):
    moment = (mass / 12) * (length ** 2 + height ** 2)
    return moment


@ureg.check('[mass]', '[length]', '[length]')
def iz_rect_prism(mass, width, height):
    moment = (mass / 12) * (width ** 2 + height ** 2)
    return moment


@ureg.check('[length]', '[length]', '[mass]/[volume]', '[length]', '[length]')
def mass_cyl(outer_dia, length, density, inner_dia=0 * inch):
    mass = ((math.pi * length * density) / 4) * (outer_dia ** 2 - inner_dia ** 2)
    return mass


@ureg.check('[mass]', '[length]', '[length]')
def ix_cyl(mass, outer_dia, inner_dia=0 * inch):
    moment = (mass / 8) * (outer_dia ** 2 + inner_dia ** 2)
    return moment


@ureg.check('[mass]', '[length]', '[length]', '[length]')
def iyiz_cyl(mass, outer_dia, length, inner_dia=0 * inch):
    moment = (mass / 48) * (3 * outer_dia ** 2 + 3 * inner_dia ** 2 + 4 * length ** 2)
    return moment
