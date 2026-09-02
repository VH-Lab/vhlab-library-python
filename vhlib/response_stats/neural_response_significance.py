import numpy as np
from scipy import stats


def _anova1(groups):
    """
    One-way ANOVA over a list of 1-D arrays, returning the p value only.

    Stands in for MATLAB's ANOVA1(VALS, GROUPMEM, 'off'), which returns the
    p value of an F test across the groups.
    """
    if len(groups) < 2:
        raise ValueError('neural_response_significance needs at least two '
                         'groups of trial responses; got %d.' % len(groups))
    for i, g in enumerate(groups):
        if g.size == 0:
            raise ValueError('group %d has no trials.' % i)

    return float(stats.f_oneway(*groups).pvalue)


def neural_response_significance(resp):
    """
    Computes significance of response variation

    [SIGP, SIGPB] = NEURAL_RESPONSE_SIGNIFICANCE(RESP)

    :param resp: dict of response properties with fields:

        curve     | 4 x number of stimulus conditions tested;
                  |   curve[0] is the stimulus parameter values tested,
                  |   curve[1] is mean responses,
                  |   curve[2] is standard deviation,
                  |   curve[3] is standard error
        ind       | list of individual trial responses for each stimulus
        spont     | spontaneous responses [mean stddev stderr]
        spontind  | individual spontaneous responses

        Optionally:
        blankresp | response to a blank trial: [mean stddev stderr]
        blankind  | individual responses to blank

        Only 'ind' and, when present, 'blankind' are read here.

    :return: tuple (sigp, sigpb)

        sigp is the P value of an ANOVA across all stimulus conditions.
        sigpb is the P value of an ANOVA across all stimulus conditions,
        including the blank if it is available. If it is not available, then
        this is identical to sigp.
    """
    if 'ind' not in resp:
        raise ValueError("resp has no 'ind' field of individual trial responses.")

    groups = [np.asarray(trials, dtype=float).reshape(-1) for trials in resp['ind']]

    sigp = _anova1(groups)

    blankind = resp.get('blankind') if hasattr(resp, 'get') else None
    if blankind is None:
        sigpb = sigp
    else:
        blank = np.asarray(blankind, dtype=float).reshape(-1)
        sigpb = _anova1(groups + [blank])

    return sigp, sigpb
