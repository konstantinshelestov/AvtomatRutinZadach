import telnetlib
import re
import config
import time

def ont_status(host):
    # Удаляем сервисные порты и онты с порта
    print(f'\n\n\n{"*" * 70}\n\n\n\t\tНачинаем подготовку оптических терминалов\n\n\n{"*" * 70}')
    with telnetlib.Telnet(host, port=23) as tn:
        tn = telnetlib.Telnet(host)
        tn.read_until(b">>User name:")
        tn.write(config.user.encode("utf-8") + b"\n")
        tn.read_until(b">>User password:")
        tn.write(config.password.encode("utf-8") + b"\n")
        tn.write('enable'.encode("utf-8") + b'\n')
        print('\nПроверяем, все ли терминалы обновили прошивку')
        count = 0
        while True:
            tn.write('display ont load state all'.encode("utf-8") + b'\n')
            time.sleep(5)
            flag = True
            result = ''
            while flag:
                output = tn.read_very_eager().decode("utf-8")
                if 'More' in output:
                    output = re.sub(".+More.+", "", output)
                    tn.write(b" ")
                    time.sleep(1)
                else:
                    flag = False
                result = result + output
            result = result.replace('\x1b[37D', '').split('\n')
            for i_elem in result:
                if 'Loading' in i_elem:
                    print('Есть терминалы, которые грузятся, ждём...')
                    time.sleep(60)
                    break
            else:
                break
        print('\nВсе подключенные терминалы прошиты')

def clear_ont(host, port):
    print(f'Удаляем все сервисные порты и прописанные на порту 0/1/{port} терминалы')
    with telnetlib.Telnet(host, port=23) as tn:
        tn = telnetlib.Telnet(host)
        tn.read_until(b">>User name:")
        tn.write(config.user.encode("utf-8") + b"\n")
        tn.read_until(b">>User password:")
        tn.write(config.password.encode("utf-8") + b"\n")
        tn.write('enable'.encode("utf-8") + b'\n')
        tn.write('config'.encode("utf-8") + b'\n')
        tn.write('undo service-port all'.encode("utf-8") + b'\n')
        tn.write('y'.encode("utf-8") + b'\n')
        time.sleep(10)
        tn.write('interface gpon 0/1'.encode("utf-8") + b'\n')
        tn.write(f'ont delete {port} all'.encode("utf-8") + b'\n')
        tn.write('y'.encode("utf-8") + b'\n')
        time.sleep(10)
        tn.write('quit'.encode("utf-8") + b'\n')
        tn.write('quit'.encode("utf-8") + b'\n')
        time.sleep(60)
        print('Выполнено')

def factory_restore(host, port):
    print(f'Сбрасываем на заводские все терминалы на порту 0/1/{port}')
    with telnetlib.Telnet(host, port=23) as tn:
        tn = telnetlib.Telnet(host)
        tn.read_until(b">>User name:")
        tn.write(config.user.encode("utf-8") + b"\n")
        tn.read_until(b">>User password:")
        tn.write(config.password.encode("utf-8") + b"\n")
        tn.write('enable'.encode("utf-8") + b'\n')
        tn.write('config'.encode("utf-8") + b'\n')
        tn.write('interface gpon 0/1'.encode("utf-8") + b'\n')
        tn.write(f'ont factory-setting-restore {port} all'.encode("utf-8") + b'\n')
        tn.write('y'.encode("utf-8") + b'\n')
        time.sleep(120)
        print('Выполнено')

