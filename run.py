import os
import sys
import time
import shutil
import config
import telebot
import datetime
import subprocess

# Мои библы
from config import bot



def logger(text):
    curr_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print('{} | {}\n'.format(text, curr_time))

def remove_folder(path, here):
    folder = os.path.join(here, "etc\\libs")
    errors = os.path.join(here, "etc\\libs\\errors")

    for root, dirs, files in os.walk(path):
        if root != errors and root != folder and not "errors" in root:
            try:
                shutil.rmtree(root) 
            except:
                ln = len(os.listdir(errors)) #Сколько в папке ошибок
                os.rename(root, os.path.join(errors, str(ln)))


def install_my_libs(*args):
    here = os.path.abspath(os.path.dirname(__file__)) 
    path_2_libs = os.path.join(here, "etc\\libs")

    for lib in args:
        path_2_lib = os.path.join(path_2_libs, lib)
        if os.path.isdir(path_2_libs) and os.path.exists(path_2_lib):
            os.chdir(path_2_lib) # Перемещение в другую директорию

            command = ["python", "setup.py", "install"]
            a = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                                    stderr=subprocess.STDOUT)
            a.stdout.read().decode("cp866")

            os.chdir(here) # Возрат обратно
            remove_folder(path_2_lib, here) #Удаление её из папки



# def check_before_run():
#     # Check version
#     if sys.version_info < (3, 6):
#         log('[Error] Your Python version: {}, need 3.6 or later'.format(sys.version_info))
#         quit(1)

#     # Check and install modules
#     ret = subprocess.call([sys.executable, 'pip', 'install', '-r', 'requirements.txt', '--quiet'])
#     if ret != 0:
#         quit(2)



def run_bot_loop():
    command = ["python", "main.py"]
    resp = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                                    stderr=subprocess.STDOUT)
            
    resp = resp.stdout.read().decode("cp866")
    return resp





if __name__ == "__main__":
    install_my_libs("myqiwi")
    logger("Начало работы")
    while True:
        error = run_bot_loop()
        logger("Перезапуск") 

        with open("etc\\data\\error.txt", "w", encoding="utf-8") as f: f.write(error)
        doc = open("etc\\data\\error.txt", "rb")
        bot.send_document(config.ADMINS_ID[0], doc)
        doc.close()


        doc = open(config.PATH_2_LOG, "rb")
        bot.send_document(config.ADMINS_ID[0], doc)
        doc.close()
        time.sleep(0)



