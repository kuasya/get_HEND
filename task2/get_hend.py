import sys
import os
import requests
import logging
import get_delta_time

from hend2thr import parse_hend_text

import config as settings
config = settings.read_config('config.yaml')

login = config['hend_web_tool']['user']
passw = config['hend_web_tool']['pass']


def sod_to_hhmmss(seconds, use_codes=False):
    hours = int(seconds / 3600)
    seconds -= 3600.0 * hours
    minutes = int(seconds / 60.0)
    seconds -= int(60.0 * minutes)
    if use_codes:
        return "{:02d}%3A{:02d}%3A{:02.0f}".format(hours, minutes, seconds)
    else:
        return "{:02d}:{:02d}:{:02.0f}".format(hours, minutes, seconds)


def download_hend(str_time):
    
    #print str_time

    # make a request
    try:
        response = requests.get(url='https://zea.lpl.arizona.edu/hendburst/query?utc={:s}'.format(str_time), auth=(login, passw), verify=False)
        print ("Response status: ", response.status_code)

        response.raise_for_status()
        return response.text

    except Exception as e:
        logging.info("Excepton in download_hend: " + str(e))
        #logging.info("Details: " + response.text)
        return None


def main():

    date = data
    # date = '2021-07-11'
    # time =  58017.942 # SOD

    str_time = "{:s}T{:s}".format(date, sod_to_hhmmss(time, use_codes=True))
    print ("{:s}T{:s}".format(date, sod_to_hhmmss(time)))

    str_hend_data = download_hend(str_time)

    if str_hend_data:
        parse_hend_text(str_hend_data, './')
    else:
        print("Request has returned no data")


data = ''
time = 0


def get_data(a):
    # функция определения даты и времени

    global list_files
    with open('HEND_correct/' + list_files[a]) as f:
        global data, time
        line = f.readline().split()
        data = line[3]
        # прибавляем 1350 сек и отклонение во времени delta_time данного файла
        time = float(line[4]) + 1350 + get_delta_time.delta_times_list[a]
        # print(neew.delta_times_list[a], float(line[4]) + 1350)

        # Изменяем формат даты
        data = data.strip("'")
        data = data.split('/')
        data = '20'+data[2]+'-'+data[1]+'-'+data[0]

        # Учитываем, что время может превысить суточное количество секунд
        if time >= 86400:
            # Изменяем дату +1 день
            if data[-1] != '9':
                data = data[:-1] + str(int(data[-1])+1)
            else:
                data = data[:-2] + str(int(data[-2]) + 1) + '0'
            time -= 86400  # обновляем время
        time = round(time, 3)


list_files = os.listdir('HEND_correct')  # список файлов в папке
# print(list_files)

for n in range(len(list_files)):
    file_name = n  # номер файла из списка
    get_data(file_name)  # определяем дату и время

    if __name__ == "__main__":
        main()

    print()
