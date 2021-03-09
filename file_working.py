from math_func import is_digit
from help_functions import ar_create, index_def
import os


def measuring_device_definition(tuple_files_names):
    k = 0
    while os.path.splitext(tuple_files_names[k])[1] != '.dat':
        k += 1
        if k == len(tuple_files_names):
            k -= 1
            break

    measuring_device = None
    if os.path.splitext(tuple_files_names[k])[1] == '.dat':
        ar_data = ar_create(tuple_files_names[k])

        for i in range(len(ar_data)):
            if 'DYNACOOL' in ar_data[i]:
                measuring_device = 'DynaCool'
                break
            if 'SQUID' in ar_data[i]:
                measuring_device = 'SQUID'
                break
            if 'TemperatureUnit' in ar_data[i]:
                measuring_device = 'LakeShore'
                break
            if 'MPMS' in ar_data[i] and ('DC' in ar_data[i] or 'RSO' in ar_data[i]):
                measuring_device = 'MPMS'
                break

    return measuring_device


def minus_values_del(arr, field_index):
    i = 0
    while i < (len(arr) - 1):
        for i in range(len(arr)):
            if arr[i][field_index] < -1:
                del arr[i]
                break

    return arr


def comma_in_point(string):
    s_1 = ''
    k = 0
    if ',' in string:
        while string[k] != ',':
            s_1 = s_1 + string[k]
            k += 1
        if s_1 != string:
            s_1 = s_1 + '.'
            for i in range(k + 1, len(string)):
                s_1 = s_1 + string[i]
        return s_1
    else:
        return string


def brackets_del(string):
    string_1 = ''
    if '(' in string or ')' in string:
        for i in range(len(string)):
            if string[i] != '(' and string[i] != ')':
                string_1 = string_1 + string[i]
        return string_1
    else:
        return string


def key_string_lakeshore_definition(tuple_files_names):
    for i in range(len(tuple_files_names)):
        if os.path.splitext(tuple_files_names[i])[1] == '.dat':
            ar_data = ar_create(tuple_files_names[i])

            temp_unit = None
            field_unit = None
            moment_unit = None
            for j in range(len(ar_data)):
                if 'TemperatureUnit' in ar_data[j]:
                    temp_unit = ar_data[j].split()[1]
                if 'MomentUnit' in ar_data[j]:
                    moment_unit = ar_data[j].split()[1]
                if 'AppliedFieldUnit' in ar_data[j]:
                    field_unit = ar_data[j].split()[1]
            return [field_unit, moment_unit, temp_unit]

    return None


def key_string_definition(tuple_files_names):
    ar_data = ar_create(tuple_files_names[0])

    key_string = None
    for i in range(len(ar_data)):
        if '[Data]' in ar_data[i]:
            key_string = ar_data[i + 1].split(',')
            break
    for i in range(len(key_string)):
        if 'Temperature' in key_string[i]:
            key_string[i] = brackets_del(key_string[i].split()[-1])
            break
    for i in range(len(key_string)):
        if 'Moment' in key_string[i] or 'moment' in key_string[i]:
            key_string[i] = brackets_del(key_string[i].split()[-1])
            break
    for i in range(len(key_string)):
        # if 'Magnetic Field' in key_string[i]:
        if 'Field' in key_string[i]:
            key_string[i] = brackets_del(key_string[i].split()[-1])
            break

    return key_string


def create_arr_part_1(s_file_name, beginning_string, split_symbol, another_mode=False):
    in_file = open(s_file_name)  # "input.txt" file reading
    data = in_file.read()  # "data" is auxiliary string
    in_file.close()

    ar_1 = data.split('\n')  # auxiliary array "ar_1" creating
    for i in range(beginning_string):
        del ar_1[0]
    del data

    k = 0
    while ar_1[k] == '':
        del ar_1[k]
        k += 1

    k = len(ar_1) - 1
    while ar_1[k] == '':
        del ar_1[k]
        k -= 1

    # if ar_1[-1] == '':
    #     del ar_1[-1]

    if another_mode == True:
        while not ('Oe' in ar_1[0]) and not ('T' in ar_1[0]) and not ('Тл' in ar_1[0]) and not ('Э' in ar_1[0]):
            del ar_1[0]
        for i in range(len(ar_1[0])):
            if (ar_1[0][i] == ',') and (i != (len(ar_1[0]) - 1)):
                split_symbol = ','
            elif (ar_1[0][i] == '.') and (i != (len(ar_1[0]) - 1)):
                split_symbol = '.'
            elif (ar_1[0][i] == ';') and (i != (len(ar_1[0]) - 1)):
                split_symbol = ';'
            elif (ar_1[0][i] == ':') and (i != (len(ar_1[0]) - 1)):
                split_symbol = ':'
            elif (ar_1[0][i] == '_') and (i != (len(ar_1[0]) - 1)):
                split_symbol = '_'
            else:
                split_symbol = ''

    ar_2 = []  # main array "ar_2" creating
    for i in range(len(ar_1)):
        if split_symbol == '':
            ar_2.append(ar_1[i].split())
        else:
            ar_2.append(ar_1[i].split(split_symbol))
    del ar_1

    return ar_2


