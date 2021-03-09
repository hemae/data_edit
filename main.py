import file_working as fw
import spec_func as sf
from constants import *
import math_func as mf
from rc_vs_h import integral_by_half_peak
from fitting import polinomial_fit
import matplotlib.pyplot as plt
import numpy as np
import os


def create_file(array, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units, vertical_units, mass, add_label='', x_coef=1, y_coef=1, x_add_coef=0, y_add_coef=0):
    try:
        os.makedirs(catalog + sample_name + depend_name, mode=0o777, exist_ok=False)
    except:
        pass
    output_file_name = catalog + sample_name + depend_name + sample_name + '_m=' + str(mass) + 'g_' + add_label
    file_output(output_file_name, array, 0, 1, horisontal_ax_name, vertical_ax_name, horisontal_units, vertical_units,
                x_coef=x_coef, y_coef=y_coef, x_coef_add=x_add_coef, y_coef_add=y_add_coef)


def field_coef_def(output_field_units):
    field_coef = 1
    if output_field_units == 'T' or output_field_units == 'Тл':
        field_coef = 1E-4
    elif output_field_units == 'kOe' or output_field_units == 'кЭ':
        field_coef = 1E-3

    return field_coef


def temp_coef_def(output_temp_units):
    temp_coef = 0
    if output_temp_units == '°С':
        temp_coef = -273.15

    return temp_coef


def moment_coef_def(mass, output_moment_units):
    moment_coef = 1
    if output_moment_units == 'emu/g' or output_moment_units == 'A*m2/kg' or output_moment_units == 'А*м2/кг':
        mass = 1
    elif output_moment_units == 'A*m2' or output_moment_units == 'А*м2':
        moment_coef = 1E-3

    return moment_coef * mass


def catalog_separate(file_name):
    symbol = file_name[-1]
    while symbol != '/' and len(file_name) != 0:
        file_name = file_name[0:-1]
        symbol = file_name[-1]
    return file_name


def file_output(file_name, arr, x_index, y_index, x_name, y_name, x_unit, y_unit, x_coef=1, y_coef=1, x_coef_add=0, y_coef_add=0):
    file = None
    k = 0
    add_index = '.txt'
    while file == None:
        if os.path.exists(file_name + add_index):
            k += 1
            add_index = '_' + str(k) + '.txt'
        else:
            file = open(file_name + add_index, 'w')
    file.write(x_name + '(' + x_unit + ') ' + y_name + '(' + y_unit + ')' + '\n')
    for i in range(len(arr)):
        file.write(str((arr[i][x_index] + x_coef_add) * x_coef) + ' ' + str((arr[i][y_index] + y_coef_add) * y_coef) + '\n')
    file.close()

    return None


def copy_arr(arr):
    copy_arr = []
    for element in arr:
        copy_arr.append(element)

    return copy_arr


