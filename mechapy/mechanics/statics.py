"""Contains functions for statics computation"""

from mechapy.units import ureg


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
