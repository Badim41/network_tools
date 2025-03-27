import json
import os
import sqlite3
import threading


class DictSQL:
    def __init__(self, name, folder="lock_storage"):
        os.makedirs(folder, exist_ok=True)
        self.db_path = f"{folder}/{name}.db"
        self.lock = threading.RLock()  # Для потокобезопасности
        self._ensure_table_exists()  # Проверяем и создаем таблицу при инициализации

    def _get_conn(self):
        """Создает новое соединение для каждого вызова."""
        return sqlite3.connect(self.db_path)

    def _ensure_table_exists(self):
        """Проверяет существование таблицы и создает ее, если нужно."""
        with self.lock:
            with self._get_conn() as conn:
                conn.execute("""
                        CREATE TABLE IF NOT EXISTS store (
                            key TEXT PRIMARY KEY,
                            value TEXT
                        )
                    """)
                conn.commit()

    def __getitem__(self, key):
        """Получение значения по ключу."""
        with self.lock:
            with self._get_conn() as conn:
                self._ensure_table_exists()
                cur = conn.cursor()
                cur.execute("SELECT value FROM store WHERE key = ?", (key,))
                result = cur.fetchone()
                if result is None:
                    raise KeyError(key)
                return json.loads(result[0])

    def __setitem__(self, key, value):
        """Установка значения по ключу."""
        with self.lock:
            with self._get_conn() as conn:
                self._ensure_table_exists()
                cur = conn.cursor()
                cur.execute("INSERT OR REPLACE INTO store (key, value) VALUES (?, ?)",
                            (key, json.dumps(value)))
                conn.commit()

    def __delitem__(self, key):
        """Удаление ключа."""
        with self.lock:
            with self._get_conn() as conn:
                self._ensure_table_exists()
                cur = conn.cursor()
                cur.execute("DELETE FROM store WHERE key = ?", (key,))
                conn.commit()

    def __contains__(self, key):
        """Проверка наличия ключа."""
        with self.lock:
            with self._get_conn() as conn:
                self._ensure_table_exists()
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM store WHERE key = ?", (key,))
                return cur.fetchone() is not None

    def get(self, key, default=None):
        """Получение значения с дефолтом."""
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        """Возвращает все пары (ключ, значение) из базы данных."""
        with self.lock:
            with self._get_conn() as conn:
                self._ensure_table_exists()
                cur = conn.cursor()
                cur.execute("SELECT key, value FROM store")
                for key, value in cur.fetchall():
                    yield key, json.loads(value)