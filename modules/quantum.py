from qiskit import IBMQ, QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram

from numpy import pi


def grovers_search(circuit):
    """
    IBM Q implementation of Grover's search algorithm with multiple solutions.
    Needed to construct simplicial complex for data analysis.
    :param circuit: IBM Q circuit object 
    """
    circuit.u3(pi * 0.5,pi * 0.5,pi * 0.5, 0)
    circuit.u3(pi/2,pi/2,pi/2, 1)
    circuit.u3(pi/2,pi/2,pi/2, 2)

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

    circuit.measure([0, 1], [0, 1])


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
