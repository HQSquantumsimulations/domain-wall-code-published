import functools
import itertools
import operator

import numpy as np

from qecsim.model import cli_description
from qecsim.models.color import Color666Code
from models.XXXZZZ import Color666PauliXXXZZZ


@cli_description('Color 6.6.6 (size INT odd >=3)')
class Color666CodeXXXZZZ(Color666Code):
    """
    Implements the X3Z3 code.
    """

    @property
    def label(self):
        """See :meth:`qecsim.model.StabilizerCode.label`"""
        return 'Color X3Z3 {}'.format(self.size)

    def new_pauli(self, bsf=None):
        """
        Convenience constructor of color 6.6.6 Pauli for this code.

        Notes:

        * For performance reasons, the new Pauli is a view of the given bsf. Modifying one will modify the other.

        :param bsf: Binary symplectic representation of Pauli. (Optional. Defaults to identity.)
        :type bsf: numpy.array (1d)
        :return: Color 6.6.6 Pauli
        :rtype: Color666Pauli
        """
        return Color666PauliXXXZZZ(self, bsf)