def get_curves(file_name, mass, editing=False):    # file_name as cortege
    arr = fw.main_file_working(file_name)
    key_string = arr[0]
    arr_2 = arr[1]

    field_units = ['Oe', 'kOe', 'T', 'Э', 'кЭ', 'Тл']
    moment_units = ['emu', 'A*m2', 'А*м2']
    spec_moment_units = ['emu/g', 'A*m2/kg', 'А*м2/кг']
    temp_units = ['K', 'К', '°С']

    integration_index = None  # field H
    integrable_index = None  # moment M (m) (emu)
    criterion_index = None  # temperature T
    add_index = None  # moment (emu/g)
    for i in range(len(key_string)):  # column index indicating
        if key_string[i] in field_units:
            integration_index = i
        if key_string[i] in moment_units:
            integrable_index = i
        if key_string[i] in temp_units:
            criterion_index = i
        if key_string[i] in spec_moment_units:
            add_index = i
    if integrable_index == None or add_index != None:
        integrable_index = add_index
        mass = 1

    koef = 1
    if key_string[integration_index] == 'kOe' \
            or key_string[integration_index] == 'кЭ':
        koef = 1E+3
    elif key_string[integration_index] == 'T' \
            or key_string[integration_index] == 'Тл':
        koef = 1E+4

    points = []
    for i in range(len(arr_2)):
        points.append([])
        points[i].append(arr_2[i][integrable_index] / mass)  # in emu/g
        points[i].append(arr_2[i][integration_index] * koef)  # all calculatings in Oe
        if key_string[criterion_index] == '°С':  # in Kelvins
            points[i].append(arr_2[i][criterion_index] + 273.15)
        else:
            points[i].append(arr_2[i][criterion_index])

    accuracy = 1  # accuracy of criterion step as fraction (for example: 1 K)
    curves_M_H = sf.create_curves(points, accuracy, TEMP, editing)
    del points

    curves_M_H = sf.sort_ascending(curves_M_H, FIELD)
    curves_M_H = sf.sort_ascending_curves(curves_M_H, TEMP)

    for i in range(len(curves_M_H)):
        curves_M_H[i] = sf.np_arr(curves_M_H[i])

    H_max = sf.max_value(curves_M_H, FIELD)
    H_max_rounded = round(H_max, -4)
    curves_M_H = sf.arr_edit(curves_M_H, FIELD, MOMENT, TEMP,
                             H_max_rounded)  # (0, f(0)) and (x_max, f(x_max)) points adding in "arr" if they're missing at one

    # linear interpolation
    kind_interp = 'linear'
    f_curves_M_H = sf.functioning_arr(curves_M_H, kind_interp, FIELD, MOMENT)

    curves = {
        'point': curves_M_H,
        'func': f_curves_M_H
    }

    return curves
# получаем массив точек из файла,
# разделенных по критерию температуры T:
# [
#   [
#    [M1, H1, T1],
#    [M2, H2, T1],
#    ...........  ],
#
#  [
#   [M1, H1, T2],
#   [M2, H2, T2],
#   ............ ],
#  ...............
# ]


def cut_curves_temp(curves_, ini_temp, fin_temp):
    curves = {
        'point': [],
        'func': []
    }
    for i in range(len(curves_['point'])):
        if (curves_['point'][i][0][TEMP] >= ini_temp) and (curves_['point'][i][0][TEMP] <= fin_temp):
            curves['point'].append(curves_['point'][i])
            curves['func'].append(curves_['func'][i])

    return curves
# оставляем в массиве кривых только кривые от начальной температуры ini_temp до конечной температуры fin_temp


def cut_curves_field(curves_, field):
    curves = {
        'point': [],
        'func': []
    }
    for curve in curves_['point']:
        new_curve = []
        for i in range(len(curve)):
            if curve[i][FIELD] > field:
                break
            new_curve.append(curve[i])
        curves['point'].append(new_curve)
    for func in curves_['func']:
        curves['func'].append(func)

    return curves
# формируем массив с точками со значением поля меньше или равно field


def get_mec(curves):
    curve = []
    for i in range(len(curves['func']) - 1):
        point = []
        temp = round((curves['point'][i + 1][0][TEMP] + curves['point'][i][0][TEMP]) / 2, 1)
        point.append(temp)
        max_field = curves['point'][i][-1][FIELD]
        mec = (mf.func_integral(curves['func'][i + 1], 0, max_field, 2) - mf.func_integral(curves['func'][i], 0, max_field, 2)) / ((curves['point'][i + 1][0][TEMP] - curves['point'][i][0][TEMP]) * 1E+4)
        point.append(mec)
        curve.append(point)

    return curve
# получаем кривую изменения магнитной энтропии dS(T) из массива данных curves
# при определенном поле H (field) и массе m mass как массив точек:
# [
#  [T1, dS1],
#  [T2, dS2],
#  ...
# ]


def get_der_curve(curve):
    returning_curve = []
    for i in range(len(curve) - 1):
        new_point = []
        x = round((curve[i + 1][0] + curve[i][0]) / 2, 1)
        new_point.append(x)
        delta_x = curve[i + 1][0] - curve[i][0]
        delta_y = curve[i + 1][1] - curve[i][1]
        y = delta_y / delta_x
        new_point.append(y)
        returning_curve.append(new_point)

    return returning_curve
# получаем кривую производной из массива кривой curve [[x1, y1], [x2, y2], ...] как массив точек:
# [
#  [x1, d_y1],
#  [x2, d_y2],
#  ...
# ]


