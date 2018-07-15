# mechapy
A toolbox for engineers that intuitively ties together an OO framework for all things mechanical, e.g.,
materials, sections, components, systems, etc., leveraging the litany of tables that engineers continue
to reference in the appendices of hard cover books. There must be a better way!

Not a mere pile of functions to compute common equations, mechapy strives to be more than this.

Importantly, units are a fundamental, non-trivial aspect of accurate engineering. To that end, this project
leverages 'pint', which is one of the most robust solutions to this problem available in the python ecosystem.
http://pint.readthedocs.io/en/latest/

The design intent is to build intuitively-constructed relationships between classes, building up from materials,
to components, to systems.

```python
>>> from mechapy.units import mm, rpm
>>> from mechapy.design import GearPair, SpurGear
>>> pinion = SpurGear(pitch_dia=300*mm, num_teeth=100, thickness=10*mm)
>>> gear = SpurGear(pitch_dia=600*mm, num_teeth=300, thickness=10*mm)
>>> mesh = GearPair(pinion=pinion, gear=gear, driving_speed=100*rpm)
>>> mesh.driven_speed
<Quantity(33.33333333333333, 'revolutions_per_minute')>
```

# Quick Installation
Download or clone. It's intended to eventually submit to pypi.

# TODO
Project is in *very* early stage of development. A lot to accomplish and would welcome some help:
* Round out materials/mechanics/statics domain
* Testing framework
* Sphinx documentation
* Submit to pypi
* Expand into other ME domains, e.g., fluids, thermo, power cycles, etc.
* The BIG goal is a robust, comprehensive ecosystem that combines OO models with all the look-up
tables, not just a grab-bag of equation functions and utilities.
