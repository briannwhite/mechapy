"""Contains object abstractions for common mechanical design components"""

class Gear(object):

    def __init__(self, pitch_dia, num_teeth, tooth_type='convolute'):
        self.pitch_dia = pitch_dia
        self.num_teeth = num_teeth
        self.tooth_type = tooth_type

class SpurGear(Gear):
    pass

class HelicalGear(Gear):
    pass

class BevelGear(Gear):
    pass

class WormGear(Gear):
    pass

class RollerBearing(object):

    def __init__(self, od, id, num_rollers, spec=None):
    pass

class BallRollerBearing(RollerBearing):
    pass

class CylRollerBearing(RollerBearing):
    pass

class SphericalRollerBearing(RollerBearing):
    pass