def get_cross_zero(curve):
    x_cross = 295
    for i in range(len(curve) - 1):
        if curve[i + 1][1] * curve[i][1] < 0:
            x1, x2 = curve[i][0], curve[i + 1][0]
            y1, y2 = curve[i][1], curve[i + 1][1]
            x_cross = (y2 * x1 - y1 * x2) / (y2 - y1)

    return x_cross
# получаем точку пересечения кривой curve [x0, y0] с Ox


def get_rc(mec):    # для ферромагнетика
    f = copy_arr(mec)
    f = sf.np_arr(f)
    integ = integral_by_half_peak(f, typ='min')

    return integ
# получаем значение интеграла dS(T)dT от T1 до T2, если это возможно
# T1 - координата точки значения половины значения пика кривой изменения энтропии слева
# T2 - справа


def get_bel_arr(curves_):
    curves = []
    for i in range(len(curves_)):
        curve = []
        for point in curves_[i]:
            new_point = []
            try:
                x = point[FIELD] / point[MOMENT]
                y = point[MOMENT] * point[MOMENT]
                new_point.append(x)
                new_point.append(y)
                new_point.append(point[TEMP])
                curve.append(new_point)
            except:
                pass
        curves.append(curve)

    return curves
# получаем набор кривых Белова-Арротта как массив точек,
# разделенных по критерию температуры T:
# [
#   [
#    [M1^2, H1/M1, T1],
#    [M2^2, H2/M1, T1],
#    ...........  ],
#
#  [
#   [M1^2, H1/M1, T2],
#   [M2^2, H2/M1, T2],
#   ............ ],
#  ...............
# ]


def get_alpha(b_a_curves):
    curve = []
    for b_a_curve in b_a_curves:
        point = []
        arr = []
        for j in range(11):
            try:
                point_arr = []
                point_arr.append(b_a_curve[-1 - j][0])
                point_arr.append(b_a_curve[-1 - j][1])
                arr.append(point_arr)
            except:
                pass
        parameters = polinomial_fit(arr, n=1)
        point.append(b_a_curve[0][2])
        point.append(- parameters[0] / parameters[1])
        curve.append(point)

    return curve
# получаем значение коэффициента alpha как функцию температуры T:
# массив точек: [[T1, alpha1], [T2, alpha2], ...]


def get_moment(curves_):
    curve = []
    for curve_ in curves_['point']:
        point = []
        point.append(curve_[0][TEMP])
        point.append(curve_[-1][MOMENT])
        curve.append(point)

    return curve
# получаем кривую момента m(T) из массива данных curves
# при определенном поле H (field) как массив точек:
# [
#  [T1, M1],
#  [T2, M2],
#  ...
# ]


# def rnd(number):
#     num = number
#     k = 1
#     while num // 10 > 0:
#         k += 1
#         num = num // 10
#
#     return round(number, - (k - 4))


def get_field_points():
    field_points = []
    x = 100
    while x < 500:
        field_points.append(x)
        x += 100
    while x < 5000:
        field_points.append(x)
        x += 250
    while x < 70000:
        field_points.append(x)
        x += 2500
    field_points.append(70000)
    field_points[-1] = field_points[-1] * 0.99999999999

    return field_points
# получаем массив точек магнитного поля H из curves


def get_extr_value(curve, point_of_extr):
    for i in range(len(curve)):
        if curve[i][0] > point_of_extr:
            if curve[i][1] > curve[i - 1][1]:
                return curve[i][1]
            else:
                return curve[i - 1][1]


def get_extr_mec_vs_field(field_points, curves_, kind=''):
    curve = []
    for field in field_points:
        point = []
        point.append(field)
        curves = cut_curves_field(curves_, field)
        magnetic_entropy_change = get_mec(curves)  # получаем кривую изменения энтропии dS(T)
        der_magnetic_entropy_change = get_der_curve(magnetic_entropy_change)  # получаем производную кривой изменения энтропии dS(T) по температуре T
        point_of_extr = get_cross_zero(der_magnetic_entropy_change)  # получаем точку экстремума кривой изменения энтропии
        extremum_of_magnetic_entropy_change = get_extr_value(magnetic_entropy_change, point_of_extr)  # получаем значение экстремума кривой изменения энтропии
        if kind == 'values':
            point.append(extremum_of_magnetic_entropy_change)
        else:
            point.append(point_of_extr)
        curve.append(point)

    return curve
