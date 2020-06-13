from qiskit import IBMQ, QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram

from preprocessing import preprocess
from quantum import config_circuit, grovers_search


if __name__ == "__main__":
    preprocess("../data/gspc/^GSPC-feb-2020-corona-daily.csv")

    with open("ibmg_token.txt", 'r') as token_file:
        token = token_file.read_line()
    IBMQ.save_account(token)

    # specify any other IBM Q backend you want to use
    simulator = Aer.get_backend('qasm_simulator')

    circuit = QuantumCircuit(3, 3)

    config_circuit(circuit, "results/circuit_config.csv")
