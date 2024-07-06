import sqlite3
from config import Config

class UserDatabase:
    table_name = 'UserConv'

    def create_table(self):
        with sqlite3.connect(Config.DATABASE_DIR) as cursor:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name}(id INTEGER PRIMARY KEY, userid INTEGER, conversation_id TEXT)
                """
            )

    def add_user(self, userid: int, conversation_id: str):
        print('[DB] Adding new user')
        with sqlite3.connect(Config.DATABASE_DIR) as cursor:
            cursor.execute(
                f"""
                INSERT INTO {self.table_name} (userid, conversation_id) VALUES (?, ?);
                """,
                (userid, conversation_id)
            )
            print('[DB] User added')

    def get_conv(self, userid: int):
        print('[DB] Pulling user')
        with sqlite3.connect(Config.DATABASE_DIR) as cursor:
            result = cursor.execute(
                f"""
                SELECT * FROM {self.table_name} WHERE userid="{userid}";
                """
            ).fetchone()

        print(f"[DB] User pulled: {result}")
        return result

    def delete_cond(self, userid: int):
        print('[DB] Deleting User')
        with sqlite3.connect(Config.DATABASE_DIR) as cursor:
            result = cursor.execute(
                f"""
                DELETE FROM {self.table_name} WHERE userid="{userid}";
                """
            )

        print(f"[DB] User deleted")