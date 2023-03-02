# get_HEND
Обработка астрономических данных

-- task1 -- определение расстояния между гамма-всплесками

-- task1 -- поиск информации по гамма-всплескам

-- task2 -- расчет отклонения во времени --

## расстояние между гамма-всплесками

Входные данные: 
- таблица гамма-всплесков с известными локализациями (Edinaya_tablitsa_lokalizatsiy.txt)
- каталог близких галактик (Katalog_galaktik.txt)

-- count_teta.py --
Данный скрипт выбирает из таблицы небесные координаты центров локализаций гамма-всплесков и центров галактик, а также радиусы колец локализаций и их погрешности. Затем скрипт находит расстояние между каждым гамма-всплеском и каждой галактикой по следующей формуле:

![image](https://user-images.githubusercontent.com/62285192/222462790-a711de48-2106-4799-a4e9-05626c6386c2.png)


Где  ![image](https://user-images.githubusercontent.com/62285192/222459620-42c486e9-6ee5-40eb-8a2a-9b7d641024f1.png)
 – прямое восхождение центра локализации гамма-всплеска,
        ![image](https://user-images.githubusercontent.com/62285192/222459645-9bcb99db-b5c3-4b95-a31a-b71804d53d4c.png)
  – склонение центра локализации гамма-всплеска,
       ![image](https://user-images.githubusercontent.com/62285192/222459677-27d25377-73cf-4bfa-ab4d-67db0b0b274c.png)
   – склонение центра локализации галактики,
      ![image](https://user-images.githubusercontent.com/62285192/222459709-b3929335-dff9-43d9-8a52-bb183fd2a2fa.png)
    – склонение центра локализации галактики.
Также, поскольку необходимо найти гамма-всплески, вспыхивавшие непосредственно внутри галактик, скрипт задает ограничение на  ![image](https://user-images.githubusercontent.com/62285192/222460022-414782d8-6873-40d1-a3a9-df886cd82040.png)
 в виде:

![image](https://user-images.githubusercontent.com/62285192/222462986-3d15b4c7-b1ce-4afd-92b4-c8b70acf6424.png)
                      

Где  R – радиус кольца локализации гамма-всплеска,
     ![image](https://user-images.githubusercontent.com/62285192/222459441-791d4828-addc-4ff9-8800-fbe195a0f129.png)
– погрешность этого радиуса.
После чего скрипт формирует и сохраняет таблицу с результатами своей работы.

В качестве результата было получено 6 всплесков-кандидатов в гигантские внегалактические вспышки магнетаров.

## поиск информации по гамма-всплескам
-- get_info.py -- парсер

Необходимо пройти по списку ссылок (links.txt) и выделить нужную информацию в таблицу (Burst info).

Пример входных данных:
https://gcn.gsfc.nasa.gov/gcn3/21247.gcn3

https://gcn.gsfc.nasa.gov/gcn3/21630.gcn3


Пример работы парсера:
Из следующей строчки в файле:
The burst light curve starts with a short (~1.5 s) pulse,
followed by a weaker pulse at ~T0+55 s (with a duration of ~6 s).
Надо получить в таблицу: +55. 
Аналогично из строки: ~T0(BAT)+478.8 s, надо выделить: (BAT)+478.8 и т.д. 
(пример, как надо — во вложении) 

## расчет отклонения во времени

-- get_hend.py --

- Сравнение файлов из HEND_correct и HEND_incorrect
- Определение разности во времени  между двумя последовательностями
