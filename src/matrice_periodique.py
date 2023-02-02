import numpy as np
from scipy.sparse import kron, csr_matrix
from tqdm import tqdm


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

# Quelques définitions
sigma_x = csr_matrix(([1, 1], ([0, 1], [1, 0])), shape=(2, 2))
sigma_y = csr_matrix(([-1j, 1j], ([0, 1], [1, 0])), shape=(2, 2))
sigma_z = csr_matrix(([1, -1], ([0, 1], [0, 1])), shape=(2, 2))
sigma_0 = csr_matrix(([1, 1], ([0, 1], [0, 1])), shape=(2, 2))

sigma_p = csr_matrix(([1], ([0], [1])), shape=(2, 2))
sigma_m = csr_matrix(([1], ([1], [0])), shape=(2, 2))

# Map du réseau
reseau ={
        0: [1, 3, 4, 10],
        1: [2, 4, 11],
        2: [3, 5, 11],
        3: [5, 10],
        4: [6, 9],
        5: [7, 8],
        6: [7, 9, 10],
        7: [8, 10],
        8: [9, 11],
        9: [11]
}

# Gen la matrice
def gen_matrice() -> csr_matrix:
    ham = csr_matrix((2**12, 2**12), dtype=float)
    for i, val in tqdm(reseau.items()):
        splus = sigma_p.copy()
        smoins = sigma_m.copy()
        zz = sigma_z.copy()
        l = 0
        while(i > l):
            splus = kron(sigma_0, splus)
            smoins = kron(sigma_0, smoins)
            zz = kron(sigma_0, zz)
            l += 1
        k = i
        for n, j in enumerate(val):
            tmplus = splus.copy()
            tmoins = smoins.copy()
            tmzz = zz.copy()
            for m in range(11 - i):
                if j != k:
                    tmplus = kron(tmplus, sigma_0)
                    tmoins = kron(tmoins, sigma_0)
                    tmzz = kron(tmzz, sigma_0)
                if j == k:
                    tmplus = kron(tmplus, sigma_m)
                    tmoins = kron(tmoins, sigma_p)
                    tmzz = kron(tmzz, sigma_z)
                k += 1
            ham += tmplus
            ham += tmoins
            ham += tmzz
    return ham

