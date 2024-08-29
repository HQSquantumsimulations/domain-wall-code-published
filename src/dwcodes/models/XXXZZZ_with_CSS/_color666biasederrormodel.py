import functools
import math
import numpy as np

from qecsim import paulitools as pt
from qecsim.model import cli_description
from qecsim.models.generic import SimpleErrorModel


@cli_description('Biased (bias FLOAT > 0, [axis] CHAR)')
class PhaseFlipErrorModel(SimpleErrorModel):
    """
    EFFECTIVE ERROR MODEL FOR SIMULATING THE XXXZZZ CODE
    * The XXXZZZ code is simulated with the CSS code and effective error model
    by interchanging X and Z errors along odd diagonals.
    """

    def __init__(self):
        """
        Initialise new biased-depolarizing error model.

        :param bias: Bias in favour of axis errors relative to  off-axis errors.
        :type bias: float
        :param axis: Axis towards which the noise is biased (default='Y', values='X', 'Y', 'Z')
        :type axis: str
        :raises ValueError: if bias is not > 0.
        :raises ValueError: if axis is not in ('X', 'Y', 'Z') (lowercase accepted).
        :raises TypeError: if any parameter is of an invalid type.
        """

    @functools.lru_cache()
    def probability_distribution(self, probability):
        """See :meth:`qecsim.model.ErrorModel.probability_distribution`"""
        p_x = p_y = 0
        p_z = probability
        p_i = 1 - probability
        return p_i, p_x, p_y, p_z

    def generate(self, code, probability, rng=None):
        """
        See :meth:`qecsim.model.ErrorModel.generate`

        Notes:

        * This method delegates to :meth:`probability_distribution` to find the probability of I, X, Y, Z operators on
          each qubit, assuming an IID error model.
        """
        rng = np.random.default_rng() if rng is None else rng
        ep = []
        prob = self.probability_distribution(probability)
        for index in code._site_indices:
            row, col = index
            if col % 2 == 0 and (row + col) % 3 == 1:
                    qubit_error = rng.choice(('I', 'X', 'Y', 'Z'), p=prob)
            elif col % 2 == 1 and (row + col) % 3 == 0:
                    qubit_error = rng.choice(('I', 'X', 'Y', 'Z'), p=prob)
            else:
                qubit_error = rng.choice(('I', 'Z', 'Y', 'X'), p=prob)
            ep.append(qubit_error)
        error = ''.join(ep)

        #return pt.pauli_to_bsf(error_pauli)
        return pt.pauli_to_bsf(error)

    @property
    def label(self):
        """See :meth:`qecsim.model.ErrorModel.label`"""
        return 'Phase-flip errors'


@cli_description('Biased (bias FLOAT > 0, [axis] CHAR)')
class BiasedDepolarizingErrorModel(PhaseFlipErrorModel):
    """
    EFFECTIVE ERROR MODEL FOR SIMULATING THE XXXZZZ CODE
    * The XXXZZZ code is simulated with the CSS code and effective error model
    by interchanging X and Z errors along odd diagonals.
    """

    def __init__(self, bias, axis='Z'):
        """
        Initialise new biased-depolarizing error model.

        :param bias: Bias in favour of axis errors relative to  off-axis errors.
        :type bias: float
        :param axis: Axis towards which the noise is biased (default='Y', values='X', 'Y', 'Z')
        :type axis: str
        :raises ValueError: if bias is not > 0.
        :raises ValueError: if axis is not in ('X', 'Y', 'Z') (lowercase accepted).
        :raises TypeError: if any parameter is of an invalid type.
        """
        try:  # paranoid checking for CLI
            if not (bias > 0 and math.isfinite(bias)):
                raise ValueError('{} valid bias values are number > 0'.format(type(self).__name__))
            if axis not in ('x', 'y', 'z', 'X', 'Y', 'Z'):
                raise ValueError("{} valid axis values are ('X', 'Y', 'Z')".format(type(self).__name__))
        except TypeError as ex:
            raise TypeError('{} invalid parameter type'.format(type(self).__name__)) from ex
        self._bias = bias
        self._axis = axis.upper()

    @property
    def bias(self):
        """
        Bias.

        :rtype: float
        """
        return self._bias

    @property
    def axis(self):
        """
        Axis.

        :rtype: str
        """
        return self._axis

    @functools.lru_cache()
    def probability_distribution(self, probability):
        """See :meth:`qecsim.model.ErrorModel.probability_distribution`"""
        # low and high-rate error probabilities
        p_lr = 1 / (2 * (self._bias + 1)) * probability
        p_hr = self._bias / (self._bias + 1) * probability
        # along given axis
        if self.axis == 'X':
            p_x, p_y, p_z = p_hr, p_lr, p_lr
        elif self.axis == 'Y':
            p_x, p_y, p_z = p_lr, p_hr, p_lr
        elif self.axis == 'Z':
            p_x, p_y, p_z = p_lr, p_lr, p_hr
        # with no-error sum to 1
        p_i = 1 - sum((p_x, p_y, p_z))
        return p_i, p_x, p_y, p_z

    @property
    def label(self):
        """See :meth:`qecsim.model.ErrorModel.label`"""
        return 'Biased-depolarizing, efficient model for XXXZZZ (bias={!r}, axis={!r})'.format(self._bias, self._axis)

    def __repr__(self):
        return '{}({!r}, {!r})'.format(type(self).__name__, self._bias, self._axis)

