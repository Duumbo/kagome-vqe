import numpy as np
import matrice_periodique as mat
from scipy.sparse.linalg import eigsh

ham = mat.gen_matrice()
w, v = eigsh(ham, k=1, which="SA")
print(w, v)
np.save("Data/ground_state.npy", v)
np.save("Data/ground_energy.npy", w)

