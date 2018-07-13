"""Mass and moments of inertia calculations of homogeneous solids"""

import os
import math

import pandas as pd

from mechapy.units import ureg, inch, mm

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


def rolled_sections_df(kind='all', units='all'):
    """Returns dataframe of rolled sections, with optional filtering by section category

    Parameters
    ----------
    kind : str, optional
        Default = 'all'
        May include any combination of 'w', 's', 'c', and 'l' (not case sensitive)
        These correspond to W-shapes, S-shapes, channel and angle sections, respectively
        For example: 'wsc', 'SL'
    units : str: optional
        Default = 'all'
        Other allowable values: {'mm', 'inch'}
    """
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'rolledshape_section_props.csv')
    df = pd.read_csv(filepath)
    if kind != 'all':
        for letter in 'WSCL':
            if letter not in kind.upper():
                df = df.loc[df.designation.str.contains(letter) == False]
        else:
            raise NameError("'kind' arg must contain some combination of 'w', 's', 'c', 'l'")
    if units == 'mm':
        df = df.loc[df.units.str.contains(units) == 'mm']
    elif units == 'inch':
        df = df.loc[df.units.str.contains(units) == 'inch']
    elif units == 'all':
        pass
    else:
        raise NameError("'kind' arg must contain some combination of 'w', 's', 'c', 'l'")
    return df


class RolledSection(object):
    def __init__(self, designation):
        if designation not in rolled_sections_df()['designation'].tolist():
            raise NameError("Invalid designation. Must be member of library registry: " +
                            str(rolled_sections_df()['designation'].tolist()))
        self.designation = designation
        sections = rolled_sections_df()
        props = sections.loc[sections['designation']==designation].to_dict(orient='records')[0]
        if props['base_unit'] == 'inch':
            unit = inch
        else:
            unit = mm
        self.area = props['area_sq'] * (unit ** 2)
        self.moment_x = props['axis_xx_ix'] * unit ** 4
        self.section_modulus_x = props['axis_xx_sx'] * unit ** 3
        self.rad_gyration_y = props['axis_xx_rx'] * unit
        self.moment_y = props['axis_yy_iy'] * unit ** 4
        self.section_modulus_y = props['axis_yy_sy'] * unit ** 3
        self.rad_gyration_y = props['axis_yy_ry'] * unit
        if ('W' in designation) or ('S' in designation) or ('C' in designation):
            self.thickness_flange = props['thick'] * unit
            self.width_flange = props['flange_width'] * unit
            self.thickness_web = props['web_thick'] * unit
            self.depth = props['depth'] * unit
        if ('C' in designation) or ('L in designation'):
            self.centroid_x = props['x'] * unit
        if 'L' in designation:
            self.rad_gyration_z = props['r_z'] * unit
            self.centroid_y = props['y'] * unit

if __name__ == '__main__':
    sect = RolledSection('L8 X 8 X 1')
    print(sect.__dict__)