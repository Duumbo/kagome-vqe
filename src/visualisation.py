import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import kron, csr_matrix
from pauli import sigma_x, sigma_y, sigma_z, sigma_0
"""
Visualization of the ground state.
"""
w, v = np.load("Data/ground_energy.npy"), np.load("Data/ground_state.npy")
v = csr_matrix(v)

# Get Observables
def observable_chain(observable):
    obx = []
    l = 0
    for i in range(12):
        obs = observable.copy()
        for j in range(12):
            if j > l:
                obs = kron(obs, sigma_0)
            if j < l:
                obs = kron(sigma_0, obs)
        l += 1
        obx.append(obs)
    return obx


# Get all sigma_z
def exp_value_obs(observable):
    obs_chain = observable_chain(observable)
    exp_val = []
    for obs in obs_chain:
        s = obs.dot(v)
        l = v.transpose().dot(s)
        exp_val.append(complex(l.toarray()).real)
    return exp_val

proj_x = exp_value_obs(sigma_x)
proj_y = exp_value_obs(sigma_y)
proj_z = exp_value_obs(sigma_z)

x = [0, 1, 2, 3, 0.5, 2.5, 1, 2, 3, 4, 1.5, 3.5]
y = [0, 0, 0, 0, np.sqrt(3)/2, np.sqrt(3)/2, np.sqrt(3), np.sqrt(3), np.sqrt(3), np.sqrt(3), 3*np.sqrt(3)/2, 3 *np.sqrt(3)/2]

fig, ax = plt.subplots()
ax.plot(x, y, "o", markersize=12)
ax.quiver(x, y, proj_x, proj_y)

fig.savefig("Images/spins_periodique.png")
