ЛАБОРАТОРНАЯ РАБОТА №1

Студент:    Нгуен Дык Ханг
Группа:     N41601
Вариант:    5141

Процесс запуска проекта:
1. Скачать все файлы в КП в отдельную папку
2. Открыть папку, запускать файл сервера tppo_serer_5141.py
   При запуске сервера, использовать командую строку: python tppo_server_5141.py <IP_Address> <PORT>
   Например: python tppo_server_5141.py 127.0.0.1 55555
3. Запускать один или несколько файлов tppo_client_5142.py: python tppo_client_5141.py
   После запуска файл слиента tppo_client_5141.py программа требует по очереди ввести ID_Address и PORT сервера.
4. Ввести команды для устоновки или получения параметров оборудования

Команды поддержки:
1. set <value> <value>  - установить проценты сдвига полота и пропуска светового потока.
2. setcanvas <value>    - установить процент сдвига полота
3. setlight <value>     - установать процент пропуска светового потока
4. get                  - получить значения процентов сдвига полота, пропуска светового потока и текущей освещенности с внешней стороны.
5. !DISCONNECT          - отключить соединение к серверу

Где - значение <value> находится в диапозоне [0 - 100]