# получаем экстремальное значение(координаты значения) dSmax как функцию от поля H field_points
# как массив точек [[H1, dSmax1], [H2, dSmax2], ...]


def get_extr_moment_vs_field(field_points, curves_):
    curve = []
    for field in field_points:
        point = []
        point.append(field)
        curves = cut_curves_field(curves_, field)
        moment = get_moment(curves)  # получаем кривую магнитного момента m(T)
        der_moment = get_der_curve(moment)  # получаем производную кривой магнитного момента m(T) по температуре T
        der_der_moment = get_der_curve(der_moment)
        extremum_of_moment = get_cross_zero(der_der_moment)  # получаем точку экстремума кривой m(T)
        point.append(extremum_of_moment)
        curve.append(point)

    return curve
# получаем экстремальное значение(координаты значения) moment как функцию от поля H field_points
# как массив точек [[H1, M1], [H2, M2], ...]


def get_rc_vs_field(field_points, curves_):
    curve = []
    for field in field_points:
        point = []
        point.append(field)
        curves = cut_curves_field(curves_, field)
        magnetic_entropy_change = get_mec(curves)  # получаем кривую изменения энтропии dS(T)
        refrigeration_capacity = get_rc(magnetic_entropy_change)    # получаем значение RC
        print(refrigeration_capacity)
        if refrigeration_capacity != None:
            point.append(refrigeration_capacity)
            curve.append(point)

    return curve
# получаем RC(H) как массив точек [[H1, RC1], [H2, RC2], ...]


def get_cur_temp_vs_field(field_points_, curves_):
    field_points = []
    for field_point in field_points_:
        field_points.append(field_point)
    for i in range(11):
        del field_points[0]
    curve = []
    for field in field_points:
        point = []
        point.append(field)
        curves = cut_curves_field(curves_, field)
        belov_arrott_curves = get_bel_arr(curves['point'])  # получаем массив кривых в координатах Белова-Арротта (в виде массива точек) из curves
        alpha = get_alpha(belov_arrott_curves)  # получаем значение коэффициента alpha как функцию температуры T из кривых Б.-А.
        curie_temperature = get_cross_zero(alpha)  # получаем температуру Кюри из alpha
        point.append(curie_temperature)
        curve.append(point)

    return curve
# получаем Tc(H) как массив точек [[H1, Tc1], [H2, Tc2], ...]


def transform_arr(arr):
    arr = np.array(arr)
    arr = arr.transpose()

    return arr


def show_graph(x_y_arr):
    for element in x_y_arr:
        plt.plot(element[0], element[1])
    plt.grid(True)
    plt.show()



file_name = ('./files/as-quenched.txt',)
catalog = catalog_separate(file_name[0])
field = 70000
mass = 1.54E-3
ini_temp = 200
fin_temp = 350

sample_name = 'Gd_perp'
output_field_units = 'T'
output_moment_units = 'emu/g'
output_temp_units = 'K'

curves = get_curves(file_name, mass)  # получаем массив кривых (в виде массива точек) из файла
curves = cut_curves_temp(curves, ini_temp, fin_temp)

field_points = get_field_points() # получаем массив точек магнитного поля H
# print(field_points)





# print(curves)
# curves_ = cut_curves_field(curves, field)
# print(curves_)

#M(H)
# curves_set = []
# for curve in curves_['point']:
#     print(curve)
#     curves_set.append([curve[:, 1], curve[:, 0]])
# show_graph(curves_set)



# curves_ = cut_curves_field(curves, field)
# moment = get_moment(curves_)  # получаем кривую магнитного момента m(T)
# der_moment = get_der_curve(moment)
# der_der_moment = get_der_curve(der_moment)

# выводим файл m(T)
# horisontal_ax_name = 'Temperature'
# vertical_ax_name = 'Moment'
# depend_name = '/m(T)/'
# horisontal_units = output_temp_units
# vertical_units = output_moment_units
# y_coef = moment_coef_def(mass, output_moment_units)
# add_label = 'H=' + str(field * field_coef_def(output_field_units)) + '_' + output_field_units
# create_file(moment, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units, vertical_units, mass, add_label, y_coef)

