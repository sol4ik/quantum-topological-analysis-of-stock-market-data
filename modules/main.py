from qiskit import IBMQ, QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram

from preprocessing import preprocess
from quantum import config_circuit, distances, persistence_homology


if __name__ == "__main__":
    preprocess("../data/gspc/^GSPC-feb-2020-corona-daily.csv")

    with open("ibmg_token.txt", 'r') as token_file:
        token = token_file.read_line()
    IBMQ.save_account(token)

    # specify any other IBM Q backend you want to use
    simulator = Aer.get_backend('qasm_simulator')

    with open("result/circuit_config.csv") as conf_file:
        n_qubits = len(conf_file.readlines()) - 1

    circuit = QuantumCircuit(n_qubits, n_qubits)

    # data preparation
    config_circuit(circuit, "results/circuit_config.csv")
    distances(circuit, n_qubits)

    # persistence homology calculations
    persistence_homology(circuit, n_qubits)

    # run IBM Q circuit and get results
    job = execute(circuit, simulator, shots=1000)

    result = job.result()
    counts = result.get_counts(circuit)
    # print("\nTotal count for states are:", counts)
    plot_histogram(counts)

    # postprocess the results
