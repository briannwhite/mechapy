"""Package for machine design elements"""

from mechapy.design.gears import Gear, SpurGear, HelicalGear, GearPair
from mechapy.design.bearings import bearing_life_revs, bearing_life_hours, dynamic_equiv_ax_load,\
    dynamic_equiv_rad_load
from mechapy.design.fasteners import MetricThreadRegistry, UnifiedThreadRegistry,\
    ScrewGradeRegistry
from mechapy.mechanics.materials import CustomMaterial, CustomMetal, BaseMetalRegistry,\
    CarbonSteelRegistry, StainlessSteelRegistry, PolymerRegistry, Polymer, Metal, CarbonSteel,\
    StainlessSteel, GrayCastIron
from mechapy.mechanics.sections import Circle, Rectangle, RolledSection
from mechapy.mechanics.statics import StressTensor, RoundBar, RectangleBeam, ThickWallCylinder,\
    ThinWallCylinder