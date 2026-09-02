"""Unit tests for vhlib.StimDecode.getstimscript.

Ported from StimulusDecoding/getstimscript.m, which loads the NewStim
stimscript ('saveScript') and the measured timing information ('MTI2') from a
stims.mat file in a recording directory.

MATLAB writes 'saveScript' as a NewStim `stimscript` object, which scipy cannot
reconstruct; these tests stand a struct in its place, so what is checked is the
directory logic, the error behaviour, and that both variables come back — not a
NewStim object model that does not exist in Python yet.
"""

import os
import shutil
import tempfile
import unittest

import numpy as np
from scipy import io as sio

from vhlib.StimDecode import getstimscript


def write_stims_mat(dirname, **variables):
    """Write a stims.mat holding the given variables."""
    sio.savemat(os.path.join(dirname, 'stims.mat'), variables)


class TestGetStimScript(unittest.TestCase):

    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dirname, True)

    def test_reads_savescript_and_mti2(self):
        write_stims_mat(self.dirname,
                        saveScript={'displayOrder': np.array([1, 2, 3, 1, 2, 3])},
                        MTI2=[{'startStopTimes': np.array([1.0, 1.5, 3.5, 4.0])},
                              {'startStopTimes': np.array([5.0, 5.5, 7.5, 8.0])}])

        thestimscript, mti = getstimscript(self.dirname)

        np.testing.assert_array_equal(thestimscript.displayOrder,
                                      np.array([1, 2, 3, 1, 2, 3]))
        self.assertEqual(len(mti), 2)
        np.testing.assert_allclose(mti[0].startStopTimes,
                                   np.array([1.0, 1.5, 3.5, 4.0]))
        np.testing.assert_allclose(mti[1].startStopTimes,
                                   np.array([5.0, 5.5, 7.5, 8.0]))

    def test_trailing_separator_is_accepted(self):
        # MATLAB's fixpath() makes 'dir' and 'dir/' equivalent.
        write_stims_mat(self.dirname, saveScript={'displayOrder': np.array([1])},
                        MTI2=[{'startStopTimes': np.array([0.0, 1.0])}])

        thestimscript, mti = getstimscript(self.dirname + os.sep)

        np.testing.assert_array_equal(thestimscript.displayOrder, np.array([1]))

    def test_missing_directory_raises(self):
        missing = os.path.join(self.dirname, 'no_such_directory')
        with self.assertRaises(FileNotFoundError) as caught:
            getstimscript(missing)
        self.assertIn('does not exist', str(caught.exception))

    def test_directory_without_stims_mat_raises(self):
        with self.assertRaises(FileNotFoundError) as caught:
            getstimscript(self.dirname)
        self.assertIn('No stims', str(caught.exception))

    def test_stims_mat_without_the_expected_variables_raises(self):
        write_stims_mat(self.dirname, someOtherVariable=np.array([1, 2, 3]))
        with self.assertRaises(KeyError) as caught:
            getstimscript(self.dirname)
        self.assertIn('saveScript', str(caught.exception))
        self.assertIn('MTI2', str(caught.exception))

    def test_stims_mat_missing_only_mti2_raises(self):
        write_stims_mat(self.dirname, saveScript={'displayOrder': np.array([1])})
        with self.assertRaises(KeyError) as caught:
            getstimscript(self.dirname)
        self.assertIn('MTI2', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
