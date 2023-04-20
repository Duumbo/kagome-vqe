import numpy as np
import matplotlib.pyplot as plt
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator
from qiskit.circuit.library import ZFeatureMap, PauliFeatureMap, ZZFeatureMap
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import ParameterVector, Parameter
from scipy.optimize import minimize
from pauli import reseau


gs = np.load("Data/ground_state.npy")
# Test ground state
test_gs = QuantumCircuit(12)
test_gs.initialize(gs[:, 0], range(12))

# Ansatz
# 1 param par qubit et un param par liaison
"""
--u(x1)--*--*
         |  |
--u(x2)--x--|
--u(x3)-----x
"""
N = 12

# Ansatz 1
qc = QuantumCircuit(N)
pz = ParameterVector("z_param", N)
pz2 = ParameterVector("z_param2", N)
for i in range(N):
    qc.h(i)
    qc.p(pz.params[i], i)
param_list = []
for i, voisins in reseau.items():
    for j in voisins:
        qc.cx(i, j)
for i in range(N):
    qc.p(pz2.params[i], i)

# Ansatz 2
qc_1 = QuantumCircuit(N)
pz_1 = ParameterVector("z_param", N)
px = ParameterVector("x_param", N)
pz2_1 = ParameterVector("z_param2", N)
px2 = ParameterVector("x_param2", N)
for i in range(N):
    qc_1.h(i)
    qc_1.u(np.pi/2, px.params[i], pz_1.params[i], i)
param_list_1 = []
for i, voisins in reseau.items():
    for j in voisins:
        qc_1.cx(i, j)
for i in range(N):
    qc_1.u(np.pi/2, px2.params[i], pz2_1.params[i], i)

# Gen Ham
"""
H=sum_{<i,j>}(S_ixS_jx+S_iyS_jy)+S_izS_jz
"""
pauli_strings = []
for i, voisins in reseau.items():
    for j in voisins:
        pauli_string_z = "".join(["Z" if (k==i) or (k==j) else "I" for k in range(N)][::-1])
        pauli_string_x = "".join(["X" if (k==i) or (k==j) else "I" for k in range(N)][::-1])
        pauli_string_y = "".join(["Y" if (k==i) or (k==j) else "I" for k in range(N)][::-1])
        pauli_strings.append(pauli_string_z)
        pauli_strings.append(pauli_string_x)
        pauli_strings.append(pauli_string_y)

for i, ansatz in enumerate([qc, ZFeatureMap(12, reps=2), PauliFeatureMap(12, reps=2), ZFeatureMap(12, reps=2), qc_1]):
    with open(f"output_{i}.txt", "w") as fp:
        it = []
        exp = []
        def callback_inter(nb_eval: int, params: np.ndarray, mean: float, meta: dict
                           ) -> None:
            it.append(nb_eval)
            exp.append(mean)
        H = SparsePauliOp(pauli_strings)
        estimator = Estimator(observables=H)
        vqe = VQE(estimator, ansatz, minimize, callback=callback_inter)
        fp.write(vqe.compute_minimum_eigenvalue(H).__str__())

        estimator = Estimator(circuits=test_gs, observables=H)
        fp.write(estimator.run(circuits=test_gs, observables=H).result().__str__())
        fp.write(np.load("Data/ground_energy.npy").__str__())
        np.save(f"Data/convergence_ansatz{i}.npy", np.array([it, exp]))
