"""Contains content for engineering materials"""

import os

import pandas as pd

METAL_MAT_PROPS = os.path.join(os.path.dirname(__file__), 'metal_mat_props.csv')
NONMETAL_MAT_PROPS = os.path.join(os.path.dirname(__file__), 'nonmetal_mat_props.csv')

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
    df = pd.read_csv

class Metal(object):
