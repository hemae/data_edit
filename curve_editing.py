from fitting import log_fit, pow_fit, polinomial_fit
import numpy as np
from constants import *
import matplotlib.pyplot as plt
# from spec_func import np_arr
# from help_functions import copy_arr

# N = 100
# sigma = 0.1
# a = 2
# b = 0
#
# x = np.linspace(5, 20, N)
# y_0 = a * np.log(x) + b
# y = y_0 + np.random.normal(0, sigma, N)
# y[41] = y[41] + 2
# y_copy = copy_arr(y)


def np_arr(arr):
    ar_1 = np.array([arr[0]])
    for i in range(len(arr) - 1):
        ar_1 = np.vstack([ar_1, arr[i + 1]])

    return ar_1


def curve_editing_log(f_ini, x_cr, y_cr, g=1.0):
    N = len(f_ini)

    # for test
    x = []
    y = []
    for i in range(len(f_ini)):
        x.append(f_ini[i][x_cr])
        y.append(f_ini[i][y_cr])
    # for test

    f = []
    for i in range(len(f_ini)):
        f.append([f_ini[i][x_cr], f_ini[i][y_cr]])
    f = np_arr(f)

    parameters = log_fit(f)
    a_fit = parameters[0]
    b_fit = parameters[1]
    y_fit = []
    for i in range(N):
        y_fit.append(a_fit * np.log(f[:, 0][i]) + b_fit)

    abs_array_of_errors = []
    for i in range(N):
        abs_array_of_errors.append(abs(f[:, 1][i] - y_fit[i]))
    stat_medium_err = sum(abs_array_of_errors) / N

    for i in range(len(abs_array_of_errors)):
        if abs_array_of_errors[i] > (1 + g) * stat_medium_err:
            f[:, 1][i] = a_fit * np.log(f[:, 0][i]) + b_fit

    for i in range(len(f_ini)):
        f_ini[i][FIELD], f_ini[i][MOMENT] = f[:, 0][i], f[:, 1][i]

    # for test
    plt.subplot(1, 1, 1)
    plt.scatter(x, y, s=3, c='red')
    # plt.scatter(x, y_copy, s=2, c='green')
    plt.plot(x, y_fit)
    # plt.scatter(x, abs_array_of_errors, s=2, c='blue')
    plt.show()
    # for test

    return None


def curve_editing_pow(f_ini, x_cr, y_cr, g=1.0):
    N = len(f_ini)

    # for test
    x = []
    y = []
    for i in range(len(f_ini)):
        x.append(f_ini[i][x_cr])
        y.append(f_ini[i][y_cr])
    # for test

    f = []
    for i in range(len(f_ini)):
        f.append([f_ini[i][x_cr], f_ini[i][y_cr]])
    f = np_arr(f)

    parameters = pow_fit(f)
    a_fit = parameters[0]
    b_fit = parameters[1]
    y_fit = []
    for i in range(N):
        y_fit.append(a_fit * pow(f[:, 0][i], b_fit))

    abs_array_of_errors = []
    for i in range(N):
        abs_array_of_errors.append(abs(f[:, 1][i] - y_fit[i]))
    stat_medium_err = sum(abs_array_of_errors) / N

    for i in range(len(abs_array_of_errors)):
        if abs_array_of_errors[i] > (1 + g) * stat_medium_err:
            f[:, 1][i] = a_fit * pow(f[:, 0][i], b_fit)

    for i in range(len(f_ini)):
        f_ini[i][FIELD], f_ini[i][MOMENT] = f[:, 0][i], f[:, 1][i]

    # for test
    plt.subplot(1, 1, 1)
    plt.scatter(x, y, s=3, c='red')
    # plt.scatter(x, y_copy, s=2, c='green')
    plt.plot(x, y_fit)
    # plt.scatter(x, abs_array_of_errors, s=2, c='blue')
    plt.show()
    # for test

    return None


def curve_editing_pol(f_ini, x_cr, y_cr, order=2, g=1.0):
    N = len(f_ini)

    # for test
    x = []
    y = []
    for i in range(len(f_ini)):
        x.append(f_ini[i][x_cr])
        y.append(f_ini[i][y_cr])
    # for test

    f = []
    for i in range(len(f_ini)):
        f.append([f_ini[i][x_cr], f_ini[i][y_cr]])
    f = np_arr(f)

    parameters = polinomial_fit(f, n=order)
    y_fit = []
    for i in range(N):
        summ = 0
        for j in range(len(parameters)):
            summ += parameters[j] * pow(f[:, 0][i], j)
        y_fit.append(summ)

    abs_array_of_errors = []
    for i in range(N):
        abs_array_of_errors.append(abs(f[:, 1][i] - y_fit[i]))
    stat_medium_err = sum(abs_array_of_errors) / N

    for i in range(len(abs_array_of_errors)):
        if abs_array_of_errors[i] > (1 + g) * stat_medium_err:
            for j in range(len(parameters)):
                summ += parameters[j] * pow(f[:, 0][i], j)
            f[:, 1][i] = summ

    for i in range(len(f_ini)):
        f_ini[i][FIELD], f_ini[i][MOMENT] = f[:, 0][i], f[:, 1][i]

    # for test
    plt.subplot(1, 1, 1)
    plt.scatter(x, y, s=3, c='red')
    # plt.scatter(x, y_copy, s=2, c='green')
    plt.plot(x, y_fit)
    # plt.scatter(x, abs_array_of_errors, s=2, c='blue')
    plt.show()
    # for test

    return None

# plt.subplot(1, 1, 1)
# plt.scatter(x, y, s=3, c='red')
# plt.scatter(x, y_copy, s=2, c='green')
# plt.plot(x, y_fit)
# plt.scatter(x, abs_array_of_errors, s=2, c='blue')
# plt.show()