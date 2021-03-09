import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d


# is a string numeric(float)? "True" - yes, "False" - No
def is_digit(string):
    if string.isdigit():  # including negative number situation
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


# integral calculating of point function (without approx...)
def integral(arr, x, y):  # in_on - integration variable index; in_le - integrable variable index
    area = 0.0
    for i in range(len(arr) - 1):
        area = area + (arr[i + 1][x] - arr[i][x]) * (arr[i + 1][y] + arr[i][y]) / 2

    return area


# integral calculating for "func"-function from a to b with "n" accuracy
def func_integral(func, a, b, n):
    area = 0.0
    for i in range(pow(10, n)):
        area = area + (func(((b - a) / pow(10, n)) * (i + 1)) + func(((b - a) / pow(10, n)) * i)) * (
                (b - a) / pow(10, n)) / 2

    return area


# differentiating
def diff(func, a, b, err_1, err_2):
    x = np.linspace(a, b, err_1 * pow(10, err_2))
    y = func(x)
    y_diff = []
    for i in range(len(x) - 1):
        y_diff.append((y[i + 1] - y[i]) / (x[i + 1] - x[i]))
    f = np.poly1d(np.polyfit(x[len(x) - 3:len(x) - 1], y_diff[len(y_diff) - 2:len(y_diff)], 1))
    y_diff.append(f(x[len(x) - 1]))
    kind_interp = 'linear'
    func_diff = interp1d(x, y_diff, kind=kind_interp)

    return func_diff


# integrating
def integ(func, a, b, err_1, err_2):
    x = np.linspace(a, b, err_1 * pow(10, err_2))
    y = func(x)
    y_integ = []
    for i in range(len(x) - 1):
        y_integ.append(integrate.simps(y[:i + 1], x[:i + 1]))
    f = np.poly1d(np.polyfit(x[len(x) - 3:len(x) - 1], y_integ[len(y_integ) - 2:len(y_integ)], 1))
    y_integ.append(f(x[len(x) - 1]))
    func_integ = interp1d(x, y_integ)

    return func_integ


# maximum of point function (point will be returned: [x, y, ...])
def maximum_of_point_func(arr, cr, amount_of_points):
    maxx = arr[0][cr]
    k = 0
    for i in range(amount_of_points):
        if arr[i][cr] > maxx:
            maxx = arr[i][cr]
            k = i

    return arr[k]


# minimum of point function (point will be returned: [x, y, ...])
def minimum_of_point_func(arr, cr, amount_of_points):
    minn = arr[0][cr]
    k = 0
    for i in range(amount_of_points):
        if arr[i][cr] < minn:
            minn = arr[i][cr]
            k = i

    return arr[k]


def max_val_func(func, a, b):
    n = 1000
    k = (b - a) / n
    maxx = func(a)
    for i in range(n):
        if maxx < func(a + i * k):
            maxx = func(a + i * k)

    return maxx


def y_cross(curve, x, y):
    points = []
    for i in range(len(curve) - 1):
        if (curve[i + 1][y] * curve[i][y]) < 0:
            points.append((curve[i + 1][x] + curve[i][x]) / 2)
    return points


def inverse_function(func, a, b, err_1, err_2):
    x = np.linspace(a, b, err_1 * pow(10, err_2))
    y = func(x)
    func_inverse = interp1d(y, x)

    return func_inverse


def inverse_function_point(curve, x, y):
    return interp1d(curve[:, y], curve[:, x])


def determinant(a): # determinator of a(nxn); returns float number of None
    def det(a):
        def minor(a, i, j):

            b = []

            for k in range(len(a)):
                if k != i:
                    string = []
                    for l in range(len(a[k])):
                        if l != j:
                            string.append(a[k][l])
                    b.append(string)

            return b

        if len(a) == 1:
            return a[0][0]

        summ = 0
        for i in range(len(a[0])):
            summ += pow(-1, i) * a[0][i] * det(minor(a, 0, i))

        return summ

    if len(a) == 0:
        return None

    if len(a[0]) == 0:
        return None

    lenght = len(a[0])
    for string in a:
        if lenght != len(string):
            return None

    if len(a) != len(a[0]):
        return None


    return det(a)




    det = 0
    return det