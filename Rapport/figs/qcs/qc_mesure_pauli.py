import qiskit as qs

qc = qs.QuantumCircuit(1)
qc.measure_all()
qc.draw("latex_source", filename="measure_z.tex")

qc = qs.QuantumCircuit(1)
qc.h(0)
qc.measure_all()
qc.draw("latex_source", filename="measure_x.tex")

qc = qs.QuantumCircuit(1)
qc.sdg(0)
qc.h(0)
qc.measure_all()
qc.draw("latex_source", filename="measure_y.tex")
