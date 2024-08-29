import functools
import itertools
from qecsim.model import cli_description
from qecsim.models.color import Color666Code
from models.XXZXXZ_with_CSS import Color666PauliXXZXXZ


@cli_description('Color 6.6.6 (size INT odd >=3)')
class Color666CodeXXZXXZ(Color666Code):
    """
    CSS color code. In conjunction with the effective error model, simulates the XXZXXZ code.
    """

    @property
    @functools.lru_cache()
    def _site_indices(self):
        """
        Return a list of the site indices of the lattice.

        Notes:

        * Each index is in the format (row, column).
        * Indices are in order of increasing column and row.

        :return: List of indices in the format (row, column).
        :rtype: list of 2-tuple of int
        """
        return [i for i in itertools.product(range(self.bound + 1), repeat=2)
                if self.is_in_bounds(i) and self.is_site(i)]

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
        return Color666PauliXXZXXZ(self, bsf)
