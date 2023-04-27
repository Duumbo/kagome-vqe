import qiskit as qs
import numpy as np

qc = qs.QuantumCircuit(2)
thet1 = qs.circuit.Parameter(r"\theta_1")
thet2 = qs.circuit.Parameter(r"\theta_2")
thet3 = qs.circuit.Parameter(r"\theta_3")
thet4 = qs.circuit.Parameter(r"\theta_4")
phi1 = qs.circuit.Parameter(r"\phi_1")
phi2 = qs.circuit.Parameter(r"\phi_2")
phi3 = qs.circuit.Parameter(r"\phi_3")
phi4 = qs.circuit.Parameter(r"\phi_4")
qc.h([0, 1])
qc.u(np.pi/2, thet1, phi1, 0)
qc.u(np.pi/2, thet2, phi2, 1)
qc.cx(0, 1)

qc.u(np.pi/2, thet3, phi3, 0)
qc.u(np.pi/2, thet4, phi4, 1)

qc.draw("latex_source", filename="ansatz2.tex")
