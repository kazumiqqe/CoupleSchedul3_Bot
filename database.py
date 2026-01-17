import sqlite3
import json
from typing import Optional, Dict, List


class Database:
    def __init__(self, db_file: str):
        """Инициализация подключения к базе данных"""
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        """Создание таблиц при первом запуске"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                schedule TEXT
            )
        """
        )
        self.connection.commit()

    def save_schedule(self, user_id: int, username: str, schedule: Dict):
        """Сохранение расписания пользователя"""
        schedule_json = json.dumps(schedule, ensure_ascii=False)

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO users (user_id, username, schedule)
            VALUES (?, ?, ?)
        """,
            (user_id, username, schedule_json),
        )
        self.connection.commit()

    def get_schedule(self, user_id: int) -> Optional[Dict]:
        """Получение расписания пользователя"""
        self.cursor.execute(
            """
            SELECT schedule FROM users WHERE user_id = ?
        """,
            (user_id,),
        )

        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        return None

    def delete_schedule(self, user_id: int):
        """Удаление расписания пользователя"""
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.connection.commit()
