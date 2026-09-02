"""Unit tests for vhlib.response_stats.neural_response_significance.

Ported from AnalysisTools/ResponsesFitsIndexesPlotting/response_stats/
neural_response_significance.m, which reports the p value of a one-way ANOVA
across stimulus conditions, and a second p value that adds the blank condition
as one more group.
"""

import unittest

import numpy as np
from scipy import stats

from vhlib.response_stats import neural_response_significance


def anova_p(groups):
    """One-way ANOVA p value computed from the definition, as a cross-check."""
    groups = [np.asarray(g, dtype=float) for g in groups]
    k = len(groups)
    n = sum(g.size for g in groups)
    grand_mean = np.concatenate(groups).mean()

    ss_between = sum(g.size * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_within = sum(((g - g.mean()) ** 2).sum() for g in groups)

    f = (ss_between / (k - 1)) / (ss_within / (n - k))
    return float(stats.f.sf(f, k - 1, n - k))


class TestNeuralResponseSignificance(unittest.TestCase):

    def setUp(self):
        # Three stimulus conditions; the middle one drives a clear response.
        self.responsive = {
            'ind': [[1.0, 2.0, 1.5, 1.2],
                    [8.0, 9.0, 8.5, 8.2],
                    [1.2, 0.9, 1.1, 1.4]],
            'blankind': [0.1, 0.2, 0.15, 0.05],
        }
        # Three conditions that differ only by noise.
        self.unresponsive = {
            'ind': [[1.0, 2.0, 1.5, 1.2],
                    [1.1, 1.9, 1.6, 1.3],
                    [1.2, 1.8, 1.4, 1.1]],
            'blankind': [1.0, 1.7, 1.5, 1.3],
        }

    def test_significant_variation_is_detected(self):
        sigp, _ = neural_response_significance(self.responsive)
        self.assertLess(sigp, 0.01)

    def test_noise_alone_is_not_significant(self):
        sigp, sigpb = neural_response_significance(self.unresponsive)
        self.assertGreater(sigp, 0.05)
        self.assertGreater(sigpb, 0.05)

    def test_p_value_matches_a_one_way_anova_over_the_stimulus_groups(self):
        sigp, _ = neural_response_significance(self.responsive)
        self.assertAlmostEqual(sigp, anova_p(self.responsive['ind']), places=12)

    def test_blank_is_added_as_one_more_group(self):
        _, sigpb = neural_response_significance(self.responsive)
        expected = anova_p(self.responsive['ind'] + [self.responsive['blankind']])
        self.assertAlmostEqual(sigpb, expected, places=12)

    def test_without_a_blank_sigpb_equals_sigp(self):
        resp = {'ind': self.responsive['ind']}
        sigp, sigpb = neural_response_significance(resp)
        self.assertEqual(sigp, sigpb)

    def test_identical_groups_give_a_p_value_of_one(self):
        trials = [1.0, 2.0, 1.5, 1.2]
        sigp, _ = neural_response_significance({'ind': [trials, list(trials), list(trials)]})
        self.assertAlmostEqual(sigp, 1.0, places=12)

    def test_unequal_trial_counts_are_allowed(self):
        # MATLAB's resp.ind is a cell list, so conditions may have different
        # numbers of trials; the group membership vector is built per trial.
        resp = {'ind': [[1.0, 2.0, 1.5],
                        [8.0, 9.0],
                        [1.2, 0.9, 1.1, 1.4]]}
        sigp, sigpb = neural_response_significance(resp)
        self.assertAlmostEqual(sigp, anova_p(resp['ind']), places=12)
        self.assertEqual(sigp, sigpb)

    def test_numpy_arrays_are_accepted(self):
        resp = {'ind': [np.array(g) for g in self.responsive['ind']],
                'blankind': np.array(self.responsive['blankind'])}
        sigp, sigpb = neural_response_significance(resp)
        self.assertAlmostEqual(sigp, anova_p(self.responsive['ind']), places=12)
        self.assertLess(sigpb, sigp)

    def test_fewer_than_two_groups_raises(self):
        with self.assertRaises(ValueError):
            neural_response_significance({'ind': [[1.0, 2.0, 1.5]]})

    def test_missing_ind_raises(self):
        with self.assertRaises(ValueError):
            neural_response_significance({'spont': [1.0, 0.1, 0.05]})

    def test_empty_group_raises(self):
        with self.assertRaises(ValueError):
            neural_response_significance({'ind': [[1.0, 2.0], []]})


if __name__ == '__main__':
    unittest.main()
