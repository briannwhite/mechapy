"""Contains content for engineering materials"""

import os

import pandas as pd

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

class Metal(object):
    """Contains attributes that are common or average to base material, e.g. steel or aluminum

    Attributes
    ----------
    modulus_elasticity_si : Quantity
        Modulus of elasticity "E" in metric units GPa
    modulus_elasticity_imp : Quantity
        Modulus of elasticity "E" in imperial units Mpsi
    modulus_rigidity_si : Quantity
        Modulus of rigidity "G" in metric units GPa
    modulus_rigitiy_imp : Quantity
        Modulus of rigidity "G" in in imperial units Mpsi

    Parameters
    ----------
    base_mat_alloy : str
        Base material. Allowable values = {'Aluminum', 'Beryl Copper', 'Brass', 'Bronze', 'Copper',
                                           'Gray Cast Iron', 'Magnesium', 'Nickel', 'Carbon Steel',
                                           'Alloy Steel', 'Stainless Steel', 'Titanium', 'Zinc'}
    """
    def __init__(self, base_mat_alloy):
        if base_mat_alloy not in ['Aluminum', 'Beryl Copper', 'Brass', 'Bronze', 'Copper',
                                  'Gray Cast Iron', 'Magnesium', 'Nickel', 'Carbon Steel',
                                  'Alloy Steel', 'Stainless Steel', 'Titanium', 'Zinc']:
            raise NameError('Invalid base material alloy name.')
        mat_props = pd.read_csv(BASE_METAL_PROPS)
        mat_props.index = mat_props['metal']
        select_mat = mat_props.loc[base_mat_alloy].to_dict()
        self.modulus_elasticity_si = select_mat['e_gpa'] * units.gigapascal
        self.modulus_elasticity_imp = select_mat['e_mpsi'] * units.megapsi
        self.modulus_rigidity_si = select_mat['g_gpa'] * units.gigapascal
        self.modulus_rigidity_imp = select_mat['g_mpsi'] * units.megapsi
        self.poissons_ratio = select_mat['nu']
        self.base_metal = select_mat['metal']
        self.coeff_therm_exp_si = select_mat['alpha_microc']

if __name__ == '__main__':
    carbon_steel = Metal('Carbon Steel')
    print(carbon_steel.__dict__)