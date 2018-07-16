"""Contains content for engineering materials"""

import os

import pandas as pd
import numpy as np

import mechapy.units as units

METAL_TENSILE_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'metal_mat_props.csv')
#NONMETAL_MAT_PROPS = os.path.join(os.path.dirname(__file__), 'nonmetal_mat_props.csv')
BASE_METAL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'base_metal_props.csv')


class CustomMetal(object):
    # TODO: complete docstrings and units
    def __init__(self, name, density, mod_elast, mod_rigid, poissons_ratio):
        self.base_metal = name
        self.density = density
        self.mod_elast = mod_elast
        self.mod_rigid = mod_rigid
        self.poissons_ratio = poissons_ratio

class CustomMetal(object):
    def __init__(self, density):
        pass  #TODO: work into add() methods of registries

class BaseMetalRegistry(object):
    def __init__(self, unit='SI'):
        mat_props = pd.read_csv(BASE_METAL_PROPS)
        metals = mat_props['metal'].tolist()
        print(metals)
        for metal in metals:
            attr_name = metal.lower().replace(' ','_')
            mat = Metal(base_mat_alloy=metal, unit=unit)
            setattr(self, attr_name, mat)

    # TODO : figure out how to handle checking multi part units
    def add_base_metal(self, base_metal, density, modulus_elasticity, modulus_rigidity, poissons_ratio):
        self.density = density  # TODO: confirm units
        self.modulus_elasticity = modulus_elasticity
        self.modulus_rigidity = modulus_rigidity
        self.poissons_ratio = poissons_ratio
        self.base_metal = base_metal

    def tolist(self):
        metals = [metal for metal in list(self.__dict__.keys()) if not metal.startswith('_')]
        return metals

class CarbonSteelRegistry(object):

    def __init__(self, unit='SI'):
        C_STEEL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'steel_tensile_props.csv')
        df = pd.read_csv(C_STEEL_PROPS)

        for idx in df.index:
            record = df.iloc[idx].to_dict()
            attr_name = 'aisi' + str(record['aisi']) + '_' + record['treatment'].lower()
            mat = CarbonSteel(record['aisi'], record['treatment'], unit=unit)
            setattr(self, attr_name, mat)

class StainlessSteelRegistry(object):
    def __init__(self, unit='SI'):
        S_STEEL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'ss_tensile_props.csv')
        df = pd.read_csv(S_STEEL_PROPS)

        for idx in df.index:
            record = df.iloc[idx].to_dict()
            attr_name = 'aisi' + str(record['aisi']) + '_' +\
                        record['structure'] + '_' + record['treatment']
            mat = StainlessSteel(record['aisi'], record['structure'], record['treatment'],
                                 unit=unit)
            setattr(self, attr_name, mat)

class Metal(object):
    """Contains attributes that are common or average to base material, e.g. steel or aluminum

    Attributes
    ----------
    modulus_elasticity : Quantity
        Modulus of elasticity "E" in metric units GPa
    modulus_rigidity : Quantity
        Modulus of rigidity "G" in metric units GPa
    density : Quantity
    poissons_ratio : float
    base_metal : str

    Parameters
    ----------
    base_mat_alloy : str
        Base material. Allowable values = {'Aluminum', 'Beryl Copper', 'Brass', 'Bronze', 'Copper',
                                           'Gray Cast Iron', 'Magnesium', 'Nickel', 'Carbon Steel',
                                           'Alloy Steel', 'Stainless Steel', 'Titanium', 'Zinc'}
    units : str
        default = 'SI'
        Allowable values: 'SI' or 'Imperial'
    """
    def __init__(self, base_mat_alloy, unit='SI'):
        mat_props = pd.read_csv(BASE_METAL_PROPS)
        if base_mat_alloy not in mat_props['metal'].tolist():
            raise NameError('Invalid base material alloy name.')
        if unit not in ['SI', 'Imperial']:
            raise NameError("Invalid name. 'Units' arg must be 'SI' or 'Imperial'")

        mat_props.index = mat_props['metal']
        select_mat = mat_props.loc[base_mat_alloy].to_dict()
        if unit == 'SI':
            self.density = select_mat['rho'] * (units.newtons / units.kilogram) # TODO: confirm units
            self.modulus_elasticity = select_mat['e_gpa'] * units.gigapascal
            self.modulus_rigidity = select_mat['g_gpa'] * units.gigapascal
        else:
            self.density = select_mat['w'] * (units.lbm / units.cu_ft) # TODO: confirm units
            self.modulus_elasticity = select_mat['e_mpsi'] * units.megapsi
            self.modulus_rigidity = select_mat['g_mpsi'] * units.megap
        self.poissons_ratio = select_mat['nu']
        self.base_metal = select_mat['metal']
        # self.coeff_therm_exp_si = select_mat['alpha_microc']

