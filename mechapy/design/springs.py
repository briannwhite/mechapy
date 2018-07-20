"""Contains classes for various spring types"""

import math

from mechapy.units import ureg

class SpringElement(object):
    """Generic spring defined by stiffness, not component dimensions

    Parameters
    ----------
    stiffness : Quantity
        if kind == 'unidirectional':
            dimensionality = [force] / [distance]
        elif kind == 'rotational':
            dimensionality = ([force] * [length]) / [angle]
    kind : str
        Default 'unidirectional'
        Allowable values: 'unidirectional', 'torsion'
    """
    def __init__(self, stiffness, kind='unidirectional'):
        if kind not in ['unidirectional', 'torsion']:
            raise NameError("'kind' arg must be member of ['unidirectional', 'torsion']")
        if dict(ureg.get_dimensionality(stiffness)) != {'[mass]': 1.0, '[time]': -2.0}:
            raise AttributeError("Stiffness must be in units [force]/[length]")
        self.stiffness = stiffness
        self.kind = kind
    #     self._deflection = 0
    #     self._load = 0
    #
    # @property
    # def deflection(self):
    #     return self._deflection
    #
    # @deflection.setter
    # def deflection(self, value):
    #

    @ureg.check('[length]')
    def apply_deflection(self, extension):
        """Apply deflection in the spring, with units corresponding to spring type (length or angle)

        Calling this method will reset any previously applied load or deflection, i.e., not
        supercomposition of loads.

        Parameters
        ----------
        extension : Quantity
            [length]
            Positive for tension, negative for compression

        Returns
        -------
        load : Quantity
            [force]
            Restoring force

        Other Notes
        -----------
        F = -k * x
        """
        load = -self.stiffness * extension
        return load
        
    @ureg.check('[force]')
    def apply_load(self, load):
        """Apply deflection in the spring, with units corresponding to spring type (length or angle)

        Calling this method will reset any previously applied load or deflection, i.e., not
        supercomposition of loads.

        Parameters
        ----------
        load : Quantity
            [force]
            Restoring force. Positive if spring in compression, and negative spring in tension.

        Returns
        -------
        load : Quantity
            [force]
            Restoring force

        Other Notes
        -----------
        F = -k * x
        """
        pass

class CoilSpring(object):
    def __init__(self, coil_dia=None, wire_dia=None, free_length=None, active_coils=None, material=None):
        self._coil_dia = coil_dia
        self._wire_dia = wire_dia
        self._length = free_length
        self._material = material
        self._active_coils = active_coils


class TensionSpring(CoilSpring):
    def __init__(self, outer_dia, wire_dia, free_length, material):
        super().__init__(outer_dia, wire_dia, free_length, material)

    ureg.check('[force]')
    def apply_static_load(self, magnitude):

class CompressionSpring(CoilSpring):
    def __init__(self, stiffness, outer_dia, wire_dia, free_length, active_coils, material):
        super().__init__(stiffness, outer_dia, wire_dia, free_length, material)
        self._active_coils = active_coils
        self._calcs()

        def _calcs(self):
            self.solid_length = self._active_coils + 2
            self.max_force = stiffness * (free_length * self.solid_length)
            self.wire_length = math.pi *

class TorsionSpring(object):
    def __init__(self, tor_stiffness, material=None):
        self._tor_stiffness