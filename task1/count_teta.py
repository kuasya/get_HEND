import csv
import math

# Открываем файл для записи данных
with open('example.txt', 'w') as f:
    print()

# Создаем конструктор записи (в табличном формате)
example = open('example.txt', 'a')
writer = csv.writer(example, delimiter='\t', lineterminator='\n')

# Формируем заголовок таблицы
row_writer = ['Lokal      ', 'Galactic     ', 'Teta            ', 'R +- err']
writer.writerow(row_writer)

# Открываем первый файл "Единая таблица локализаций"
with open('Edinaya_tablitsa_lokalizatsiy.txt') as f1:
    f1.readline().strip()
    file1 = csv.reader(f1, delimiter='\t')

    # Построчно считываем alfa и delta из первого файла,
    # а также lokal, R, error R
    for row in file1:
        if str(row[0]) != '':
            i = 0
            if str(row[0])[0] != ' ':
                lokal = (row[0]).split()[0]
                alfa1 = float((row[0]).split()[1])
                delta1 = float((row[0]).split()[2])
                r = float((row[0]).split()[3])
                error_r = float((row[0]).split()[4])
            else:
                lokal = lokal
                alfa1 = float((row[0]).split()[0])
                delta1 = float((row[0]).split()[1])
                r = float((row[0]).split()[2])
                error_r = float((row[0]).split()[3])

            # Работа со вторым файлом "Каталог галактик"
            # (для каждой строчки из первого файла)
            with open('Katalog_galaktik (1).txt') as f2:
                f2.readline().strip()
                file2 = csv.reader(f2, delimiter='\t')
                for row2 in file2:
                    galactic = row2[0].strip()  # галактика

                    # Получаем alfa и delta из второго файла
                    try:
                        alfa2 = float(row2[1])
                        try:
                            delta2 = float(row2[2])
                        # учитываем различный формат исходных данных
                        except ValueError:
                            delta2 = float(row2[2].split()[0])
                    except ValueError:
                        alfa2 = float(row2[1].split()[0])
                        delta2 = float(row2[1].split()[1])

                    # Вычисляем teta по формуле:
                    teta = math.acos(math.sin(delta1)*math.sin(delta2)+math.cos(delta1)*math.cos(delta2)*math.cos(alfa1-alfa2))
                    teta = teta*180/math.pi  # перевод в градусы

                    interval = str(r) + '+-' + str(error_r)
                    # Находим teta, удовлетворяющий условию:
                    if r - error_r < teta < r + error_r:
                        if len(galactic) == 6:
                            galactic += ' '

                        # Запись полученных данных в таблицу
                        row_writer = [lokal, galactic + '\t', teta, interval]
                        writer.writerow(row_writer)


example.close()