class CarbonSteel(object):
    """Contains strength attributes for common carbon steel types

    Constructed with default args, instantiates a 1015 as-rolled carbon steel

    Attributes
    ----------
    tensile_strength : float <Quantity>
        Tensile strength in corresponding units
    yield_strength : float <Quantity>
        Yield strength in corresponding units
    elongation_pct : float
        Percentage elongation
    area_reduction : float
        Reduction area
    brinell_hardness : float
        Brinell hardness value
    izod_impact : float <Quantity>
        Izod impact in corresponding joules

    Parameters
    ----------
    aisi : int, optional
        Default = 1015
        One of following: {1015, 1020, 1030, 1040, 1050, 1095, 1118, 3140, 4130, 4140, 4340, 6150,
                           8650, 8740, 9255}
    treatment : str, optional
        Default = 'As-rolled'
        One of following: {'As-rolled', 'Normalized', 'Annealed'}
    unit : str, optional
        Default = 'SI'
        Allowable values: 'SI' or 'Imperial'
    """
    def __init__(self, aisi=1015, treatment='As-rolled', unit='SI'):
        aisi_specs = [1015, 1020, 1030, 1040, 1050, 1095, 1118, 3140, 4130, 4140, 4340, 6150,
                      8650, 8740, 9255]
        treatments = ['As-rolled', 'Normalized', 'Annealed']
        if aisi not in aisi_specs:
            raise ValueError('Invalid AISI specification number. Must be member of ' +
                             str(aisi_specs))
        if treatment not in treatments:
            raise NameError('Invalid treatment name. Must be member of ' + str(treatments))
        # Grade-specific tensile properties
        C_STEEL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'steel_tensile_props.csv')
        df = pd.read_csv(C_STEEL_PROPS)
        props = df.loc[(df['aisi'] == aisi) & (df['treatment'] == treatment)] \
            .to_dict(orient='records')[0]

        # Generic Steel Properties
        mat_props = pd.read_csv(BASE_METAL_PROPS)
        mat_props.index = mat_props['metal']
        select_mat = mat_props.loc['Carbon Steel'].to_dict()

        self.base_metal = 'Carbon Steel'
        self.aisi = aisi
        self.treatment = treatment
        self.elongation_pct = props['elongation_pct']
        self.area_reduction_pct = props['area_reduction']
        self.brinell_hardness = props['brinell_hardness']
        self.poissons_ratio = select_mat['nu']
        self.base_metal = select_mat['metal']
        if unit == 'SI':
            self.density = select_mat['rho'] * (units.kg / units.cu_m)
            self.tensile_strength = props['ts_mpa'] * units.megapascal
            self.yield_strength = props['ys_mpa'] * units.megapascal
            self.izod_impact_j = props['izod_impact_j'] * units.joule
            self.modulus_elasticity = select_mat['e_gpa'] * units.gigapascal
            self.modulus_rigidity = select_mat['g_gpa'] * units.gigapascal
            self.coeff_therm_exp = select_mat['alpha_microc'] # TODO: add units
        elif unit == 'Imperial':
            self.density = select_mat['w'] * (units.lbm / units.cu_in) # TODO: confirm units
            self.tensile_strength = props['ts_ksi'] * units.ksi
            self.yields_strength = props['ys_ksi'] * units.ksi
            # TODO: add imperial izod
            self.modulus_elasticity = select_mat['e_mpsi'] * units.megapsi
            self.modulus_rigidity = select_mat['g_mpsi'] * units.megapsi
            # TODO: add imperial thermal expansion


