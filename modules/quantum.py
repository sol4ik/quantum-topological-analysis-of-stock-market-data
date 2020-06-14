from qiskit import QuantumCircuit

from numpy import pi


def config_circuit(circuit, config_file):
    """
    Config quantum circuit.
    Set scaled distances between data points.
    :param circuit: IBM G circuit object
    :param config_file: file to read configurations from
    """
    # counter for quantum bits
    q = 0

    with open(config_file, 'r') as file:
        for line in file.read_lines()[1:]:
            comma = line.index(',')
            a = float(line[:comma])
            b = float(line[comma + 1:])

            circuit.u2(pi * a, pi * b, q)
            q += 1

    # test case
    # circuit.u3(pi * 0.5, pi * 0.5, pi * 0.5, 0)
    # circuit.u3(pi / 2, pi / 2, pi / 2, 1)
    # circuit.u3(pi / 2, pi / 2, pi / 2, 2)


def grovers_search(circuit):
    """
    IBM Q implementation of Grover's search algorithm with multiple solutions
    implemented on 3 qubits.
    Needed to construct simplicial complex for data analysis.
    :param circuit: IBM Q circuit object 
    """
    circuit.x(0)
    circuit.x(1)
    circuit.x(2)

    circuit.h(0)
    circuit.cx(1, 0)
    circuit.cx(2, 0)

    circuit.h(0)
    circuit.id(1)
    circuit.id(2)

    circuit.x(0)
    circuit.x(1)
    circuit.x(2)

    circuit.h(0)
    circuit.h(1)
    circuit.h(2)

    # circuit.measure([0, 1], [0, 1])


if __name__ == "__main__":
    with open("ibmq_token.txt", 'r') as token_file:
        token = token_file.readlines()[0]
    IBMQ.save_account(token)
    
    # specify any other IBM Q backend ypu want to use
    simulator = Aer.get_backend('qasm_simulator')
    
    circuit = QuantumCircuit(3, 3)

    grovers_search(circuit)

    job = execute(circuit, simulator, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)

    print("\nTotal count for states are:", counts)

    plot_histogram(counts)
