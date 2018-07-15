"""Contains object abstractions for common mechanical design components"""

import math

import pint

ureg = pint.UnitRegistry()

class Gear(object):
    """Base class for gears

    Properties
    ----------
    pitch_dia : Quantity
        [length]
        Pitch diameter
    num_teeth : int
        Number of teeth
    """

    def __init__(self, pitch_dia, num_teeth):
        dia_dim = dict(ureg.get_dimensionality(pitch_dia))
        if '[length]' not in dia_dim:
            raise AttributeError("Arg 'pitch_dia' must have [length] dimensionality")
        self._pitch_dia = pitch_dia
        self._num_teeth = num_teeth

    @property
    def pitch_dia(self):
        return self._pitch_dia

    #@ureg.check('[length]')
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
    """Class with derived attributes for spur gear geometry

    Attributes
    ----------
    diametral_pitch : Quantity
        [length]
        Number of teeth per pitch diameter, commonly represented as 'P'
    thickness : Quantity
        [length]
        Gear thickness
    circular_pitch : Quantity
        [length]
        pi / P
    addendum : Quantity
        [length]
        1 / P
    dedendum : Quantity
        [length]
        1.25 / P
    dedendum_shaved : Quantity
        [length]
        1.35 / P
    working_depth : Quantity
        [length]
        2 / P
    whole_depth : Quantity
        [length]
        2.25 / P
    whole_depth_shaved : Quantity
        [length]
        2.35 / P
    clearance : Quantity
        [length]
        0.25 / P
    clearance_shaved : Quantity
        [length]
        0.35 / P
    outside_dia : Quantiy
        [length]
        (N + 2) / P
    root_dia : Quantity
        [length]
        (N - 2.5) / P
    root_dia_shaved : Quantity
        [length]
        (N - 2.7) / P
    circular_thickness_basic : Quantity
        [length]
        1.5708 / P

    Properties
    ----------
    pitch_dia : Quantity
        [length]
        Pitch diameter
        N / P
    num_teeth : Quantity
        [length]
        Number of teeth
    """
    def __init__(self, pitch_dia, num_teeth, thickness):
        dia_dim = dict(ureg.get_dimensionality(pitch_dia))
        t_dim = dict(ureg.get_dimensionality(thickness))
        if '[length]' not in dia_dim:
            raise AttributeError("Arg 'pitch_dia' must have [length] dimensionality")
        if '[length]' not in t_dim:
            raise AttributeError("Arg 'thickness' must have [length] dimensionality")
        super().__init__(pitch_dia, num_teeth)
        self.thickness = thickness
        self._calcs()

    def _calcs(self):
        """Calculate derived properties"""
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

