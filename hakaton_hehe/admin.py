import sqlite3
from tabulate import tabulate
from keyboard import admin_kb

def role_admin(dispetcher, bot):
    try:
        while True:
            choice = int(input("""
            Здравствуйте!\n Что вы хотите сделать?
-1 Посмотреть наполнение таблиц
-2 Создать пользователя
-3 Изменить данные пользователя
-4 Удалить пользователя"""))
            with sqlite3.connect("database/hton.db") as conn:
                cur = conn.cursor()
                if choice == 1:
                    cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
                    tables = cur.fetchall()
                    print("Запрос принят ...")
                    for table in tables:
                        table_name = ''.join(map(str, table)) # - выводим из массива в кортеж, а из кортежа в строку
                        cur.execute(f"PRAGMA table_info({table_name});") # - содержимое столбцов
                        columns = cur.fetchall()
                        column_names = [column[1] for column in columns] # - выводит название столбцов
                        if table_name != 'sqlite_sequence':
                            print(f"{table_name}: ({', '.join(column_names)})\n")
                    select = str(input("Введите название таблицы, которую хотите посмотреть:\n"))
                    if select == 'sqlite_sequence':
                        print("Таблица не существует!")
                    else:
                        cur.execute(f'SELECT * FROM {select}')

                        column_names = [description[0] for description in cur.description]
                        print(tabulate(cur.fetchall(), headers=column_names, tablefmt="github"))
                        
                elif choice == 2:
                    try:
                        with sqlite3.connect('haton.db') as con:
                                cur = con.cursor()
                                new_id = str(input("Введите id нового пользователя "))
                                new_fio = str(input("Введите ФИО нового пользователя "))
                                new_tgid = str(input("Введите tg никнейм нового пользователя "))
                                new_phone = int(input("Введите номар нового пользователя "))
                                new_role = str(input("Введите роль нового пользователя "))
                                
                                cur.execute(f"""INSERT INTO user(id, fio, tgid, phone_number, role)
                                VALUES ({new_id}, '{new_fio}', '{new_tgid}', {new_phone}, {new_role});""")
                    except:
                        print("Ошибка ввода")
                
                elif choice == 3:
                    try:
                        with sqlite3.connect('haton.db') as con:
                            cur = conn.cursor()
                            name_table = str(input("Напишите название таблицы в которой хотите изменить запись "))
                            cur = con.cursor()
                            current_zapis_name = str(input("Напишите текущее название стобца='новое значение'(оборачивай в ковычки если это текст), которое должно в нём быть\n"))
                            new_zapis_name = str(input("Напишите условие. Например нужно изменить имя Влад на имя Данил, введите: 'Влад', если хотите изменить цифру то пишите БЕЗ КОВЫЧЕК\n"))
                            
                            cur.execute(f"""UPDATE {name_table} SET {current_zapis_name} WHERE {new_zapis_name}""")
                    except:
                        print("Ошибка ввода")
                        
                elif choice == 4:
                    try:
                        with sqlite3.connect('haton.db'):
                            cur = conn.cursor()
                            name_table = str(input("Напишите название таблицы в которой хотите удалить запись "))
                            current_zapis_name = str(input("Напишите условие. Например нужно удалить Влада, введите: 'Влад'\n"))
                            
                            cur.execute(f"""DELETE FROM {name_table} WHERE {current_zapis_name}""")
                    except:
                        print("Ошибка ввода")
    except:
        print("Ошибка ввода")
        