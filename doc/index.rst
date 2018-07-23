.. mechapy documentation master file, created by
    sphinx-quickstart on Fri Jul 20 15:24:40 2018.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Mechapy: Pythonic Mechanical Engineering
========================================

Release v\ |version|.

**Mechapy** is a library that provides highly intuitive object-oriented relationships
for core mechanical engineering. Its purpose is not an exhaustive repository
of engineering formulas, although of course many are included. Rather,
the goal is to make the boring stuff easy.

Exhaustive registries of materials, sections, fastener specs/grades, etc. provides
programmatic, object-oriented access to look-up tables. Coupled with classes for
common machine components and geometries, low-level engineering is elegantly
automated.

Furthermore, accurate units are paramount in sound engineering. This library builds on
`pint <http://pint.readthedocs.io/en/latest/>`_. The python ecosystem has several
options for handling units in calculations, but pint has emerged as one of the leaders
in this space. It plays nicely with numpy, and it flexibly enables user-customized
additions to its registry.

**Unit-friendly, object-oriented engineering materials:**

    >>> import mechapy as mp
    >>> steel=mp.CarbonSteel(1050,'Annealed')
    >>> steel.density
    <Quantity(7.7, 'kilogram / meter ** 3')>
    >>> steel.mod_elast
    <Quantity(207, 'gigapascal')>
    >>> steel.yield_strength
    <Quantity(365.4, 'megapascal')>
    >>> steel.yield_strength.to(mp.units.ksi)  # Convert to imperial ksi
    <Quantity(52.99678936661845, 'kilopound_force_per_square_inch')>


**Machine component abstractions:**

    >>> thread = mp.MetricThread('M8 X 1.25')
    >>> thread.__dict__
    {'major_dia': <Quantity(8.0, 'milliliter')>,
     'minor_dia': <Quantity(6.47, 'milliliter')>,
     'pitch': 1.25,
     'size': 'M8 X 1.25',
     'stress_area': <Quantity(36.6, 'milliliter ** 2')>}
    >>> grade = mp.SteelScrewGrade(8.8)
    >>> grade.__dict__
    {'area_reduction_min': 35.0,
     'diameter_max': <Quantity(36.0, 'milliliter')>,
     'diameter_min': <Quantity(17.0, 'milliliter')>,
     'elongation': 12.0,
     'proof_load': <Quantity(600, 'megapascal')>,
     'rockwell_hardness_max': 'C34',
     'rockwell_hardness_min': 'C23',
     'sae_grade': 8.8,
     'tensile_strength': <Quantity(830, 'megapascal')>,
     'yield_strength': <Quantity(660.0, 'megapascal')>}
    >>> length = 30 * mp.units.mm
    >>> screw = mp.Screw(thread, grade, length)

**Registry access:**

    >>> ut_reg = mp.UnifiedThreadRegistry()
    >>> len(ut_reg)  # Quantity of pre-configured unified thread specs
    687

Features
--------

Initial development focus is on core mechanics and machine design domains

- Common engineering materials, e.g., metals, polymers
- Common 2D geometries, including exhaustive array of standard structural sections
- Common 3D geometries and their properties
- Stress tensor (planar or non-planar)
- Fastener thread specs and steel grades
- Gears and gear pairs
- Rolling-element bearings

This approach to object-oriented engineering principles easily extends to
all domains of engineering. (Help to achieve this end is welcome!)


The User Guide
--------------

This section of the documentation walks through the fundamentals of interacting
with mechapy.

.. toctree::
    :maxdepth: 2
    :caption: Contents:


API Documentation / Guide
-------------------------

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
