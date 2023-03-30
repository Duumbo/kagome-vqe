import numpy as np
import matplotlib.pyplot as plt
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator
from qiskit.circuit.library import ZFeatureMap, PauliFeatureMap
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

qc = QuantumCircuit(N)
pz = ParameterVector("z_param", N)
pz2 = ParameterVector("z_param2", N)
for i in range(N):
    qc.h(i)
    qc.p(pz.params[i], i)
param_list = []
for i, voisins in reseau.items():
    for j in voisins:
        param_list.append(pl := Parameter(f"theta{i},{j}"))
        qc.cp(pl, i, j)
for i in range(N):
    qc.p(pz2.params[i], i)

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

with open("output.txt", "w") as fp:
    H = SparsePauliOp(pauli_strings)
    estimator = Estimator(observables=H)
    ansatz = ZFeatureMap(12, reps=2)
    vqe = VQE(estimator, qc, minimize)
    fp.write(vqe.compute_minimum_eigenvalue(H).__str__())

    estimator = Estimator(circuits=test_gs, observables=H)
    fp.write(estimator.run(circuits=test_gs, observables=H).result().__str__())
    fp.write(np.load("Data/ground_energy.npy").__str__())
