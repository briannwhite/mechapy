"""Contains object abstractions for common mechanical design components"""

import math

class Gear(object):

    def __init__(self, pitch_dia, num_teeth, tooth_type='involute'):
        self._pitch_dia = pitch_dia
        self._num_teeth = num_teeth
        self.tooth_type = tooth_type

    @property
    def pitch_dia(self):
        return self._pitch_dia

    @pitch_dia.setter
    def pitch_dia(self, value):
        self._pitch_dia = value

    @property
    def num_teeth(self):
        return self._num_teeth

    @num_teeth.setter
    def num_teeth(self, value):
        self._num_teeth = value

class SpurGear(Gear):

    def __init__(self, pitch_dia, num_teeth, thickness, tooth_type='involute'):
        super().__init__(pitch_dia, num_teeth, tooth_type)
        self.thickness = thickness
        self._calcs()

    def _calcs(self):
        self.diametral_pitch = self.num_teeth / self.pitch_dia
        self.circular_pitch = math.pi / self.diametral_pitch
        self.addendum = 1 / self.diametral_pitch
        self.dedendum = 1.25 / self.diametral_pitch
        self.dedendum_shaved = 1.35 / self.diametral_pitch
        self.working_depth = 2 / self.diametral_pitch
        self.whole_depth = 2.25 / self.diametral_pitch
        self.whole_depth_shaved = 2.35 / self.diametral_pitch
        self.clearance = 0.25 / self.diametral_pitch
        self.clearance_shaved = 0.35 / self.diametral_pitch
        self.outside_dia = (self.num_teeth + 2) / self.diametral_pitch
        self.root_dia = (self.num_teeth - 2.5) / self.diametral_pitch
        self.root_dia_shaved = (self.num_teeth - 2.7) / self.diametral_pitch
        self.circular_thickness_basic = 1.5708 / self.diametral_pitch

    @Gear.num_teeth.setter
    def num_teeth(self, value):
        Gear.num_teeth.fset(self, value)
        self._calcs()

    @Gear.pitch_dia.setter
    def pitch_dia(self, value):
        Gear.pitch_dia.fset(self, value)
        self._calcs()

# class HelicalGear(Gear):
#     pass
#
# class BevelGear(Gear):
#     pass
#
# class WormGear(Gear):
#     pass

class SpurGearPair(object):
    """Gear pair with optional driving speed

    Parameters
    ----------
    pinion : mechapy.design.gears.Gear
    gear : mechapy.design.gears.Gear
    driving_speed : float <radians / second>
    """
    def __init__(self, pinion, gear, driving_speed=0):
        self.pinion = pinion
        self.gear = gear
        self._driving_speed = driving_speed
        self.driven_speed = driving_speed * (pinion.num_teeth / gear.num_teeth)
        self.center_distance = (pinion.pitch_dia + gear.pitch_dia) / 2

    @property
    def driving_speed(self):
        return self._driving_speed

    @driving_speed.setter
    def driving_speed(self, value):
        self.driven_speed = value * (self.pinion.num_teeth / self.gear.num_teeth)

class ReductionShaft(object):
    def __init__(self, pinion, gear=None):
        self.pinion = pinion
        self.gear = gear


if __name__ == '__main__':
    spurgear = SpurGear(pitch_dia=300, num_teeth=100, thickness=10)
    print(spurgear.__dict__)
    spurgear.num_teeth = 150
    print(spurgear.__dict__)