class StainlessSteel(object):
    """Contains strength attributes for common stainless steel types

    Constructed with default args, instantiates AISI 302 austenitic stainless steel

    Attributes
    ----------
    aisi : int
        AISI specification
    structure : str
        Metallic microstructure, e.g., 'austenitic', 'martensitic', 'ferritic'
    treatment : str
        One of 'anneled', 'cold worked', heat treated'
    tensile_strength : float <Quantity>
        Ultimate tensile strength in corresponding units
    yield_strength : float <Quantity>
        Yield strength in corresponding units
    elongation : float <Quantity>
        Elongation in percentage
    izod_impact : float <Quantity>
        Izod impact in corresponding units
    durability : str
        VP, P, F, G, VG = Very Poor, Poor, Fair, Good, Very Good
    machinability : str
        VP, P, F, G, VG = Very Poor, Poor, Fair, Good, Very Good
    weldability : str
        VP, P, F, G, VG = Very Poor, Poor, Fair, Good, Very Good

    Parameters
    ----------
    aisi : int, optional
        Default = 1015
        One of following: {302, 303, 304, 310, 347, 384, 410, 414, 416, 431, 440, 430, 446}
    treatment : str, optional
        Default = 'As-rolled'
        One of following: {'As-rolled', 'Normalized', 'Annealed'}
    """
    def __init__(self, aisi=302, structure='austenitic', treatment='annealed', unit='SI'):
        aisi_specs = [302, 303, 304, 310, 347, 384, 410, 414, 416, 431, 440, 430, 446]
        if aisi not in aisi_specs:
            raise ValueError('Invalid AISI spec number. Must be member of ' + str(aisi_specs))
        if structure not in ['austenitic', 'martensitic', 'ferritic']:
            raise NameError("'structure' arg must be one of 'austenitic', 'martensitic',"
                            " 'ferritic'")
        if treatment not in ['annealed', 'cold worked', 'heat treated']:
            raise NameError("'structure' arg must be one of 'annealed', 'cold worked', "
                            "'heat treated'")
        if unit not in ['SI', 'Imperial']:
            raise NameError("'unit' arg must equal 'SI' or 'Imperial'")

        # Strength properties
        S_STEEL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'ss_tensile_props.csv')
        df = pd.read_csv(S_STEEL_PROPS)
        props = df.loc[(df['aisi'] == aisi) &
                       (df['structure'] == structure) &
                       (df['treatment'] == treatment)].to_dict(orient='records')[0]

        # Generic stainless steel properties
        mat_props = pd.read_csv(BASE_METAL_PROPS)
        mat_props.index = mat_props['metal']
        select_mat = mat_props.loc['Stainless Steel'].to_dict()

        self.poissons_ratio = select_mat['nu']
        self.base_metal = select_mat['metal']
        self.aisi = aisi
        self.structure = props['structure']
        self.treatment = props['treatment']
        self.elongation = props['el']
        self.durability = props['durability']
        self.machinability = props['machinability']
        self.weldability = props['weldability']
        if unit == 'Imperial':
            self.tensile_strength = props['uts_ksi'] * units.ksi
            self.yield_strength = props['sy_ksi'] * units.ksi
            self.modulus_elasticity = select_mat['e_mpsi'] * units.megapsi
            self.modulus_rigidity = select_mat['g_mpsi'] * units.megapsi
            self.density = select_mat['w'] * units.lbm / units.cu_in
            self.izod_impact = props['izod'] * units.ftlb
        else:
            self.tensile_strength = (props['uts_ksi'] * units.ksi).to(units.MPa)
            self.yield_strength = (props['sy_ksi'] * units.ksi).to(units.MPa)
            self.modulus_elasticity = select_mat['e_gpa'] * units.gigapascal
            self.modulus_rigidity = select_mat['g_gpa'] * units.gigapascal
            self.density = select_mat['rho'] * units.kilogram / units.cu_m
            self.izod_impact = (props['izod'] * units.ftlb).to(units.joules)
        # self.coeff_therm_exp_si = select_mat['alpha_microc']

class DuctileIron(object):
    def __init__(self, grade):
        pass  # TODO: fill out this class

class GrayCastIron(object):
    def __init__(self, grade):
        pass  # TODO: fill out this class

class WroughtAluminum(object):
    def __init__(self, grade):
        pass  # TODO: fill out this class

class CastAluminum(object):
    def __init__(self, grade):
        pass

if __name__ == '__main__':
    generic_carbon_steel = Metal('Carbon Steel')
    specific_carbon_steel = CarbonSteel()
    specific_stainless_steel = StainlessSteel()
    base_registry = BaseMetalRegistry()
    cs_registry = CarbonSteelRegistry()
    ss_registry = StainlessSteelRegistry()
    print(generic_carbon_steel.__dict__)
    print(specific_carbon_steel.__dict__)
    print(specific_stainless_steel.__dict__)
    print(base_registry.__dict__)
    print(ss_registry.__dict__)
    print(cs_registry.__dict__)