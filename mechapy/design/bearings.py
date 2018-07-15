"""Contains object abstractions for common mechanical design components"""

import math

import pint

ureg = pint.UnitRegistry()

@ureg.check('[force]', '[force]', None)
def bearing_life_revs(dynamic_load_rating, dynamic_load, kind='ball'):
    """Bearing L10 calculation per ISO 281

    This approach to bearing life is appropriate for the general case,
    which is assumed to have some dynamic content in its loading composition.
    It represents 90% reliability.

    L_10 = (C / P) ** p
    Exponent "p" is 3 for ball bearings, and 3.333 for roller bearings

    Parameters
    ----------
    dynamic_load_rating : Quantity
        [force]
        Basic dynamic load rating, typically represented by C
    dynamic_load : Quantity
        [force]
        Equivalent dynamic bearing load, typically represented by P
    kind : str
        Default = 'ball'
        Allowable values: 'ball' or 'roller'

    Returns
    -------
    float
        Millions of revolutions
    """
    exp = dict(ball=3, roller=10/3)
    life_revs = (dynamic_load_rating / dynamic_load) ** exp[kind]
    return life_revs

@ureg.check('[force]', '[force]', '[time]', None)
def bearing_life_hours(dynamic_load_rating, dynamic_load, rpm, kind='ball'):
    """Bearing L10 calculation per ISO 281

    This approach to bearing life is appropriate for the general case,
    which is assumed to have some dynamic content in its loading composition.
    It represents 90% reliability.

    L_10h = (1000000 / (60 * rpm)) * (C / P) ** p
    Exponent "p" is 3 for ball bearings, and 3.333 for roller bearings

    Parameters
    ----------
    dynamic_load_rating : Quantity
        [force]
        Basic dynamic load rating, typically represented by C
    dynamic_load : Quantity
        [force]
        Equivalent dynamic bearing load, typically represented by P
    rpm : Quantity
        1 / [time]
        Rotational speed in rpm
    kind : str
        Default = 'ball'
        Allowable values: 'ball' or 'roller'

    Returns
    -------
    float
        Operating hours
    """
    try:
        speed = rpm.to(ureg.rpm)
    except AttributeError:
        raise AttributeError("'rpm' argument must have units of 'rpm' or 'Hz'")
    life_revs = bearing_life_revs(dynamic_load_rating, dynamic_load, kind)
    life_hours = (1000000 / 60 * speed) * life_revs
    return life_hours

@ureg.check('[force]', '[force]', None, None)
def dynamic_equiv_rad_load(actual_rad_load, actual_ax_load, rad_load_factor, ax_load_factor):
    """Determine dynamic equivalent radial load

    The load factors are found in bearing manufacturer tables.

    Parameters
    ----------
    actual_rad_load : Quantity
        [force]
        Actual radial load
    actual_ax_load : Quantity
        [force]
        Actual axial load
    rad_load_factor : float
        Radial load factor, found in manufacturer tables
    ax_load_factor : float
        Axial load factor, found in manufacturer tables

    Returns
    -------
    Quantity
        [force]
        Dynamic equivalent radial load
    """
    dyn_eq_rad_load = rad_load_factor * actual_rad_load + ax_load_factor * actual_ax_load
    return dyn_eq_rad_load

@ureg.check('[force]', '[force]')
def dynamic_equiv_ax_load(actual_ax_load, actual_rad_load):
    """Determine the dynamic equivalent axial load

    This is based on assumption: actual_rad_load / actual_ax_load <= 0.55

    Parameters
    ----------
    actual_ax_load : Quantity
        [force]
        Actual axial load
    actual_rad_load : Quantity
        [force]
        Actual radial load

    Returns
    -------
    Quantity
        [force]
        Dynamic equivalent axial load
    """
    if actual_rad_load / actual_ax_load > 0.55:
        raise ValueError('Ratio of radial/axial load exceeds 0.55 max limit.')
    axial_load = actual_ax_load + 1.2 * actual_rad_load
    return axial_load