class HelicalGear(Gear):
    class SpurGear(Gear):
        """Class with derived attributes for helical gear geometry

        Attributes
        ----------
        diametral_pitch : Quantity
            [length]
            Number of teeth per pitch diameter, commonly represented as 'P'
        norm_diametral_pitch : Quantity
            [length]
            Normal diametral pitch = P / cos(beta)
        thickness : Quantity
            [length]
            Gear thickness
        circular_pitch : Quantity
            [length]
            pi / P
        norm_circular_pitch : Quantity
            [length]
            Normal circular pitch = P_c * cos(beta)
        axial_pitch : Quantity
            [length]
            Axial pitch = P_c / tan(beta)
        addendum : Quantity
            [length]
            1 / P
        norm_module : Quantity
            [length]
            Normal module = 1 / (P * cos(beta))
        dedendum : Quantity
            [length]
            1.25 / P
        dedendum_shaved : Quantity
            [length]
            1.35 / P
        working_depth : Quantity
            [length]
            2 / P
        whole_depth : Quantity
            [length]
            2.25 / P
        whole_depth_shaved : Quantity
            [length]
            2.35 / P
        clearance : Quantity
            [length]
            0.25 / P
        clearance_shaved : Quantity
            [length]
            0.35 / P
        outside_dia : Quantiy
            [length]
            (N + 2) / P
        root_dia : Quantity
            [length]
            (N - 2.5) / P
        root_dia_shaved : Quantity
            [length]
            (N - 2.7) / P
        circular_thickness_basic : Quantity
            [length]
            1.5708 / P

        Properties
        ----------
        pitch_dia : Quantity
            [length]
            Pitch diameter
            N / P
        num_teeth : Quantity
            [length]
            Number of teeth
        beta : Quantity
            [angle]
            helix angle
        """
    def __init__(self, pitch_dia, num_teeth, thickness, beta):
        dia_dim = dict(ureg.get_dimensionality(pitch_dia))
        t_dim = dict(ureg.get_dimensionality(thickness))
        if '[length]' not in dia_dim:
            raise AttributeError("Arg 'pitch_dia' must have [length] dimensionality")
        if '[length]' not in t_dim:
            raise AttributeError("Arg 'thickness' must have [length] dimensionality")
        try:
            beta = beta.to(ureg.radians)
        except AttributeError:
            raise AttributeError("'beta' arg must be passed with degrees or radians units")
        else:
            self._beta = beta
        super().__init__(pitch_dia, num_teeth)
        self.thickness = thickness
        self._calcs()

    def _calcs(self):
        """Calculate derived properties"""
        self.diametral_pitch = self.num_teeth / self.pitch_dia
        self.norm_diametral_pitch = self.diametral_pitch / math.cos(self.beta)
        self.circular_pitch = math.pi / self.diametral_pitch
        self.norm_circular_pitch = self.circular_pitch * math.cos(self.beta)
        self.axial_pitch = self.circular_pitch / math.tan(self.beta)
        self.addendum = 1 / self.diametral_pitch
        self.norm_module = self.addendum / math.cos(self.beta)
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
        """Override number of teeth setter"""
        Gear.num_teeth.fset(self, value)
        self._calcs()

    @Gear.pitch_dia.setter
    def pitch_dia(self, value):
        """Override pitch diameter setter"""
        Gear.pitch_dia.fset(self, value)
        self._calcs()

    @property
    def beta(self):
        """Beta getter"""
        return self._beta

    @beta.setter
    def beta(self, value):
        """Beta setter"""
        try:
            beta = value.to(ureg.radians)
        except AttributeError:
            raise AttributeError("'beta' arg must be passed with degrees or radians units")
        else:
            self._beta = value
        self._calcs()

class GearPair(object):
    """Gear pair with optional driving speed

    Parameters
    ----------
    pinion : SpurGear or HelicalGear
    gear : SpurGear or HelicalGear
    driving_speed : float <radians / second>
    """
    def __init__(self, pinion, gear, driving_speed=0):
        if (not isinstance(pinion, SpurGear)) or (not isinstance(gear, SpurGear)):
            raise TypeError("'pinion' and 'gear' args must be type 'SpurGear'")
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
    """Container for a pinion/gear pair, using Gear class

    Attributes
    ----------
    pinion : Gear
    gear : Gear

    Parameters
    ----------
    pinion : Gear
        Driving component (typically smaller in size)
    gear : Gear, optional
        Driven component
    """
    def __init__(self, pinion, gear=None):
        self.pinion = pinion
        self.gear = gear


if __name__ == '__main__':
    spurgear = SpurGear(pitch_dia=300*ureg.mm, num_teeth=100, thickness=10*ureg.mm)
    print(spurgear.__dict__)
    spurgear.num_teeth = 150
    print(spurgear.__dict__)
    heligear = HelicalGear(pitch_dia=200*ureg.mm, num_teeth=200, thickness=10*ureg.mm, beta=20*ureg.radians)
    print(heligear.__dict__)
    heligear.beta = 15 * ureg.degrees
    print(heligear.__dict__)
    gearpair = GearPair(pinion=SpurGear(pitch_dia=300*ureg.mm, num_teeth=100, thickness=10*ureg.mm),
                        gear=SpurGear(pitch_dia=600*ureg.mm, num_teeth=300, thickness=10*ureg.mm),
                        driving_speed=100*ureg.rpm)
    print(gearpair.driven_speed)
