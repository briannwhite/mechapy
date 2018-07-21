"""Contains classes and registries for screw threads and grades"""

import os

import pandas as pd

from mechapy.units import inch, mm, ksi, MPa

class UnifiedScrewThread(object):
    """Contains dimensional attributes for external unified screw threads

    Parameters
    --------
    size : str
        [size]-[threads per inch] [series]
        Examples, '1 1/8-7 UNC', '5/16-20 UN'
        If fractional greater than 1, include space before fraction, and no decimals.
    fit_class : str
        Default = '2A', which represents most common.
        Other options = '1A' and '3A', but '1A' has very few instances
    """

    def __init__(self, size, fit_class='2A'):
        UST_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'unified_screw_threads.csv')
        df = pd.read_csv(UST_PROPS)
        props = df.loc[(df['size'] == size) & (df['fit_class'] == fit_class)].to_dict(orient='records')[0]
        self.size = props['size'].split('-')[0]
        self.threads_per_inch = props['size'].replace(r"\xa0", " ").split('-')[1].split(' U')[0]
        self.series = props['size'].split(' ')[-1]
        self.fit_class = props['fit_class']
        self.allowance = props['allowance']
        self.major_dia_max = self.major_dia = props['max_major_dia'] * inch
        self.major_dia_min = props['min_major_dia'] * inch
        try:
            self.major_dia = props['min_dia'] * inch
        except:
            pass
        self.pitch_max = props['max_pitch']
        self.pitch_min = props['min_pitch']
        self.minor_dia = props['minor_dia']

    def __str__(self):
        string = self.size + '-' + self.threads_per_inch + ' ' + self.series + ', Class ' + self.fit_class
        return string

class UnifiedThreadRegistry(object):
    def __init__(self):
        UST_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'unified_screw_threads.csv')
        df = pd.read_csv(UST_PROPS)
        names = df['size'].tolist()
        classes = df['fit_class'].tolist()
        for (name, fitclass) in zip(names, classes): # TODO: figure this out
            thread = UnifiedScrewThread(name, fitclass)
            attr_name = (name + '_' + fitclass).replace('-', '_').replace(' ', '_')
            setattr(self, attr_name, thread)

if __name__ == '__main__':
    screw = UnifiedScrewThread('1 3/16-16 UN', '3A')
    print(screw)
    screw_reg = UnifiedThreadRegistry()
    print(screw_reg.__dict__.keys())