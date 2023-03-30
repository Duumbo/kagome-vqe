from scipy.sparse import csr_matrix

# Quelques définitions
sigma_x = csr_matrix(([1, 1], ([0, 1], [1, 0])), shape=(2, 2))
sigma_y = csr_matrix(([-1j, 1j], ([0, 1], [1, 0])), shape=(2, 2))
sigma_z = csr_matrix(([1, -1], ([0, 1], [0, 1])), shape=(2, 2))
sigma_0 = csr_matrix(([1, 1], ([0, 1], [0, 1])), shape=(2, 2))

sigma_p = csr_matrix(([2], ([0], [1])), shape=(2, 2))
sigma_m = csr_matrix(([2], ([1], [0])), shape=(2, 2))

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