# выводим файл dm/dT(T)
# horisontal_ax_name = 'Temperature'
# vertical_ax_name = 'Moment/Temperature'
# depend_name = '/dmdT(T)/'
# horisontal_units = output_temp_units
# vertical_units = output_moment_units + '/' + output_temp_units
# y_coef = moment_coef_def(mass, output_moment_units)
# add_label = 'H=' + str(field * field_coef_def(output_field_units)) + '_' + output_field_units
# create_file(der_moment, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, add_label, y_coef)

# выводим файл d2m/dT2(T)
# horisontal_ax_name = 'Temperature'
# vertical_ax_name = 'Moment/Temperature2'
# depend_name = '/d2mdT2(T)/'
# horisontal_units = output_temp_units
# vertical_units = output_moment_units + '/' + output_temp_units + '2'
# y_coef = moment_coef_def(mass, output_moment_units)
# add_label = 'H=' + str(field * field_coef_def(output_field_units)) + '_' + output_field_units
# create_file(der_der_moment, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, add_label, y_coef)

# получаем m(T, H=field), dm/dT и d2m/dT2
# moment = transform_arr(moment)
# show_graph([[moment[0, :], moment[1, :]]])
# der_moment = transform_arr(der_moment)
# show_graph([[der_moment[0, :], der_moment[1, :]]])
# der_der_moment = transform_arr(der_der_moment)
# show_graph([[der_der_moment[0, :], der_der_moment[1, :]]])




# curves_ = cut_curves_field(curves, field)
# magnetic_entropy_change = get_mec(curves_)  # получаем кривую изменения энтропии dS(T)
# der_magnetic_entropy_change = get_der_curve(magnetic_entropy_change)

# выводим файл dS(T)
# horisontal_ax_name = 'Temperature'
# vertical_ax_name = 'MECh'
# depend_name = '/dS(T)/'
# horisontal_units = output_temp_units
# vertical_units = 'J/kg * K'
# add_label = 'H=' + str(field * field_coef_def(output_field_units)) + '_' + output_field_units
# create_file(magnetic_entropy_change, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, add_label)

# выводим файл dS/dT(T)
# horisontal_ax_name = 'Temperature'
# vertical_ax_name = 'MECh_der_K'
# depend_name = '/dSdT(T)/'
# horisontal_units = output_temp_units
# vertical_units = 'J/kg * K2'
# add_label = 'H=' + str(field * field_coef_def(output_field_units)) + '_' + output_field_units
# create_file(der_magnetic_entropy_change, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, add_label)

# получаем dS(T, H=field) и dS/dT
# magnetic_entropy_change = transform_arr(magnetic_entropy_change)
# show_graph([[magnetic_entropy_change[0, :], -magnetic_entropy_change[1, :]]])
# der_magnetic_entropy_change = transform_arr(der_magnetic_entropy_change)
# show_graph([[der_magnetic_entropy_change[0, :], -der_magnetic_entropy_change[1, :]]])




extremum_of_mec_vs_field = get_extr_mec_vs_field(field_points, curves, kind='values') # получаем dSmax(H)
# print(extremum_of_mec_vs_field)

# выводим файл dSmax(H)
# horisontal_ax_name = 'Magnetic Field'
# vertical_ax_name = 'MECh'
# depend_name = '/dSmax(H)/'
# horisontal_units = output_field_units
# vertical_units = 'J/kg * K'
# x_coef = field_coef_def(output_field_units)
# add_label = str(ini_temp) + output_temp_units + '_' + str(fin_temp) + output_temp_units
# create_file(extremum_of_mec_vs_field, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, add_label, x_coef)

# получаем dSmax(H)
extremum_of_mec_vs_field = transform_arr(extremum_of_mec_vs_field)
show_graph([[extremum_of_mec_vs_field[0, :], -extremum_of_mec_vs_field[1, :]]])




# temperature_extremum_of_mec_vs_field = get_extr_mec_vs_field(field_points, curves, kind='points') # получаем T_dSmax(H)
# print(temperature_extremum_of_mec_vs_field)

