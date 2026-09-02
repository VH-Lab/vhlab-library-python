"""Unit tests for the MEASUREDDATA interval accessors.

Ported from AnalysisTools/MeasuredData/@measureddata/get_intervals.m and
set_intervals.m. NDI-matlab calls get_intervals on cells loaded from a VH lab
experiment file (`+ndi/+setup/+conv/+vhlab/importMeasuredDataCells.m`), and in
Python those cells arrive as dicts or as .mat structs rather than as
MeasuredData objects, so the module-level wrappers accept all three.
"""

import unittest

import numpy as np

from vhlib.md import MeasuredData, get_intervals, set_intervals


class MatStructLike:
    """Stands in for a scipy mat_struct: attributes, not dict keys."""

    def __init__(self, intervals):
        self.intervals = intervals


class TestMeasuredDataIntervalMethods(unittest.TestCase):

    def setUp(self):
        self.intervals = np.array([[0.0, 10.0], [20.0, 30.0]])
        self.md = MeasuredData(self.intervals, 'a long description', 'brief')

    def test_get_intervals_returns_the_intervals(self):
        np.testing.assert_array_equal(self.md.get_intervals(), self.intervals)

    def test_set_intervals_replaces_them(self):
        new = np.array([[1.0, 2.0]])
        returned = self.md.set_intervals(new)

        np.testing.assert_array_equal(self.md.get_intervals(), new)
        # MATLAB returns a new object; Python mutates and returns self, as the
        # other MeasuredData methods do, so the MATLAB idiom still reads right.
        self.assertIs(returned, self.md)

    def test_set_intervals_does_not_disturb_the_associates(self):
        self.md.associate('trials', 'test', [1, 2, 3], 'trial numbers')
        self.md.set_intervals(np.array([[5.0, 6.0]]))

        self.assertEqual(self.md.numassociates(), 1)


class TestIntervalWrappers(unittest.TestCase):

    def setUp(self):
        self.intervals = np.array([[0.0, 10.0], [20.0, 30.0]])
        self.new = np.array([[3.0, 4.0]])

    def test_measureddata_object(self):
        md = MeasuredData(self.intervals)
        np.testing.assert_array_equal(get_intervals(md), self.intervals)
        np.testing.assert_array_equal(get_intervals(set_intervals(md, self.new)),
                                      self.new)

    def test_dict(self):
        cell = {'intervals': self.intervals, 'associates': []}
        np.testing.assert_array_equal(get_intervals(cell), self.intervals)

        returned = set_intervals(cell, self.new)
        self.assertIs(returned, cell)
        np.testing.assert_array_equal(cell['intervals'], self.new)

    def test_mat_struct(self):
        cell = MatStructLike(self.intervals)
        np.testing.assert_array_equal(get_intervals(cell), self.intervals)

        set_intervals(cell, self.new)
        np.testing.assert_array_equal(cell.intervals, self.new)

    def test_dict_without_intervals_raises(self):
        with self.assertRaises(ValueError):
            get_intervals({'associates': []})

    def test_object_without_intervals_raises(self):
        with self.assertRaises(ValueError):
            get_intervals(object())
        with self.assertRaises(ValueError):
            set_intervals(object(), self.new)


if __name__ == '__main__':
    unittest.main()
