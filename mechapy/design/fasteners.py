"""Contains classes and registries for screw threads and grades"""

import os
import math

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
        try:
            self.threads_per_inch = float(props['size'].split('-')[1].split(' U')[0]) * inch ** -1
        except ValueError:
            if props['size'].split('-')[1].split(' U')[0] == '4 1/2':  # Edge case in table data
                self.threads_per_inch = 4.5 * inch ** -1
            else:
                raise
        self.series = props['size'].split(' ')[-1]
        self.fit_class = props['fit_class']
        self.allowance = props['allowance']
        self.major_dia_max = self.major_dia = float(props['max_major_dia']) * inch
        self.major_dia_min = props['min_major_dia'] * inch
        try:
            self.min_dia = props['min_dia'] * inch
        except:
            pass
        self.pitch_max = self.pitch = props['max_pitch']
        self.pitch_min = props['min_pitch']
        self.minor_dia = props['minor_dia']
        self.stress_area = (math.pi / 4) * (self.major_dia - 0.938194 / self.threads_per_inch) ** 2

    def __str__(self):
        string = 'Unified Screw Thread: ' + self.size + '-' + str(self.threads_per_inch) + ' ' +\
                 self.series + ', Class ' + self.fit_class
        return string

class MetricThread(object):
    def __init__(self, size):
        MT_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'metric_screw_threads.csv')
        df = pd.read_csv(MT_PROPS)
        props = df.loc[(df['size'] == size)].to_dict(orient='records')[0]
        self.size = props['size']
        self.pitch = props['pitch']
        self.major_dia = props['major_dia'] * mm
        self.minor_dia = props['minor_dia'] * mm
        self.stress_area = props['stress_area'] * (mm ** 2)

    def __str__(self):
        string = 'Metric Screw Thread: ' + self.size
        return string

class UnifiedThreadRegistry(object):
    def __init__(self):
        UST_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'unified_screw_threads.csv')
        df = pd.read_csv(UST_PROPS)
        names = df['size'].tolist()
        classes = df['fit_class'].tolist()
        for name, fitclass in zip(names, classes): # TODO: figure this out
            thread = UnifiedScrewThread(name, fitclass)
            attr_name = 'thread_' + (name + '_' + fitclass)\
                .replace('-', '_')\
                .replace(' ', '_')\
                .lower()
            setattr(self, attr_name, thread)

    def add_custom_thread(self, props):
        pass

class MetricThreadRegistry(object):
    """Registry for common external metric threads

    Examples
    --------
    >>> mreg = MetricThreadRegistry()
    """
    def __init__(self):
        UST_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'unified_screw_threads.csv')
        df = pd.read_csv(UST_PROPS)
        names = df['size'].tolist()
        classes = df['fit_class'].tolist()
        for name, fitclass in zip(names, classes):
            thread = UnifiedScrewThread(name, fitclass)
            attr_name = 'thread_' + (name + '_' + fitclass)\
                .replace('-', '_')\
                .replace(' ', '_')\
                .lower()
            setattr(self, attr_name, thread)

class SteelScrewGrade(object):
    """Common class for imperial and SI steel screw SAE grades

    Parameters
    ----------
    grade : int or float
        Examples = 8 or 9.8
    """
    def __init__(self, grade):
        GRADE_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'steel_screw_grades.csv')
        df = pd.read_csv(GRADE_PROPS)
        props = df.loc[(df['sae'] == grade)].to_dict(orient='records')[0]
        self.sae_grade = props['sae']
        if props['unit'] == 'mm':
            pressure = MPa
            length = mm
        else:
            pressure = ksi
            length = inch
        self.diameter_min = props['diameter_min'] * length
        self.diameter_max = props['diameter_max'] * length
        self.proof_load = props['proof_load'] * pressure
        self.yield_strength = props['yield_strength'] * pressure
        self.tensile_strength = props['tensile_strength'] * pressure
        self.elongation = props['elongation_min']
        self.area_reduction_min = props['area_red_min']
        self.rockwell_hardness_min = props['rockwell_min']
        self.rockwell_hardness_max = props['rockwell_max']

class ScrewGradeRegistry(object):
    def __init__(self):
        GRADE_PROPS = os.path.join(os.path.dirname(__file__), 'data', 'steel_screw_grades.csv')
        df = pd.read_csv(GRADE_PROPS)
        names = df['sae'].tolist()
        print(names)
        for name in names:
            thread = SteelScrewGrade(name)
            if name % 1 == 0:
                name = int(name)  # Drop decimal place for imperial grades
            attr_name = 'sae_' + str(name).replace('.', '_')
            setattr(self, attr_name, thread)

class Screw(object):
    """Component class with dependencies on thread and grade-related objects"""
    def __init__(self, thread, grade, length):
        if not isinstance(MetricThread, UnifiedScrewThread):
            raise TypeError("Thread must be instance of 'MetricThread' or 'UnifiedScrewThread'")
        self.thread = thread
        self.grade = grade
        self.length = length


if __name__ == '__main__':
    screw = UnifiedScrewThread('1 3/16-16 UN', '3A')
    print(screw)
    print(screw.__dict__)
    screw_reg = UnifiedThreadRegistry()
    print(screw_reg.__dict__.keys())
    metric_screw = MetricThread('M30 X 3.5')
    print(metric_screw)
    print(metric_screw.__dict__)
    screw_reg_metric = MetricThreadRegistry()
    print(screw_reg_metric.__dict__.keys())
    metric_grade = SteelScrewGrade(9.8)
    print(metric_grade.__dict__)
    grade_reg = ScrewGradeRegistry()
    print(grade_reg.__dict__.keys())