def create_arr_part_2(ar_1, ini_index, fin_index):
    ar_2 = ar_1
    am_el = len(ar_2[0])  # "am_el" amount of elements in one point, it needs for array "ar_2" editing

    for i in range(len(ar_2)):  # float-string array "ar_2" transformation
        for j in range(len(ar_2[i])):
            ar_2[i][j] = comma_in_point(ar_2[i][j])

    k = 0  # array "ar_2" editing (excess points deleting)
    while k < len(ar_2):
        if len(ar_2[k]) != am_el:  # ATTENTION, it depends on "am_el" (amount of columns or elements)
            ar_2.pop(k)
            k -= 1
        else:
            # for j in range(len(ar_2[k])):
            for j in range(ini_index, fin_index + 1):
                if not is_digit(ar_2[k][j]):
                    ar_2.pop(k)
                    k -= 1
                    break
        k += 1

    for i in range(len(ar_2)):  # float-string array "ar_2" transformation
        # for j in range(len(ar_2[i])):
        for j in range(ini_index, fin_index + 1):
            ar_2[i][j] = float(ar_2[i][j])

    return ar_2


def create_temp_arr(s_file_name):
    in_file = open(s_file_name)  # "input.txt" file reading
    data = in_file.read()  # "data" is auxiliary string
    in_file.close()

    ar_1 = data.split('\n')  # auxiliary array "ar_1" creating
    for i in range(280):
        del ar_1[0]
    del data

    temp_arr = []
    m = 0
    while is_digit(ar_1[m]):
        temp_arr.append(float(ar_1[m]))
        m += 1

    return temp_arr


def ini_fin_index_definition(key_string):
    field_index = index_def(key_string, 'Oe')
    if field_index == None:
        field_index = index_def(key_string, 'kOe')
    if field_index == None:
        field_index = index_def(key_string, 'T')

    moment_index = index_def(key_string, 'emu')

    moment_g_index = index_def(key_string, 'emu/g')

    temp_index = index_def(key_string, 'K')
    if temp_index == None:
        temp_index = index_def(key_string, '°С')

    index_arr = [field_index, moment_index, moment_g_index, temp_index]
    for i in range(len(index_arr)):
        if index_arr[i] == None:
            del index_arr[i]
            break

    return [min(index_arr), max(index_arr)]


def file_working_lakeshore(tuple_files_names):
    key_string = key_string_lakeshore_definition(tuple_files_names)

    ini_index = 0
    fin_index = 1

    arr = []
    arr_temp = []
    m = -1
    for filename in tuple_files_names:
        if os.path.splitext(filename)[1] == '.txt':
            arr.append(create_arr_part_2(create_arr_part_1(filename, 12, ''), ini_index, fin_index))
            m += 1
            for filename_ in tuple_files_names:
                if os.path.splitext(filename_)[0] == os.path.splitext(filename)[0] and os.path.splitext(filename_)[
                    1] == '.dat':
                    arr_temp = create_temp_arr(filename_)
            for j in range(len(arr[m])):
                arr[m][j].append(arr_temp[j])

    for i in range(len(arr)):
        del arr[i][-1]

    arr_1 = []
    for i in range(len(arr)):
        for point in arr[i]:
            arr_1.append(point)
    del arr

    try:
        arr_1 = minus_values_del(arr_1, index_def(key_string, 'Oe'))
    except TypeError:
        try:
            arr_1 = minus_values_del(arr_1, index_def(key_string, 'kOe'))
        except TypeError:
            try:
                arr_1 = minus_values_del(arr_1, index_def(key_string, 'T'))
            except TypeError:
                pass

    return (key_string, arr_1)


def file_working(tuple_files_names, beg_str):
    key_string = key_string_definition(tuple_files_names)

    ini_fin_indexes = ini_fin_index_definition(key_string)
    ini_index = ini_fin_indexes[0]
    fin_index = ini_fin_indexes[1]

    arr = []
    for filename in tuple_files_names:
        arr.append(create_arr_part_2(create_arr_part_1(filename, beg_str, ','), ini_index, fin_index))

    arr_1 = []
    for i in range(len(arr)):
        for point in arr[i]:
            arr_1.append(point)
    del arr

    try:
        arr_1 = minus_values_del(arr_1, index_def(key_string, 'Oe'))
    except TypeError:
        try:
            arr_1 = minus_values_del(arr_1, index_def(key_string, 'kOe'))
        except TypeError:
            try:
                arr_1 = minus_values_del(arr_1, index_def(key_string, 'T'))
            except TypeError:
                pass

    return (key_string, arr_1)


def file_working_another(file_name):
    arr_1 = create_arr_part_1(file_name, 0, '', another_mode=True)
    key_string = arr_1[0]  # "key_string" is string of columns names
    ini_fin_indexes = ini_fin_index_definition(key_string)
    ini_index = ini_fin_indexes[0]
    fin_index = ini_fin_indexes[1]
    arr_2 = create_arr_part_2(arr_1, ini_index, fin_index)  # this is just points (without sorting and distribution)
    del arr_1

    return (key_string, arr_2)


def main_file_working(tuple_files_names):
    measuring_device = measuring_device_definition(tuple_files_names)
    if measuring_device == 'LakeShore':
        data = file_working_lakeshore(tuple_files_names)
    elif measuring_device == 'SQUID':
        data = file_working(tuple_files_names, 27)
    elif measuring_device == 'DynaCool' or measuring_device == 'MPMS':
        data = file_working(tuple_files_names, 30)
    else:
        data = file_working_another(tuple_files_names[0])

    return data
