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
    Represent point from surface of Bloch sphere within three angles.
    ! In this case input vector is 2-dimensional, but in general case - any power of 2

    |s> = a |0> + b |1>
    |s> = cos (a` / 2) |0> + e^(i * phi) sin (a` / 2) |1>
    Since a and b are real numbers, phi = 0.
    Thus a` = 2 * arccos(a) and b = 2 * arcsin(a)

    Represent each angle within pi.
    :param vect: input point
    :return: 2-element tuple - values of angles (a, b)
    """
    a = 2 * arccos(vect[0])
    b = 2 * arcsin(vect[1])
    pi_a = "pi*" + str(round(a / pi, 3))
    pi_b = "pi*" + str(round(b / pi, 3))
    return pi_a, pi_b, "pi*0"


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
    embedding_dim = 2  # ! power of 2
    embedding_time_delay = 2
    for i in range(len(resampled_data) - embedding_dim * embedding_time_delay):
        to_append = [resampled_data[i + embedding_time_delay * j] for j in range(embedding_dim)]
        data_cloud.append(tuple(to_append))

    # construct quantum state for each point
    q_coefs = list()
    for i in range(len(data_cloud)):
        cur_norm = norm(data_cloud[i])
        q_coefs.append(tuple([data_cloud[i][j] / cur_norm for j in range(embedding_dim)]))

    # to angles - for U3 gate
    angles = list()
    for vect in q_coefs:
        angles.append(to_angles(vect))

    # write circuit configurations to .csv file
    with open("results/circuit_conf.csv", 'w') as config_file:
        print("a,b,phi", file=config_file)
        for vect in angles:
            print("{},{},{}".format(vect[0], vect[1], vect[2]), file=config_file)


if __name__ == "__main__":
    preprocess("../data/gspc/^GSPC-feb-2020-corona-daily.csv")
