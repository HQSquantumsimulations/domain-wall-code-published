import numpy as np
from qecsim.models.color import Color666Pauli

class Color666PauliXXXZZZ(Color666Pauli):
    """
    Defines a Pauli operator of the XXXZZZ code on a 6.6.6 lattice.

    DIFFERENCE WITH THE CSS CODE:
    * In 3 out of 6 stabilizers Xs and Zs have to be interchanged, see method:plaquette
    * Logical Xs and Zs have to be defined accordingly, see method:logical_x and method:logical_z

    """

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

    def plaquette(self, operator, index):
        """
        Apply a plaquette operator at the given index.

        Notes:

        * Index is in the format (row, column).
        * Parts of plaquettes that lie outside the lattice have no effect on the lattice.

        :param operator: Pauli operator. One of 'I', 'X', 'Y', 'Z'.
        :type operator: str
        :param index: Index identifying the plaquette in the format (row, column).
        :type index: 2-tuple of int
        :return: self (to allow chaining)
        :rtype: Color666Pauli
        :raises IndexError: If index is not a plaquette index.
        """
        r, c = index
        # check valid index
        if not self.code.is_plaquette(index):
            raise IndexError('{} is not a plaquette index.'.format(index))
        # flip plaquette sites

        if operator == 'X':
            if c % 2 == 0:
                self.site('X', (r - 1, c - 1), (r - 1, c), (r, c + 1))
                self.site('Z', (r, c - 1), (r + 1, c), (r + 1, c + 1))
            else:
                self.site('Z', (r - 1, c - 1), (r - 1, c), (r, c + 1))
                self.site('X', (r, c - 1), (r + 1, c), (r + 1, c + 1))
        else:
            if c % 2 == 1:
                self.site('X', (r - 1, c - 1), (r - 1, c), (r, c + 1))
                self.site('Z', (r, c - 1), (r + 1, c), (r + 1, c + 1))
            else:
                self.site('Z', (r - 1, c - 1), (r - 1, c), (r, c + 1))
                self.site('X', (r, c - 1), (r + 1, c), (r + 1, c + 1))
        return self

    def logical_x(self):
        """
        Apply a logical X operator, i.e. column of X along leftmost sites.

        Notes:

        * The column of X is applied to the leftmost column to allow optimisation of the MPS decoder.

        :return: self (to allow chaining)
        :rtype: Color666Pauli
        """
        i = 0
        for row in range(self.code.bound + 1):
            index = row, 0
            if self.code.is_site(index):
                if i % 2 == 0:
                    self.site('X', index)
                else:
                    self.site('Z', index)
                i = i + 1
        return self

    def logical_z(self):
        """
        Apply a logical Z operator, i.e. column of Z along leftmost sites.

        Notes:

        * The column of Z is applied to the leftmost column to allow optimisation of the MPS decoder.

        :return: self (to allow chaining)
        :rtype: Color666Pauli
        """
        i = 0
        for row in range(self.code.bound + 1):
            index = row, 0
            if self.code.is_site(index):
                if i % 2 == 0:
                    self.site('Z', index)
                else:
                    self.site('X', index)
                i = i + 1
        return self
