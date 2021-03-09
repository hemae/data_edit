import spec_func as sf
import math_func as mf
from constants import *


def language_def(output_field_units):
    if output_field_units == 'T' \
            or output_field_units == 'Oe' \
            or output_field_units == 'kOe':
        language = 'en'
    else:
        language = 'ru'

    return language


def temperature_range_num(curves, initial_temp, final_temp):
    initial_num = 0
    while (curves['point'][initial_num][0][TEMP] < initial_temp):
        initial_num += 1
    final_num = len(curves['point']) - 1

    while (curves['point'][final_num][0][TEMP] > final_temp):
        final_num = final_num - 1
    final_num += 1

    nums = []
    nums.append(initial_num)
    nums.append(final_num)

    return nums


def max_field_update_for_many(curves, amount_of_samples, max_field):
    max_ = curves[0]['point'][0][-1][FIELD]
    for i in range(amount_of_samples):
        if max_ > curves[i]['point'][0][-1][FIELD]:
            max_ = curves[i]['point'][0][-1][FIELD]
    max_field_ = round(max_, -4)
    if (max_field == None) or (max_field > max_field_):
        max_field = max_field_

        return max_field
    else:

        return max_field


def range_temp_update(curves, amount_of_samples, initial_temp, final_temp):
    if amount_of_samples == 1:
        if initial_temp < curves['point'][0][0][TEMP]:
            initial_temp = curves['point'][0][0][TEMP]
        if final_temp > curves['point'][-1][0][TEMP]:
            final_temp = curves['point'][-1][0][TEMP]
        return [initial_temp, final_temp]
    for i in range(amount_of_samples):
        if initial_temp < curves[i]['point'][0][0][TEMP]:
            initial_temp = curves[i]['point'][0][0][TEMP]
        if final_temp > curves[i]['point'][-1][0][TEMP]:
            final_temp = curves[i]['point'][-1][0][TEMP]

    return [initial_temp, final_temp]


def range_temp_update_mine(initial_temp, final_temp, output_temp_units):
    if initial_temp == None:
        initial_temp = - 1E+4
    if final_temp == None:
        final_temp = 1E+4
    if output_temp_units == '°С':
        initial_temp = initial_temp + 273
        final_temp = final_temp + 273

    return [initial_temp, final_temp]


def max_field_update(curves, max_field):
    max_f = round(sf.max_value(curves['point'], FIELD), -4)
    if (max_field == None) or (max_field > max_f):
        max_field = max_f

    return max_field


def mce_max_curie(delta_s):
    for i in range(len(delta_s)):
        print(mf.maximum_of_point_func(delta_s[i], MCE, len(delta_s[i])))


### FOR UNITS
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


def file_name_separate(files):
    files_name = ''
    for file in files:
        num = len(file) - 1
        symbol = file[num]
        name = ''
        while symbol != '/':
            name = symbol + name
            num -= 1
            symbol = file[num]
        files_name = files_name + name + '\n'

    return files_name


def file_name_separate_one(filename):
    file_name = ''
    num = len(filename) - 1
    symbol = filename[num]
    name = ''
    while symbol != '/':
        name = symbol + name
        num -= 1
        symbol = filename[num]
    file_name = file_name + name

    return file_name


def catalog_separate(file_name):
    symbol = file_name[-1]
    while symbol != '/' and len(file_name) != 0:
        file_name = file_name[0:-1]
        symbol = file_name[-1]
    return file_name

def ar_create(file_name):
    in_file = open(file_name)  # "input.txt" file reading
    data = in_file.read()  # "data" is auxiliary string
    in_file.close()
    ar_data = data.split('\n')  # auxiliary array "ar_1" creating

    return ar_data


def brackets_del(string):
    string_1 = ''
    if '(' in string or ')' in string:
        for i in range(len(string)):
            if string[i] != '(' and string[i] != ')':
                string_1 = string_1 + string[i]
        return string_1
    else:
        return string


def is_numeral(symbol):
    try:
        int(symbol)
        return True
    except ValueError:
        return False


def symbol_in_point(string, symbol):
    s_1 = ''
    k = 0
    if symbol in string:
        while string[k] != symbol:
            s_1 = s_1 + string[k]
            k += 1
        if s_1 != string:
            s_1 = s_1 + '.'
            for i in range(k + 1, len(string)):
                s_1 = s_1 + string[i]
        return s_1
    else:
        return string


def digit_from_string(string):
    connecting_symbols = ['.', ',', '_']
    arr_digit_string = []
    arr_initial_num_symbol = []
    arr_final_num_symbol = []
    ini_num = 0
    while ini_num <= len(string):
        indicator = 0
        for i in range(ini_num, len(string)):
            if is_numeral(string[i]):
                indicator += 1
                arr_initial_num_symbol.append(i)
                k = i
                digit_string = ''
                while is_numeral(string[k]) or (string[k] in connecting_symbols):
                    digit_string += string[k]
                    k += 1
                    if k == len(string):
                        break
                arr_final_num_symbol.append(k)
                arr_digit_string.append(digit_string)
                ini_num = k
                break
        if indicator == 0:
            break

    for i in range(len(arr_digit_string)):
        if arr_digit_string[i][-1] in connecting_symbols:
            arr_digit_string[i] = arr_digit_string[i][:-1]

    for i in range(len(arr_digit_string)):
        for symbol in connecting_symbols:
            arr_digit_string[i] = symbol_in_point(arr_digit_string[i], symbol)

    return [arr_initial_num_symbol, arr_final_num_symbol, arr_digit_string]


def index_def(arr, val):
    for i in range(len(arr)):
        if val == arr[i]:
            return i
    return None


def copy_arr(arr):
    f = []
    for point in arr:
        f.append(point)

    return f