# выводим файл T_dSmax(H)
# horisontal_ax_name = 'Magnetic Field'
# vertical_ax_name = 'max_mec_temp'
# depend_name = '/T_dSmax(H)/'
# horisontal_units = output_field_units
# vertical_units = 'K'
# x_coef = field_coef_def(output_field_units)
# create_file(temperature_extremum_of_mec_vs_field, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, x_coef=x_coef)

# получаем T_dSmax(H)
# temperature_extremum_of_mec_vs_field = transform_arr(temperature_extremum_of_mec_vs_field)
# show_graph([[temperature_extremum_of_mec_vs_field[0, :], temperature_extremum_of_mec_vs_field[1, :]]])




# refrigeration_capacity_vs_field = get_rc_vs_field(field_points, curves) # получаем RC(H)
# print(refrigeration_capacity_vs_field)

# выводим файл RC(H)
# horisontal_ax_name = 'Magnetic Field'
# vertical_ax_name = 'RC'
# depend_name = '/RC(H)/'
# horisontal_units = output_field_units
# vertical_units = 'J/kg'
# x_coef = field_coef_def(output_field_units)
# add_label = str(ini_temp) + output_temp_units + '_' + str(fin_temp) + output_temp_units
# create_file(refrigeration_capacity_vs_field, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, add_label, x_coef)

# получаем RC(H)
# refrigeration_capacity_vs_field = transform_arr(refrigeration_capacity_vs_field)
# show_graph([[refrigeration_capacity_vs_field[0, :], refrigeration_capacity_vs_field[1, :]]])




# temperature_extremum_of_moment_vs_field = get_extr_moment_vs_field(field_points, curves) # получаем T_m_extr(H)
# print(temperature_extremum_of_moment_vs_field)

# выводим файл T_m_extr(H)
# horisontal_ax_name = 'Magnetic Field'
# vertical_ax_name = 'max_temp_der_moment'
# depend_name = '/T_m_extr(H)/'
# horisontal_units = output_field_units
# vertical_units = 'K'
# x_coef = field_coef_def(output_field_units)
# add_label = str(ini_temp) + output_temp_units + '_' + str(fin_temp) + output_temp_units
# create_file(temperature_extremum_of_moment_vs_field, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, add_label, x_coef)

# T_m_extr(H)
# temperature_extremum_of_moment_vs_field = transform_arr(temperature_extremum_of_moment_vs_field)
# show_graph([[temperature_extremum_of_moment_vs_field[0, :], temperature_extremum_of_moment_vs_field[1, :]]])




# curie_temperature_vs_field = get_cur_temp_vs_field(field_points, curves) # получаем Tc(H) методом Б.-А.
# print(curie_temperature_vs_field)

# выводим файл Tc(H)
# horisontal_ax_name = 'Magnetic Field'
# vertical_ax_name = 'Curie_temp'
# depend_name = '/Tc(H)/'
# horisontal_units = output_field_units
# vertical_units = 'K'
# x_coef = field_coef_def(output_field_units)
# create_file(curie_temperature_vs_field, catalog, sample_name, depend_name, horisontal_ax_name, vertical_ax_name, horisontal_units,
#             vertical_units, mass, x_coef=x_coef)

# Tc(H) B-A
# curie_temperature_vs_field = transform_arr(curie_temperature_vs_field)
# show_graph([[curie_temperature_vs_field[0, :], curie_temperature_vs_field[1, :]]])




# сравниваем диаграммы Tc(H) полученные различными способами
# temperature_extremum_of_mec_vs_field = transform_arr(temperature_extremum_of_mec_vs_field)
# temperature_extremum_of_moment_vs_field = transform_arr(temperature_extremum_of_moment_vs_field)
# curie_temperature_vs_field = transform_arr(curie_temperature_vs_field)
# need_to_show = [
#     [temperature_extremum_of_mec_vs_field[0, :], temperature_extremum_of_mec_vs_field[1, :]],
#     [temperature_extremum_of_moment_vs_field[0, :], temperature_extremum_of_moment_vs_field[1, :]],
#     [curie_temperature_vs_field[0, :], curie_temperature_vs_field[1, :]]
# ]
# show_graph(need_to_show)