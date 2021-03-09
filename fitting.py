import numpy as np
from math_func import determinant


def copy_arr(arr):
    f = []
    for point in arr:
        f.append(point)

    return f


def np_arr(arr):
    ar_1 = np.array([arr[0]])
    for i in range(len(arr) - 1):
        ar_1 = np.vstack([ar_1, arr[i + 1]])

    return ar_1


def polinomial_fit(f_ini, n=2): # f_ini = [[x1, f(x1)], [[x2, f(x2)], ...]; n is order of polinomial
    f = copy_arr(f_ini)
    f = np_arr(f)

    num = len(f)

    coefs = []
    for i in range(2 * n + 1):
        coefs.append(sum(pow(f[:, 0], i)) / num)
    coefs.reverse()

    matrix_0 = []
    matrix_b = []
    for i in range(n + 1):
        matrix_b.append(np.dot(pow(f[:, 0], i).T, f[:, 1]) / num)
        string = []
        for j in range(n + 1):
            string.append(coefs[j])
        del coefs[0]
        matrix_0.append(string)
    matrix_b.reverse()

    matrices = []
    matrices.append(matrix_0)

    for i in range(n + 1):
        matr = []
        for j in range(len(matrix_0)):
            string = []
            for k in range(len(matrix_0[j])):
                string.append(matrix_0[j][k])
            matr.append(string)
        for j in range(len(matr)):
            matr[j][i] = matrix_b[j]
        matrices.append(matr)

    # print(matrices)

    parameters = []
    for i in range(n + 1):
        parameters.append(determinant(matrices[i + 1]) / determinant(matrices[0]))
    parameters.reverse()

    return parameters


def assemble_func(parameters, x_arr): # returns array of f(x)
    y = []
    for x in x_arr:
        summ = 0
        for i in range(len(parameters)):
            summ += parameters[i] * pow(x, i)
        y.append(summ)

    return y


def log_fit(f_ini):
    f = copy_arr(f_ini)
    f = np_arr(f)

    num = len(f)

    alpha_1 = (sum(np.log(f[:, 0]))) / num
    alpha_2 = (np.dot(np.log(f[:, 0]).T, np.log(f[:, 0]))) / num
    betha_1_1 = (np.dot(f[:, 1].T, np.log(f[:, 0]))) / num
    gamma_1 = (sum(f[:, 1])) / num

    return [(determinant([[betha_1_1, alpha_1], [gamma_1, 1]])) / (determinant([[alpha_2, alpha_1], [alpha_1, 1]])), (determinant([[alpha_2, betha_1_1], [alpha_1, gamma_1]])) / (determinant([[alpha_2, alpha_1], [alpha_1, 1]]))]


def exp_fit(f_ini):
    f = copy_arr(f_ini)
    f = np_arr(f)

    num = len(f)

    alpha_1 = (sum(f[:, 0])) / num
    alpha_2 = (np.dot(f[:, 0].T, f[:, 0])) / num
    betha_1_1 = (np.dot(f[:, 0].T, np.log(f[:, 1]))) / num
    gamma_1 = (sum(np.log(f[:, 1]))) / num


    return [np.exp((determinant([[gamma_1, alpha_1], [betha_1_1, alpha_2]])) / (determinant([[1, alpha_1], [alpha_1, alpha_2]]))),
            (determinant([[1, gamma_1], [alpha_1, betha_1_1]])) / (
                determinant([[1, alpha_1], [alpha_1, alpha_2]]))]


def pow_fit(f_ini):
    f = copy_arr(f_ini)
    f = np_arr(f)

    num = len(f)

    alpha_1 = (sum(np.log(f[:, 0]))) / num
    alpha_2 = (np.dot(np.log(f[:, 0]).T, np.log(f[:, 0]))) / num
    betha_1_1 = (np.dot(np.log(f[:, 0]).T, np.log(f[:, 1]))) / num
    gamma_1 = (sum(np.log(f[:, 1]))) / num


    return [np.exp((determinant([[gamma_1, alpha_1], [betha_1_1, alpha_2]])) / (determinant([[1, alpha_1], [alpha_1, alpha_2]]))),
            (determinant([[1, gamma_1], [alpha_1, betha_1_1]])) / (
                determinant([[1, alpha_1], [alpha_1, alpha_2]]))]
