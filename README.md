# Quantum-topological analysis of stock market data

Here is a short description of the final project for Architecture of Computer Systems course by Solomiia Leno on quantum-topological analysis of stock market data.

## table of contents
1. [aim of project](#aim-of-project)
2. [topological data analysis](#topological-data-analysis)
3. [why quantum?](#why-quantum)
4. [algorithm](#algorithm)
5. [implementation details](#implementation-details)
6. [data and testing](#data-and-testing)
7. [references](#references)

## aim of project
The aim of the project is to implement **quantum algorithm for detecting possible time allocaions of stock market crashes using topological data analysis** on IBM Quantum Experience API of **quantum computers**.

## topological data analysis
**Topological data analysis** (shortly - TDA) is an approach to the analysis of topologically stuctured data.This approach manages well the highly dimnesioned or noisy data.

TDA provides a general framework to analyze such data in a manner that is insensitive to the particular metric chosen and provides dimensionality reduction and robustness to noise. Beyond this, it inherits functoriality, a fundamental concept of modern mathematics, from its topological nature, which allows it to adapt to new mathematical tools.

## why quantum?
Due to quantum superposition principle one quantum bit may take **infinitely many** different states (each being a different superposition of two classical sates - **0** and **1**).

Thus **n** quantum bits allow us to store all **2^n** possible topologiacl stucture that may be created with **n** pieces of data.

Same principle allows one to perform **parallel** computations, in our case - computation of topological model (pairwise distances between data pieces).

One more import factor is **memory**. 

## algorithm
Detailed explanation of TDA based analysis of stock market crashes along with Python code is in the **experimets/algorithm.ipynb** Jupyter notebook.

## implementation details
The quantum algorithm is implemented with [IBM Quantum Experience](https://quantum-computing.ibm.com/) as well as plain Python code.

## data and testing
As testing data I chose 4 significant histirical cases of stock market crashes: Wall Street crash, Black Monday crash, Crisis of 2008 and 2020 Coronavirus crash.

All the data is stored in **.csv** files and contains info on values of **Dow-Jones** and **S&P 500 indexes** on the time periods of the crashes.

You can find the data files as well as more detailed description and visualizations in this repo - **data** directory.

## references
You can find more detailed report on the project [**here**](https://sol4ik.github.io/AoCS-report/).

Here is the [**link**](https://docs.google.com/presentation/d/16S5xK0NhVxzvIlZIi0GVV4fMD2bYA7v2nEAYY3zeXXA/edit?usp=sharing) to my project presentation.

All the test data are downloaded from **Yahoo! Finance**.

Some of the sources I worked with:
- Vakarchuk I. Quantum mechanics. Lviv State University of Ivan Franko; 1998. 614 p.
- Lloyd, Seth & Garnerone, Silvano & Zanardi, Paolo. (2014). Quantum algorithms for topological and geometric analysis of big data. Nature Communications. 10.1038/ncomms10138. 
  - [**link**](https://www.researchgate.net/publication/264742794_Quantum_algorithms_for_topological_and_geometric_analysis_of_big_data/citation/download)
- Detecting stock marketcrashes with topological data analysis
  - [**link**](https://towardsdatascience.com/detecting-stock-market-crashes-with-topological-data-analysis-7d5dd98abe42)
- Persistent homology with examples
  - [**link**](https://towardsdatascience.com/persistent-homology-with-examples-1974d4b9c3d0)
