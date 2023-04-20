import numpy as np
from scipy.sparse import kron, csr_matrix, eye
from tqdm import tqdm
from pauli import sigma_x, sigma_y, sigma_z, reseau, sigma_0


"""
Diagonalisation exacte du réseau Kagome avec l'Hamiltonien de Heisenberg.
Soit l'Hamiltonien de Heisenberg
$$
H=-J\sum_{\left<i,j\right>}\sigma_i\sigma_j-h
$$
On peut le réécrire
$$
H=-J\sum_{<i,j>}\qty(2\qty(\sigma_i^+\sigma_j^-+\sigma_i^-\sigma_j^+)+\sigma_i^z\sigma_j^z)
$$
"""

# Gen la matrice
def gen_matrice() -> csr_matrix:
    ham_z = eye(1, dtype=float)
    ham_x = eye(1, dtype=float)
    ham_y = eye(1, dtype=float)
    ham = csr_matrix((2**12, 2**12), dtype=float)
    for i, val in tqdm(reseau.items()):
        for j in val:
            l = 11
            while l != -1:
                if l == i:
                    ham_z = kron(ham_z, sigma_z)
                    ham_x = kron(ham_x, sigma_x)
                    ham_y = kron(ham_y, sigma_y)
                elif l == j:
                    ham_z = kron(ham_z, sigma_z)
                    ham_x = kron(ham_x, sigma_x)
                    ham_y = kron(ham_y, sigma_y)
                else:
                    ham_z = kron(ham_z, sigma_0)
                    ham_x = kron(ham_x, sigma_0)
                    ham_y = kron(ham_y, sigma_0)
                l -= 1
            print(ham)
            ham = ham + ham_y + ham_z + ham_x
            ham_z = eye(1, dtype=float)
            ham_x = eye(1, dtype=float)
            ham_y = eye(1, dtype=float)
    return ham

