Мануал Windows/Windows server

1. Скачиваем python на дедик с оф.сайта: https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe
2. Устанавливаем его, обязательно поставив галку в графе "Add Python to PATH"
3. Распаковываем архив со скриптом в любое удобное место на диске.
4. Нажимаем Win+R и в пишем cmd в открывшемся поле ввода
5. Далее в командной строке поочередно пишем команды:
pip install requests
pip install coinbase
pip install pytelegrambotapi
pip install telebot
6. Далее переходим в папку распакованного из архива скрипта, указав путь к ней:
cd С:/путь/до/бота
7. Запускаем бота:
py run.py
8. Пиарим свой обменник)

P.S. Пункт 7 выполняем после заполнения данных в файле config.py в корневой папке распакованного скрипта  