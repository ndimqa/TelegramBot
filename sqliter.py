import sqlite3

class SQLighter:

    def __init__(self, database_file):
        #Подключаемся к БД и сохраняем курсор соединения
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        #Получаем всх активных подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'subscriptions' WHERE 'status' = ?", (status,)).fetchall()
    
    def subscriber_exist(self, user_id):
        #Проверяем подписку 
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'subscriptions' WHERE 'user_id' = ?",(user_id,)).fetchall()
            return bool(len(result))
    
    def add_subscriber(self, user_id, status = True):
        #Добовляем новго подписчика
        with self.connection:
            return self.cursor.execute("INSERT INTO 'subscriptions' ('user_id', 'status') VALUES (?, ?)",(user_id,status))
    
    def update_subscription(self, user_id, status):
        # Обновляем статус подписчика
        return self.cursor.execute("UPDATE 'subscriptions' SET 'status' = ? WHERE 'user_id' = ?",(status,user_id))
    
    def close(self):
        #Закрываем соединение с БД
        self.connection.close()