"""Contains content for engineering materials"""

import os

import pandas as pd
import numpy as np

import mechapy.units as units

METAL_TENSILE_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'metal_mat_props.csv')
#NONMETAL_MAT_PROPS = os.path.join(os.path.dirname(__file__), 'nonmetal_mat_props.csv')
BASE_METAL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'base_metal_props.csv')

def get_mats(kind='metals', base=None, desc=None, spec=None, unit='lb-in-sec'):
    """Get material properties

    Parameters
    ----------
    kind : str
        Allowable values: {'Metals', 'Nonmetals'}
    base : str
        Allowable values for metals: {'Steel', 'Cast Iron', 'Aluminum', 'Copper'}
        Allowable values for nonmetals:
    """
    pass

def mat_registry():
    pass

class CustomMetal(object):
    def __init__(self, name, density, mod_elast, mod_rigid, poissons_ratio):
        self.base_metal = name
        self.density = density
        self.mod_elast = mod_elast
        self.mod_rigid = mod_rigid
        self.poissons_ratio = poissons_ratio

class CustomAlloy(object):
    def __init__(self, density):
        pass

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
    pass

class StainlessSteelRegistry(object):
    pass

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
    ts_mpa : float <Quantity>
        Tensile strength in MPa units
    ts_ksi : float <Quantity>
        Tensile strength in ksi units
    ys_mpa : float <Quantity>
        Yield strength in MPa units
    ys_ksi : float <Quantity>
        Yield strength in ksi units
    elongation_pct : float
        Percentage elongation
    area_reduction : float
        Reduction area
    brinell_hardness : float
        Brinell hardness value
    izod_impact_j : float <Quantity>
        Izod impact in joules units
    izod_impact_ftlb : float <Quanity>
        Izod impact in ft-lb units

    Parameters
    ----------
    aisi : int, optional
        Default = 1015
        One of following: {1015, 1020, 1030, 1040, 1050, 1095, 1118, 3140, 4130, 4140, 4340, 6150,
                           8650, 8740, 9255}
    treatment : str, optional
        Default = 'As-rolled'
        One of following: {'As-rolled', 'Normalized', 'Annealed'}
    """
    def __init__(self, aisi=1015, treatment='As-rolled'):
        aisi_specs = [1015, 1020, 1030, 1040, 1050, 1095, 1118, 3140, 4130, 4140, 4340, 6150,
                      8650, 8740, 9255]
        treatments = ['As-rolled', 'Normalized', 'Annealed']
        if aisi not in aisi_specs:
            raise ValueError('Invalid AISI specification number. Must be member of ' +
                             str(aisi_specs))
        if treatment not in treatments:
            raise NameError('Invalid treatment name. Must be member of ' + str(treatments))
        C_STEEL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'steel_tensile_props.csv')
        df = pd.read_csv(C_STEEL_PROPS)
        props = df.loc[(df['aisi'] == aisi) & (df['treatment'] == treatment)] \
            .to_dict(orient='records')[0]
        self.base_metal = 'Carbon Steel'
        self.aisi = aisi
        self.treatment = treatment
        self.ts_mpa = props['ts_mpa'] * units.megapascal
        self.ts_ksi = props['ts_ksi'] * units.ksi
        self.ys_mpa = props['ys_mpa'] * units.megapascal
        self.ys_ksi = props['ys_ksi'] * units.ksi
        self.elongation_pct = props['elongation_pct']
        self.area_reduction_pct = props['area_reduction']
        self.brinell_hardness = props['brinell_hardness']
        self.izod_impact_j = props['izod_impact_j'] * units.joule

        # Generic Steel Properties
        mat_props = pd.read_csv(BASE_METAL_PROPS)
        mat_props.index = mat_props['metal']
        select_mat = mat_props.loc['Carbon Steel'].to_dict()
        self.modulus_elasticity_si = select_mat['e_gpa'] * units.gigapascal
        self.modulus_elasticity_imp = select_mat['e_mpsi'] * units.megapsi
        self.modulus_rigidity_si = select_mat['g_gpa'] * units.gigapascal
        self.modulus_rigidity_imp = select_mat['g_mpsi'] * units.megapsi
        self.poissons_ratio = select_mat['nu']
        self.base_metal = select_mat['metal']
        self.coeff_therm_exp_si = select_mat['alpha_microc']

class StainlessSteel(object):
    """Contains strength attributes for common stainless steel types

    Constructed with default args, instantiates AISI 302 austenitic stainless steel

    Attributes
    ----------
    aisi : int
        AISI specification
    structure : str
        Metallic microstructure, e.g., 'austenitic', 'martensitic', 'ferritic'
    su_an : float <Quantity>
        Ultimate tensile strength, annealed
    su_cw : float <Quantity>
        Ultimate tensile strength, cold-worked
    su_ht : float <Quanity>
        Ultimate tensile strength, heat-treated
    sy_an : float <Quantity>
        Yield strength, annealed
    sy_cw : float <Quantity>
        Yield strength, cold-worked
    sy_ht : float <Quantity>
        Yield strength, heat-treated
    el_an : float <Quantity>
        Elongation, annealed
    el_cw : float <Quantity>
        Elongation, cold-worked
    el_ht : float <Quantity>
        Elongation, heat-treated
    izod_an : float <Quantity>
        Izod impact, annealed
    izod_cw : float <Quantity>
        Izod impact, cold-worked
    izod_ht : float <Quantity>
        Izod impact, heat-treated
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
    def __init__(self, aisi=302):
        aisi_specs = [302, 303, 304, 310, 347, 384, 410, 414, 416, 431, 440, 430, 446]
        if aisi not in aisi_specs:
            raise ValueError('Invalid AISI spec number. Must be member of ' + str(aisi_specs))

        # Strength properties
        S_STEEL_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'ss_tensile_props.csv')
        df = pd.read_csv(S_STEEL_PROPS)
        props = df.loc[(df['aisi'] == aisi)].to_dict(orient='records')[0]
        # for column in df.columns:
        #     setattr(self, column, props[column])
        self.base_metal = 'Stainless Steel'
        self.aisi = aisi
        self.structure = props['structure']
        self.su_an = props['su_an'] * units.ksi
        self.su_cw = props['su_cw'] * units.ksi
        self.su_ht = props['su_ht'] * units.ksi
        self.sy_an = props['su_an'] * units.ksi
        self.sy_cw = props['su_cw'] * units.ksi
        self.ys_ht = props['su_ht'] * units.ksi
        self.el_an = props['el_an']
        self.el_cw = props['el_cw']
        self.el_ht = props['el_ht']
        self.izod_an = props['izod_an']
        self.izod_cw = props['izod_cw']
        self.izoc_ht = props['izod_ht']
        self.durability = props['durability']
        self.machinability = props['machinability']
        self.weldability = props['weldability']

        # Generic stainless steel properties
        mat_props = pd.read_csv(BASE_METAL_PROPS)
        mat_props.index = mat_props['metal']
        select_mat = mat_props.loc['Stainless Steel'].to_dict()
        self.modulus_elasticity_si = select_mat['e_gpa'] * units.gigapascal
        self.modulus_elasticity_imp = select_mat['e_mpsi'] * units.megapsi
        self.modulus_rigidity_si = select_mat['g_gpa'] * units.gigapascal
        self.modulus_rigidity_imp = select_mat['g_mpsi'] * units.megapsi
        self.density_si =select_mat['rho'] * units.kilogram / units.cu_m # TODO: confirm units

        self.poissons_ratio = select_mat['nu']
        self.base_metal = select_mat['metal']
        self.coeff_therm_exp_si = select_mat['alpha_microc']



if __name__ == '__main__':
    generic_carbon_steel = Metal('Carbon Steel')
    specific_carbon_steel = CarbonSteel()
    specific_stainless_steel = StainlessSteel()
    print(generic_carbon_steel.__dict__)
    print(specific_carbon_steel.__dict__)
    print(specific_stainless_steel.__dict__)