import numpy as np
from qecsim.models.color import Color666Pauli

class Color666PauliXXXXZZ(Color666Pauli):

    def operator(self, index):
        """
        Returns the operator on the site identified by the index.

        :param index: Index identifying a site in the format (row, column).
        :type index: 2-tuple of int
        :return: Pauli operator. One of 'I', 'X', 'Y', 'Z'.
        :rtype: str
        :raises IndexError: If index is not an in-bounds site index.
        """
        # check valid in-bounds index
        if not (self.code.is_site(index) and self.code.is_in_bounds(index)):
            raise IndexError('{} is not an in-bounds site index for code of size {}.'.format(index, self.code.size))
        # extract binary x and z
        flat_index = self._flatten_site_index(index)
        x = self._xs[flat_index]
        z = self._zs[flat_index]
        # return Pauli
        if x == 1 and z == 1:
            return 'Y'
        elif x == 1:
            return 'X'
        elif z == 1:
            return 'Z'
        else:
            return 'I'

    def logical_z(self):
        """
        Apply a logical X operator, i.e. column of X along leftmost sites.

        Notes:

        * The column of X is applied to the leftmost column to allow optimisation of the MPS decoder.

        :return: self (to allow chaining)
        :rtype: Color666Pauli
        """
        for row in range(self.code.bound + 1):
            index = row, 0
            if self.code.is_site(index):
                self.site('X', index)
        return self

    def logical_x(self):
        """
        Apply a logical Z operator, i.e. column of Z along leftmost sites.

        Notes:

        * The column of Z is applied to the leftmost column to allow optimisation of the MPS decoder.

        :return: self (to allow chaining)
        :rtype: Color666Pauli
        """
        for row in range(self.code.bound + 1):
            index = row, 0
            if self.code.is_site(index):
                self.site('Z', index)
        return self