# ** coding: utf-8**
import pymysql


class DatabaseClient:

    settings_dict = {
        'HOST': '120.77.38.20',
        'NAME': 'root',
        'PASSWORD': 'Mcc616254086',
        'DB_NAME': 'Reading',
    }

    def __init__(self):
        self.db = None
        self.cursor = None

    def __enter__(self):
        if self.db is None:
            self.db = pymysql.connect(host=self.settings_dict['HOST'], user=self.settings_dict['NAME'],
                                      password=self.settings_dict['PASSWORD'], db=self.settings_dict['DB_NAME'],
                                      use_unicode=True, charset="utf8")
            self.cursor = self.db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db is not None:
            self.db = None
            self.cursor = None

    def execute(self, sql, args):
        try:
            self.cursor.executemany(sql, args)
            self.db.commit()
        except self.db.DatabaseError:
            self.db.rollback()
        finally:
            self.db.close()
