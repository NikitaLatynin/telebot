import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable
import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]
#
    def add_user(self, user_id, name, tg_nick, inst_nick):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`, `name`, `tg_nick`, `inst_nick`) VALUES (?, ?, ?, ?)", (user_id, name, tg_nick, inst_nick))
        return self.conn.commit()
    
    def get_all_users(self):
        self.cursor.execute("SELECT `user_id` FROM users")
        users = self.cursor.fetchall()
        return users
        # for user in users:
        #     try:
        #         bot.send_message(user[0], message_text)
        #     except:
        #         pass


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
