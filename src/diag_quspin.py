from quspin.operators import hamiltonian
from quspin.basis import spin_basis_general
import numpy as np

##### define model parameters #####
L = 12  # system size
J_0 = -1.0  # interaction
hz = 1.0  # z external field

##### set up Heisenberg Hamiltonian in an external z-field #####
# compute spin-1/2 basis
#basis = spin_basis_1d(L,pauli=False)
#basis = spin_basis_1d(L,pauli=False,Nup=L//2) # zero magnetisation sector
basis = spin_basis_general(L, S="1/2", pauli=-1)  # and positive parity sector

# define operators with OBC using site-coupling lists
lattice = [
    (0, 1), (0, 2), (0, 4), (0, 11),
    (1, 2), (1, 3), (1, 8),
    (2, 10), (2, 6),
    (3, 4), (3, 5), (3, 8),
    (4, 5), (4, 11),
    (5, 7), (5, 9),
    (6, 7), (6, 8), (6, 10),
    (7, 8), (7, 9),
    (9, 10), (9, 11)
]
J = [[J_0, i, j] for i, j in lattice]  # OBC
h_z = [[hz, i] for i in range(L)]

# static and dynamic lists
static = [["+-", J], ["-+", J], ["zz", J]]  #, ["z", h_z]]
dynamic = []

# compute the time-dependent Heisenberg Hamiltonian
H_XXZ = hamiltonian(static, dynamic, basis=basis, dtype=np.float64)


# calculate minimum and maximum energy only
Emin = H_XXZ.eigsh(k=10, which="SA", return_eigenvectors=False)
print(Emin)

# calculate the eigenstate closest to energy E_star
E_star = 0.0
E, psi_0 = H_XXZ.eigsh(k=1, sigma=E_star, maxiter=1E4)
psi_0 = psi_0.reshape((-1,))
