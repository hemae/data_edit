import numpy as np
from scipy.interpolate import interp1d
import math_func as mf
from curve_editing import curve_editing_log, curve_editing_pow, curve_editing_pol
from constants import *


# from list to numpy.array transformation
def np_arr(arr):
    ar_1 = np.array([arr[0]])
    for i in range(len(arr) - 1):
        ar_1 = np.vstack([ar_1, arr[i + 1]])

    return ar_1


# def editing_curves(ar_1):
#     pass


# at the exit of "create_curves_1()" it has got array of curves array
def create_curves(arr, ac, cr_in, editing):
    ar_1 = [
        []]  # array of curves [[[x4, y4, num1, ..], [x1, y1, num1, ..], ...], [[x4, y4, num1, ..], [x1, y1, num1, ..], ...], ....]
    criterion = [round(arr[0][cr_in])]  # for example "num" - number of curve
    for i in range(len(arr)):
        indicate = 0
        for j in range(len(criterion)):
            if (arr[i][cr_in] < (criterion[j] + ac)) and (
                    arr[i][cr_in] > (criterion[j] - ac)):  # difference by step of criterion more than 2 * "ac"
                arr[i][cr_in] = round(arr[i][cr_in])
                ar_1[j].append(arr[i])
                indicate += 1
                break
        if indicate == 0:
            criterion.append(round(arr[i][cr_in]))
            arr[i][cr_in] = round(arr[i][cr_in])
            ar_1.append([arr[i]])

    if editing == True:
        for i in range(len(ar_1)):
            count = 0
            while count < len(ar_1[i]):
                if ar_1[i][count][MOMENT] <= 0 or ar_1[i][count][FIELD] <= 0:
                    del ar_1[i][count]
                else:
                    count += 1
            curve_editing_pow(ar_1[i], FIELD, MOMENT)

    return ar_1


# ascending by m - element (H - column)
def sort_ascending(arr, m):
    for j in range(len(arr)):
        for k in range(len(arr[j])):
            for i in range(len(arr[j]) - k - 1):
                if arr[j][i + 1][m] < arr[j][i][m]:
                    b = arr[j][i]
                    arr[j][i] = arr[j][i + 1]
                    arr[j][i + 1] = b

    return arr


# statistical processing by parameter m
def stat(arr, m):
    medium = []
    for i in range(len(arr)):
        medium.append(0)
        for j in range(len(arr[i])):
            medium[i] = medium[i] + arr[i][j][m]
        medium[i] = round(medium[i] / len(arr[i]))
        for j in range(len(arr[i])):
            arr[i][j][m] = medium[i]

    return medium


# sort ascending by parameter m between curves
def sort_ascending_curves(arr, m):
    for k in range(len(arr)):
        for i in range(len(arr) - k - 1):
            if arr[i + 1][0][m] < arr[i][0][m]:
                b = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = b

    return arr


# (0, f(0)) and (x_max, f(x_max)) points adding in "arr" if they're missing at one
def arr_edit(arr, in_on, in_le, cr_in, x_max):
    for i in range(len(arr)):
        if arr[i][:, in_on][0] > 0:
            f = np.poly1d(np.polyfit(arr[i][:, in_on][:2],
                                     arr[i][:, in_le][:2], 1))
            list_a = []
            for j in range(len(arr[i][0])):
                list_a.append(0)
            list_a[in_on] = 0
            list_a[cr_in] = arr[i][0][cr_in]
            list_a[in_le] = f(0)
            arr[i] = np.vstack([list_a, arr[i]])

        if arr[i][:, in_on][arr[i].shape[0] - 1] < x_max:
            f = np.poly1d(np.polyfit(arr[i][:, in_on][arr[i].shape[0] - 2:arr[i].shape[0]],
                                     arr[i][:, in_le][arr[i].shape[0] - 2:arr[i].shape[0]], 1))
            list_a = []
            for j in range(len(arr[i][0])):
                list_a.append(0)
            list_a[in_on] = x_max
            list_a[cr_in] = arr[i][0][cr_in]
            list_a[in_le] = f(x_max)
            arr[i] = np.vstack([arr[i], list_a])

    return arr


# max value in "arr" by "in_on" parameter
def max_value(arr, in_on):
    x_max = 0
    for i in range(len(arr)):
        if arr[i][:, in_on][arr[i].shape[0] - 1] > x_max:
            x_max = arr[i][:, in_on][arr[i].shape[0] - 1]

    return x_max


# array of curves => array of functions
def functioning_arr(arr, kind_interp, x, y):
    f_arr = []
    for i in range(len(arr)):
        f_arr.append(interp1d(arr[i][:, x], arr[i][:, y], kind=kind_interp))

    return f_arr


# creating array of differented functions from array of these functions
def arr_diff(f_arr, x_min, x_max, err_1, err_2):
    f_diff_arr = []
    for i in range(len(f_arr)):
        f_diff_arr.append(mf.diff(f_arr[i], x_min, x_max, err_1, err_2))

    return f_diff_arr


# creating array of integrated functions from array of these functions
def arr_integ(f_arr, x_min, x_max, err_1, err_2):
    f_integ_arr = []
    for i in range(len(f_arr)):
        f_integ_arr.append(mf.integ(f_arr[i], x_min, x_max, err_1, err_2))

    return f_integ_arr


def index_def(arr, val):
    for i in range(len(arr)):
        if val == arr[i]:
            return i
    return None


def step_def(curves_points, ini_num, fin_num):
    steps = []
    amount = []
    k = 0
    picket_temp = [ini_num]
    for i in range(ini_num, fin_num - 1):
        step = curves_points[i + 1][0][TEMP] - curves_points[i][0][TEMP]
        if (i != 0) and (step != (curves_points[i][0][TEMP] - curves_points[i - 1][0][TEMP])):
            k += 1
            picket_temp.append(i)
        if step in steps:
            amount[index_def(steps, step)] += 1
        else:
            steps.append(step)
            amount.append(1)
    picket_temp.append(fin_num - 1)

    n = sum(amount)
    max_proportion = amount[0] / n
    for i in range(len(amount)):
        if max_proportion < (amount[i] / n):
            max_proportion = amount[i] / n
    if max_proportion < 0.85:
        if k == (len(steps) - 1):
            step = steps
        else:
            step = None
    elif max_proportion < 0.3:
        step = None
    else:
        step = steps[index_def(steps, max(steps))]

    step_ = [step, picket_temp]

    return step_


def which_peak(extremum_value, curve, criter):
    index_extremum = index_def(curve[:, criter], extremum_value)
    if (index_extremum != 0) and (index_extremum != (len(curve) - 1)):
        if (curve[index_extremum - 1][criter] < extremum_value) and (
                curve[index_extremum + 1][criter] < extremum_value):
            return 'up_peak'
        else:
            return 'down_peak'
    else:
        return None


def curve_cutting(curve, cr, value):
    curve_up_to = np.array([curve[0]])
    curve_after = np.array([curve[index_def(curve[:, cr], value)]])

    for i in range(len(curve) - 1):
        if curve[i][cr] < value:
            curve_up_to = np.vstack([curve_up_to, curve[i + 1]])
        else:
            curve_after = np.vstack([curve_after, curve[i + 1]])

    return [curve_up_to, curve_after]


def sort_ascending_1(arr):
    for k in range(len(arr)):
        for i in range(len(arr) - k - 1):
            if arr[i + 1] < arr[i]:
                b = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = b

    return arr