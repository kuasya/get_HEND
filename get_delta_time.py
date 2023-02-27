import os

list_files1 = os.listdir('HEND_correct')  # список файлов в папке
# print(list_files1)

list_files2 = os.listdir('HEND_incorrect')
# print(list_files2)


def delta(element):
    # функция определения разности времен (delta_time) двух файлов

    global b1, j, line1, line2, delta_line

    # Условие совпадения последовательностей
    if j == 100:
        return float(line2[0]) - float(line1[0])

    # Сравниваем два файла
    if b1 == element:
        # если элементы совпадают, сравниваем следующую пару элементов
        j += 1
        line1 = f1.readline().split()
        line2 = f2.readline().split()

        b1 = line1[1]
        element = line2[1]
        return delta(element)

    else:
        # если элементы не совпадают, переходим на новую строку
        j = 0
        line2 = f2.readline().split()
        delta_line += 1
        element = line2[1]
        return delta(element)  # сравниваем новую пару элементов


delta_times_list = []

# В каждой паре файлов correct-incorrect находим delta_time
for k in range(len(list_files1)):
    with open('HEND_correct/'+list_files1[k]) as f1:
        for i in range(3):
            f1.readline()

        # Учитываем, что имя файла incorrect может отличаться на +1
        try:
            f2 = open('HEND_incorrect/' + list_files1[k])
        except FileNotFoundError:
            new = list_files1[k][:13] + str(int(list_files1[k][13:14])+1) + list_files1[k][14::]
            f2 = open('HEND_incorrect/' + new)

        for i in range(3):
            f2.readline()

        # Сравниваем последовательности двух файлов
        line1 = f1.readline().split()
        line2 = f2.readline().split()
        b1 = line1[1]  # первый элемент последовательности для f1
        b2 = line2[1]  # f2
        delta_line = 4  # начало последовательности
        j = 0
        delta_time = delta(b2)  # отклонение во времени

        # Формируем список delta_time для всех пар
        delta_times_list += [delta_time]
        # print(list_files1[k], 'отклонение', delta_time, 'сек, строка', delta_line)

# print(delta_times_list)

# this part is in get_hend
#
# data = ''
# time = 0
#
#
# def get_data(a):
#     with open('HEND_correct/'+a) as f:
#         global data, time
#         line = f.readline().split()
#         data = line[3]
#         time = float(line[4]) + 1350
#
#         data = data.strip("'")
#         data = data.split('/')
#         data = '20'+data[2]+'-'+data[1]+'-'+data[0]
#
#         if time >= 86400:
#             if data[-1] != '9':
#                 data = data[:-1] + str(int(data[-1])+1)
#             else:
#                 data = data[:-2] + str(int(data[-2]) + 1) + '0'
#             time -= 86400
#         time = round(time, 3)
#
#
# list_files = os.listdir('HEND_correct')
# # print(list_files)
#
# for name in list_files:
#     file_name = name
#     get_data(file_name)
#     print(data, time)

