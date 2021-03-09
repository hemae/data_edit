from fitting import polinomial_fit
from math_func import maximum_of_point_func, minimum_of_point_func, integral


def cut_curve(f_ini, typ='max'):    #returns [list, list]
    if typ == 'max':
        max_point = maximum_of_point_func(f_ini, 1, len(f_ini))
        left_part = []
        right_part = []
        i = 0
        x = f_ini[i][0]
        while x <= max_point[0] and i < len(f_ini):
            left_part.append([f_ini[i][0], f_ini[i][1]])
            i += 1
            x = f_ini[i][0]
        i -= 1
        while i < len(f_ini):
            right_part.append([f_ini[i][0], f_ini[i][1]])
            i += 1
    elif typ == 'min':
        min_point = minimum_of_point_func(f_ini, 1, len(f_ini))
        left_part = []
        right_part = []
        i = 0
        x = f_ini[i][0]
        while x <= min_point[0] and i < len(f_ini):
            left_part.append([f_ini[i][0], f_ini[i][1]])
            i += 1
            x = f_ini[i][0]
        while i < len(f_ini):
            right_part.append([f_ini[i][0], f_ini[i][1]])
            i += 1
    else:
        pass


    return [left_part, right_part]


def integral_by_half_peak(f, typ='max'):    #  returns float number or None
    if typ == 'max':
        cut_f = cut_curve(f, typ='max')
        left_f = cut_f[0]
        right_f = cut_f[1]

        if len(left_f) == 0 or len(right_f) == 0:
            return None

        half_peak = left_f[-1][1] / 2

        parameters_left_f = polinomial_fit(left_f, n=2)
        parameters_right_f = polinomial_fit(right_f, n=2)

        step = left_f[1][0] - left_f[0][0]
        x = left_f[0][0]
        if left_f[1][1] - left_f[0][1] > 0:
            while left_f[0][1] < half_peak:
                x -= step
                y = 0
                for i in range(len(parameters_left_f)):
                    y += parameters_left_f[i] * pow(x, i)
                left_f = [[x, y]] + left_f
        else:
            pass

        step = right_f[-1][0] - right_f[-2][0]
        x = right_f[-1][0]
        if right_f[-1][1] - left_f[-2][1] < 0:
            while right_f[-1][1] > half_peak:
                x += step
                y = 0
                for i in range(len(parameters_right_f)):
                    y += parameters_right_f[i] * pow(x, i)
                right_f = right_f + [[x, y]]
        else:
            pass

        left_integral = integral(left_f, 0, 1)
        right_integral = integral(right_f, 0, 1)
        return left_integral + right_integral
    else:
        cut_f = cut_curve(f, typ='min')
        left_f = cut_f[0]
        right_f = cut_f[1]

        if len(left_f) == 0 or len(right_f) == 0:
            return None

        half_peak = left_f[-1][1] / 2

        parameters_left_f = polinomial_fit(left_f, n=2)
        parameters_right_f = polinomial_fit(right_f, n=2)

        step = left_f[1][0] - left_f[0][0]
        x = left_f[0][0]
        if left_f[1][1] - left_f[0][1] < 0:
            while left_f[0][1] > half_peak:
                x -= step
                y = 0
                for i in range(len(parameters_left_f)):
                    y += parameters_left_f[i] * pow(x, i)
                left_f = [[x, y]] + left_f
        else:
            pass

        step = right_f[-1][0] - right_f[-2][0]
        x = right_f[-1][0]
        if right_f[-1][1] - left_f[-2][1] > 0:
            while right_f[-1][1] < half_peak:
                x += step
                y = 0
                for i in range(len(parameters_right_f)):
                    y += parameters_right_f[i] * pow(x, i)
                right_f = right_f + [[x, y]]
        else:
            pass

        try:
            left_integral = integral(left_f, 0, 1)
            right_integral = integral(right_f, 0, 1)
            integral_ = left_integral + right_integral
            return - integral_
        except:
            return None


# import numpy as np
# from spec_func import np_arr
#
# a = 200 / 162
# b = - 2000 / 81
# c = 19 * 200 / 162
#
# x_1 = np.linspace(6, 13, 1000)
# y_1 = a * pow(x_1, 2) + b * x_1 + c
#
# f = []
# for i in range(len(x_1)):
#     f.append([x_1[i], y_1[i]])
# f = np_arr(f)
#
# print(integral_by_half_peak(f, typ='min'))