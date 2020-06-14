# Quantum-topological analysis of stock market data

Here is a short description of the final project for Architecture of Computer Systems course by Solomiia Leno on quantum-topological analysis of stock market data.

## table of contents
1. [aim of project](#aim-of-project)
2. [topological data analysis](#topological-data-analysis)
3. [why quantum?](#why-quantum)
4. [algorithm](#algorithm)
5. [quantum algorithm](#quantum-algorithm)
6. [implementation details](#implementation-details)
    1. [limitations](#limitations)
    2. [circuits](#circuits)
7. [data and testing](#data-and-testing)
8. [usage](#usage)
9. [references](#references)

## aim of project
The aim of the project is to implement **quantum algorithm for detecting possible time allocaions of stock market crashes using topological data analysis** on IBM Quantum Experience API for **quantum computers**.

## topological data analysis
**Topological data analysis** (shortly - TDA) is an approach to the analysis of topologically stuctured data.This approach manages well the highly dimnesioned or noisy data.

TDA provides a general framework to analyze such data in a manner that is insensitive to the particular metric chosen and provides dimensionality reduction and robustness to noise. Beyond this, it inherits functoriality, a fundamental concept of modern mathematics, from its topological nature, which allows it to adapt to new mathematical tools.

## why quantum?
Due to quantum superposition principle, one quantum bit may take **infinitely many** different states (each being a different superposition of two classical sates - **0** and **1**).

Thus **n** quantum bits allow us to store all **2^n** possible topologiacl stucture that may be created with **n** pieces of data.

Same principle allows one to perform **parallel** computations, in our case - computation of topological model (simplicial complex) and persistent Betti numbers calculation.

All in all, total time complexity of quantum inplementation of persistent homology is **O(n^3)** while implementation on classical computer has complexity of **O(2^2n)**.

## algorithm
The algorithm is based on the **perisitent homology** approach to data analysis. As topological indicator **Betti numbers** are chosen (usually this method produces very noisy data but it is the most convenient algorithm for quantisation).

Detailed explanation of TDA based analysis of stock market crashes along with Python code is in the [**experimets/algorithm.ipynb**](https://github.com/sol4ik/quantum-computing/blob/master/experiments/algorithm.ipynb) Jupyter notebook.

## quantum algorithm
Main reference for the quantum algorithm development was **Quantum algorithms for topological and geometric analysis of big data** by S.Lloyd (link in the [references section](#references)).

First step in the algorithm pipeline is to **process the input data** using classical computer. The steps are the following:

1. download the data on stock prices from Yahoo! Finance and save in the **.csv** format
2. load the data and store the values of `Close` price only
  * it is a common practice to use Close values when working with stock market data
3. create data cloud with **Takens' embedding** algorithm
  * the **embedding dimension** must be **a power of 2**
  * in the implementation presented, `embedding_dim = 2`
4. **normalize** the data cloud
  * consider each point as a vector from ![R^n](https://latex.codecogs.com/gif.latex?%5Cmathbb%7BR%7D%5En) and normalize it to be of unit length
5. express each data point as inpput alngles for **U3 gates**
  * **U3** is a quantum gate that allows one to set qubit to any possible state. U3 is denoted by the following rotation matrix
  
    ![U3 matrix](https://latex.codecogs.com/gif.latex?U3%28%5Ctheta%2C%20%5Cphi%2C%20%5Calpha%29%20%3D%20%5Cbegin%7Bpmatrix%7D%20cos%28%5Cfrac%7B%5Ctheta%7D%7B2%7D%29%20%26%20-e%5E%7Bi%5Calpha%7D%20sin%28%5Cfrac%7B%5Ctheta%7D%7B2%7D%29%5C%5C%20e%5E%7Bi%20%5Cphi%7D%20sin%28%5Cfrac%7B%5Ctheta%7D%7B2%7D%29%20%26%20e%5E%7Bi%28%5Calpha%20&plus;%20%5Cphi%29%7D%20cos%28%5Cfrac%7B%5Ctheta%7D%7B2%7D%29%20%5Cend%7Bpmatrix%7D)
  * since this gate is applied to **|0>** state, the resulting state looks as following
  
    ![quantum state](https://latex.codecogs.com/gif.latex?%7C%5Cpsi_0%3E%20%3D%20cos%28%5Ctheta/_2%29%20&plus;%20e%5E%7Bi%5Cphi%7D%20sin%28%5Ctheta/_2%29)
  * thus, since we start with |0> state ![alpha = 0](https://latex.codecogs.com/gif.latex?%5Calpha%20%3D%200) and ![phi = 0](https://latex.codecogs.com/gif.latex?%5Cphi%20%3D%200) because both coordinates of data point are real numbers
6. create the IBM Q circuit with needed amount of quantum bits
  * it is possible to have as many as **32** quantum bits in the circuit, but if you want to get convenient results with quantum computer you are limited with only **5** quantum bits due to coherence
  * this way you are limited to only **3 2-dimensional** data points
7. set quantum bits to needed states with **U3** gates
8. calculate pairwise distances between the data points
  * set as **a** and **b** quantum states denoting hte points we want to calculate the distance between and **0** as the state of contol bit, the one the distance will be calculated to
  
    ![distance calulation](https://latex.codecogs.com/gif.latex?%5C%5C%20%7C%5Cpsi_0%3E%20%3D%20%7Ca%2C%20b%2C%200%3E%20%5C%5C%20%5Ctext%7Bapply%20%5Ctextbf%7BHadamar%7D%20gate%20to%20control%20bit%7D%20%5C%5C%20%7C%5Cpsi_1%3E%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%28%7Ca%2C%20b%2C%200%3E%20&plus;%20%7Ca%2C%20b%2C%201%3E%29%20%5C%5C%20%5Ctext%7Bapply%20%5Ctextbf%7Bcontrolled%20swap%7D%20operator%20to%20%5Ctextbf%7Ba%7D%20and%20%5Ctextbf%7Bb%7D%7D%20%5C%5C%20%5Ctext%7Bcontrolled%20swap%20operator%20takes%20in%203-bit%20quantum%20state%20and%20%5Ctextbf%7Bswaps%20first%20two%7D%20if%20the%20last%20one%20is%20%5Ctextbf%7B1%7D%7D%20%5C%5C%20%7C%5Cpsi_2%3E%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%28%7Ca%2C%20b%2C%200%3E%20&plus;%20%7Cb%2C%20a%2C%201%3E%29%20%5C%5C%20%5Ctext%7Bapply%20%5Ctextbf%7BHadamar%7D%20gate%20to%20control%20bit%7D%20%5C%5C%20%7C%5Cpsi_2%3E%20%3D%20%5Cfrac%7B1%7D%7B2%7D%7C0%3E%28%7Ca%2C%20b%3E%20&plus;%20%7Cb%2C%20a%3E%29%20&plus;%20%5Cfrac%7B1%7D%7B2%7D%7C1%3E%28%7Ca%2C%20b%3E%20&plus;%20%7Cb%2C%20a%3E%29)
* now, the control bit is in the quantum state denoting distance between **a** and **b**
9. contruct **simplicial complex** from the pairwise distances between points
  * **Grover's search algorithm** is used for this task
  * you can find detailed description of Grover's search [here](https://quantum-computing.ibm.com/docs/guide/q-algos/grover-s-algorithm)
  * main idea is to implement Grover's algorithm with **oracle** that allows multiple solutions, since multiple simplicial complexes can be cinstructed from a single data cloud
10. perform **quantum persistent homology** algorithm  

## implementation details
The quantum algorithm is implemented with [IBM Quantum Experience](https://quantum-computing.ibm.com/) as well as plain Python code.

All the source code can be found in the **modules** directory.

* **preprocessing.py**
  * contains funntions for data preprocessing: load data, transform to data cloud using **Takens' embedding** and data normalization
* **quantum.py**
  * contains functions that are directly related to quantum algorithm implementation: circuit configuration, Grove's search alogorithm implementation etc.
* **postprocessing.py**
* **main.py**
  * brings all the functional together and manages the access to IBMQ backend

### limitations
When it comes to implementing the quantum persistent homology algorithm several limitations arise.

* due coherence and high error rate it is possible to get concenient results only by working with **5-qubit** computers or **simulation**
  * thus, it is possible to process **only three 2-dimnesional points** within the quantum implementation of the algorithm 
* IBM Q API **does not allow one to create custom gate for 3 qubits** which is needed for distances calculations
* again, due to lack of computational accuracy and **qRAM** it is impossible to conveniently implement the calculation of quantum density matrix needed for further calculations of Betti numbers

### circuits
Since not all of the algorithm can be implemented within IBM Quantum Experience API, I worked on several smaller circuits.

You can find the ciruits schemas in the **citcuits** directory.

## data and testing
As testing data I chose 4 significant histirical cases of stock market crashes: Wall Street crash, Black Monday crash, Crisis of 2008 and 2020 Coronavirus crash.

All the data is stored in **.csv** files and contains info on values of **Dow-Jones** and **S&P 500 indexes** on the time periods of the crashes.

You can find the data files as well as more detailed description and visualizations in this repo - **data** directory.


## usage
In order to try the software developed you need to clone this repository and run the following commands in the terminal

    cd quantum-comuting/modules
  
    virtualenv venv
    sourse venv/bin/activate
  
    pip install -r requirements.txt
  
    touch ibmq_token.txt
  
Go to [IBM Quantum Experience](https://quantum-computing.ibm.com/) and create **personal account** or simply log in if you have one. 

In **My Account** section find **Quiskit in local environment** and copy your account token. Insert the token in newly created **ibmq_token.txt** file or right in the **main.py** code.

Run the program with 

    python main.py
  
In order to configure the backend you want to run the circuit on, go to **main.py** and find the following code

    simulator = Aer.get_backend('specify backed you want to use here')
  
**BUT** for development I recommend using IBMQ directly as it allows one to run circuit gates step by step, view partial results and monitor the queue for backend.

## references
Here is the [**link**](https://docs.google.com/presentation/d/16S5xK0NhVxzvIlZIi0GVV4fMD2bYA7v2nEAYY3zeXXA/edit?usp=sharing) to my project presentation.

All the test data are downloaded from **Yahoo! Finance**.

Some of the sources I worked with:
- Vakarchuk I. Quantum mechanics. Lviv State University of Ivan Franko; 1998. 614 p.
- Lloyd, Seth & Garnerone, Silvano & Zanardi, Paolo. (2014). Quantum algorithms for topological and geometric analysis of big data. Nature Communications. 10.1038/ncomms10138. 
  - [**link**](https://www.researchgate.net/publication/264742794_Quantum_algorithms_for_topological_and_geometric_analysis_of_big_data/citation/download)
- Dawid Kopczyk. (2018). Quantum machine learning for data scientists
  - [**link**](https://arxiv.org/pdf/1804.10068.pdf)
- Detecting stock market crashes with topological data analysis
  - [**link**](https://towardsdatascience.com/detecting-stock-market-crashes-with-topological-data-analysis-7d5dd98abe42)
- Persistent homology with examples
  - [**link**](https://towardsdatascience.com/persistent-homology-with-examples-1974d4b9c3d0)
