# get_HEND
Обработка астрономических данных

## Гамма-всплесков
папка task1 
Входные данные: 
- таблица гамма-всплесков с известными локализациями 
- каталог близких галактик

Данный скрипт выбирает из таблицы небесные координаты центров локализаций гамма-всплесков и центров галактик, а также радиусы колец локализаций и их погрешности. Затем скрипт находит расстояние между каждым гамма-всплеском и каждой галактикой по следующей формуле:

 ![image](https://user-images.githubusercontent.com/62285192/222459567-5d7a0d8b-2534-4c17-aa38-483ffc765931.png)


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

                       ![image](https://user-images.githubusercontent.com/62285192/222459216-0a471424-fcc2-4522-8b27-616fd39d8a29.png)
                      

Где  R – радиус кольца локализации гамма-всплеска,
     ![image](https://user-images.githubusercontent.com/62285192/222459441-791d4828-addc-4ff9-8800-fbe195a0f129.png)
– погрешность этого радиуса.
После чего скрипт формирует и сохраняет таблицу с результатами своей работы.
В качестве результата было получено 6 всплесков-кандидатов в гигантские внегалактические вспышки магнетаров.


## расчет отклонения во времени
папка task2
-- Сравнение файлов из HEND_correct и HEND_incorrect
-- Определение разности во времени  между двумя последовательностями
