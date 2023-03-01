import numpy as np
from scipy.sparse import kron, csr_matrix
from tqdm import tqdm
from pauli import sigma_0, sigma_m, sigma_p, reseau, sigma_z


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

