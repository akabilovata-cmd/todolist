import sqlite3

class Task:
    def __init__(self, description, status):
        self.description = description
        self.status = status

conn = sqlite3.connect('todolist.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, 
               description TEXT NOT NULL, 
               status TEXT)""")

def add_task(conn,cursor):
    description = input('Добавьте задачу: ')
    if not description.strip():
        print('Поле не может быть пустым. ')
        return
    status = ('TODO')
    task = Task(description, status)
    cursor.execute('INSERT INTO tasks (description, status) VALUES (?, ?)', (task.description, task.status))
    conn.commit()

def view_tasks(conn, cursor):
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    if not tasks:
        print('\nСписок задач пуст. ')
        return
    print('\n---Все задачи!---')
    for task in tasks:
        print(f"[{task[0]}] Статус: {task[2]} | Задача: {task[1]}")

def complete_task(conn, cursor):
    # 1. ПОЛУЧАЕМ ВВОД ОТ ПОЛЬЗОВАТЕЛЯ
    task_id_input = input('Введите ID задачи, которую нужно отметить как выполненную: ')
    
    try:
        # Пытаемся преобразовать ввод в число
        task_id = int(task_id_input)
    except ValueError:
        print('Ошибка: ID задачи должен быть числом.')
        return
        
    new_status = 'DONE' # Используем стандартизированный статус
    
    # 2. ИСПРАВЛЕННЫЙ SQL-ЗАПРОС (Убрана COLLATE NOCASE и исправлены кавычки)
    cursor.execute(
        'UPDATE tasks SET status = ? WHERE id = ?', 
        (new_status, task_id)
    )
    
    if cursor.rowcount > 0:
        print(f'Задача с ID {task_id} отмечена как {new_status}!')
    else:
        # Проверка rowcount — отличная практика!
        print(f'Задача с ID {task_id} не найдена.')
        
    conn.commit()

def delete_task(conn, cursor):
    # 1. ПОЛУЧАЕМ ВВОД ОТ ПОЛЬЗОВАТЕЛЯ
    task_id_input = input('Введите ID задачи, которую нужно удалить: ')
    
    try:
        # Пытаемся преобразовать ввод в число
        task_id = int(task_id_input)
    except ValueError:
        print('Ошибка: ID задачи должен быть числом.')
        return
         
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount > 0:
        print(f'Задача с ID {task_id} удалена!')
    else:
        # Проверка rowcount — отличная практика!
        print(f'Задача с ID {task_id} не найдена.')
    conn.commit()

def menu(conn, cursor):
    while True:
        print("\n--- Менеджер Задач ---")
        print("1. Добавить задачу")
        print("2. Посмотреть все задачи")
        print("3. Отметить как выполненную")
        print("4. Удалить задачу")
        print("5. Выйти")

        try:
            choice = int(input('Введите цифру: '))
        
            if choice == 1:
                # ВЫЗОВ ФУНКЦИИ add_task
                add_task(conn, cursor) 
            elif choice == 2:
                # ВЫЗОВ ФУНКЦИИ view_tasks
                view_tasks(conn, cursor)
            elif choice == 3:
                # ВЫЗОВ ФУНКЦИИ complete_task
                complete_task(conn, cursor)
            elif choice == 4:
                # ВЫЗОВ ФУНКЦИИ delete_task
                delete_task(conn, cursor)
            elif choice == 5:
                print("Выход из программы. До свидания!")
                break  # Это останавливает цикл while True
            else:
                print('Неверный выбор. Введите число от 1 до 5.')

        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

if __name__ == '__main__':
    menu(conn, cursor)
    conn.close()
    
print('Изменение в проекте')