"""Contains engineering units abstraction, leveraging 'pint' package"""

import pint

# Some units conventions will override typical pythonic naming
# pylint: disable=invalid-name

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

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
sec = seconds = second = ureg.second
minute = minutes = min = ureg.minute
hour = hours = ureg.hour
day = days = ureg.day

# mass
lb = lbs = pound = pounds = ureg.pound
kilogram = kg = kilgrams = ureg.kilogram

# Force
newton = newtons = ureg.newton
kN = ureg.kilonewton
lbf = ureg.force_pound

# revolutions
rpm = ureg.rpm
hz = Hz = hertz =ureg.hertz

# pressure
psi = ureg.psi
ksi = ureg.kilopsi
megapsi = ureg.megapsi
psf = ureg.psi * 144
newtons_per_square_meter = newton / meter ** 2
kilopascal = kPa = ureg.kPa
megapascal = MPa = ureg.MPa
gigapascal = GPa = ureg.GPa

# area
sq_in = ureg.sq_in
sq_ft = ureg.sq_ft
sq_yd = ureg.sq_yd
sq_mm = ureg.millimeter ** 2
sq_cm = ureg.centimeter ** 2
sq_m = ureg.meter ** 2
sq_km = ureg.kilometer ** 2

# volume
cu_ft = ureg.ft ** 3
cu_in = ureg.inch ** 3
cu_mm = ureg.mm ** 3
cu_cm = ureg.cm ** 3
cu_m = cu_meter = ureg.meter ** 3

# energy
btu = ureg.btu
joule = joules = J = ureg.joule
kilojoule = kilojoules = kJ = ureg.kilojoule
ftlb = footpound = footpounds = ureg.foot * ureg.force_pound
inlb = inchpound = inchpounds = ureg.inch * ureg.force_pound

# temperature
degF = ureg.degF
degC = ureg.degC
degK = ureg.degK