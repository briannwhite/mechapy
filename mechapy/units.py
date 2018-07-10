"""Contains engineering units abstraction, leveraging 'pint' package"""

import pint

# pylint: disable=invalid-name

ureg = pint.UnitRegistry()

# distance
mm = ureg.milliliter
cm = ureg.centimeter
meter = ureg.meter
km = ureg.kilometer
inch = ureg.inch
foot = ureg.foot
yard = ureg.yard
mile = ureg.mile

# time
sec = ureg.second
minute = ureg.minute
hour = ureg.hour
day = ureg.day

# Force
newton = ureg.newton
kN = ureg.kilonewton
lbf = ureg.force_pound

# Pressure
psi = ureg.psi
psf = ureg.psi * 144
newtons_per_square_meter = newton / meter ** 2
kilopascal = ureg.kPa
megapascal = ureg.MPa

# Area
sq_in = ureg.sq_in
sq_ft = ureg.sq_ft
sq_yd = ureg.sq_yd
sq_mm = ureg.millimeter ** 2
sq_cm = ureg.centimeter ** 2
sq_m = ureg.meter ** 2
sq_km = ureg.kilometer ** 2
