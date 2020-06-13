from pandas import read_csv
from numpy import arccos, arcsin, pi, round


def norm(vect):
    """
    Calculate Eucledian norm of vector in R^n.
    :param vect: n-element tuple - vector in R^n
    :return: float value - Eucledian norm of vect
    """
    norm = 0
    for i in range(len(vect)):
        norm += vect[i] ** 2
    return norm ** 0.5


def to_angles(vect):
    """
    Represent point from surface of Bloch sphere within two angles.
    (x, y, z) = (sin a cos b, sin a sin b, cos b)
    Represent each angle within pi.
    :param vect: inout point
    :return: 2-element tuple - values of angles (a, b)
    """
    b = arccos(vect[2])
    a = arcsin(vect[0] / b)
    pi_a = "pi*" + str(round(a / pi, 3))
    pi_b = "pi*" + str(round(b / pi, 3))
    return pi_a, pi_b


def preprocess(path):
    """
    Preprocess data for quantum implementation of persistent homology algorithm
    and write circuit starting configuration to .csv file.
    :param path: path to data file
    """
    # load data
    data = read_csv(path)["Close"]

    # data thinning
    resampled_data = list()
    sum = 0
    for i in range(len(data)):
        if i % 5 != 0:
            sum += data[i]
        else:
            resampled_data.append(sum / 5)
            sum = 0

    # data cloud - takens' embedding
    data_cloud = list()
    embedding_dim = 3
    embedding_time_delay = 2
    for i in range(len(resampled_data) - embedding_dim * embedding_time_delay):
        to_append = [resampled_data[i + embedding_time_delay * j] for j in range(embedding_dim)]
        data_cloud.append(tuple(to_append))

    # normalize data - points on Bloch sphere
    for i in range(len(data_cloud)):
        p_norm = norm(data_cloud[i])
        data_cloud[i] = tuple([data_cloud[i][j] / p_norm for j in range(embedding_dim)])

    # to angles - for U3 gate
    angles = list()
    for vect in data_cloud:
        angles.append(to_angles(vect))

    # write circuit configurations to .csv file
    with open("results/circuit_conf.csv", 'w') as config_file:
        print("a,b", file=config_file)
        for vect in angles:
            print("{},{}".format(vect[0], vect[1]), file=config_file)


if __name__ == "__main__":
    preprocess("../data/gspc/^GSPC-feb-2020-corona-daily.csv")