def online_ont(host, port):
    with telnetlib.Telnet(host, port=23) as tn:
        tn = telnetlib.Telnet(host)
        tn.read_until(b">>User name:")
        tn.write(config.user.encode("utf-8") + b"\n")
        tn.read_until(b">>User password:")
        tn.write(config.password.encode("utf-8") + b"\n")
        tn.write('enable'.encode("utf-8") + b'\n')
        print(f'Введена команда display ont info 0 1 {port} all')
        count = 0
        while count < 3:
            tn.write(f'display ont info 0 1 {port} all'.encode("utf-8") + b'\n')
            time.sleep(5)
            flag = True
            result = ''
            while flag:
                output = tn.read_very_eager().decode("utf-8")
                if 'More' in output:
                    output = re.sub(".+More.+", "", output)
                    tn.write(b" ")
                    time.sleep(1)
                else:
                    flag = False
                result = result + output
            result = result.replace('\x1b[37D', '').split('\n')
            for i_elem in result:
                if 'offline' in i_elem:
                    print('Есть терминал offline, ждём...')
                    time.sleep(30)
                    break
            else:
                count = 4
                break
            count += 1
        print('\nПолучаем перечень онтов')
        output = []
        for i_elem in result:
            if 'online' in i_elem and 'active' in i_elem:
                output.append(i_elem.split()[2])
        print('\nСписок онтов', output)
        return output
def show_version(host, port):
    print('\nНачинаем загружать конфиг на терминалы')
    with telnetlib.Telnet(host, port=23) as tn:
        tn = telnetlib.Telnet(host)
        tn.read_until(b">>User name:")
        tn.write(config.user.encode("utf-8") + b"\n")
        tn.read_until(b">>User password:")
        tn.write(config.password.encode("utf-8") + b"\n")
        tn.write('enable'.encode("utf-8") + b'\n')
        tn.write(f'display ont version 0 1 {port} all'.encode("utf-8") + b'\n')
        flag = True
        result = ''
        while flag:
            output = tn.read_very_eager().decode("utf-8")
            if 'More' in output:
                output = re.sub(".+More.+", "", output)
                tn.write(b" ")
                time.sleep(1)
            else:
                flag = False
            result = result + output
        result = result.replace('\x1b[37D', '').split('\n')




def prepare_ont(host, onts, port):
    print('\nНачинаем загружать конфиг на терминалы')
    with telnetlib.Telnet(host, port=23) as tn:
        tn = telnetlib.Telnet(host)
        tn.read_until(b">>User name:")
        tn.write(config.user.encode("utf-8") + b"\n")
        tn.read_until(b">>User password:")
        tn.write(config.password.encode("utf-8") + b"\n")
        tn.write('enable'.encode("utf-8") + b'\n')
        tn.write('diagnose'.encode("utf-8") + b'\n')
        for i_ont in onts:
            print(f'Началась загрузка конфигурации на {i_ont}-й терминал\n')
            # tn.write('ont-load info configuration Prepare_HS8545M5.xml ftp 10.2.1.3 huawei ksa5oz6y'.encode("utf-8") + b'\n')
            tn.write(
                'ont-load info configuration Prepare_all.xml ftp 10.2.1.3 huawei ksa5oz6y'.encode("utf-8") + b'\n')
            time.sleep(0.5)
            tn.write(f'ont-load select 0/1 {port} {i_ont}'.encode("utf-8") + b'\n')
            time.sleep(0.5)
            tn.write('ont-load start'.encode("utf-8") + b'\n')
            tn.write(b'\n')
            time.sleep(30)
            tn.write(f'display ont-load select 0/1 {port} {i_ont}'.encode("utf-8") + b'\n')
            while True:
                output = tn.read_very_eager().decode("utf-8")
                print(output)
                if 'Loading' in output:
                    time.sleep(10)
                else:
                    break
            tn.write('ont-load stop'.encode("utf-8") + b'\n')
            output = tn.read_very_eager().decode("utf-8")
            print(output)
            print('Терминал сконфигурирован\n')
        tn.write('quit'.encode("utf-8") + b'\n')
        print(f'\n\n\n{"*"* 70}\n\n\n\t\tПодготовка терминалов завершена!\n\n\n{"*"* 70}')

host = '172.16.17.232'
try:
    port = int(input('Введите номер порта головной станции '))
    ont_status(host)
    clear_ont(host, port)
    factory_restore(host, port)
    ont_lst = online_ont(host, port)
    prepare_ont(host, ont_lst, port)
except ValueError:
    print('Некорректный ввод')







