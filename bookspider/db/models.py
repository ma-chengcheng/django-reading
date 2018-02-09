# **coding: utf-8**
from bookspider.db.client import DatabaseClient


class BasicModel(object):

    """模型基类"""

    # 表名
    __table__ = ''

    # 字段列表
    _fields = []
    _values = []

    def __init__(self, *args):

        self._values = []

        if self.__table__ != 'book_chapter':

            if len(args) != len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))

            for name, value in zip(self._fields, args):
                setattr(self, name, value)

            self._values.append(list(args))

        else:
            self._values = args[0]

    def save(self):

        col_names = ', '.join(self._fields)
        col_values = ', '.join(['%s' for i in range(len(self._fields))])

        sql = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(self.__table__, col_names, col_values)

        client = DatabaseClient()
        with client:
            client.execute(sql, self._values)


class BookModel(BasicModel):

    """书籍信息"""

    __table__ = 'book'

    _fields = ['author', 'book_name', 'cover', 'book_describe', 'book_type', 'update_time']


class BookProfileModel(BasicModel):

    """书籍额外信息"""

    __table__ = 'book_profile'

    _fields = ['book_id']


class BookChapterModel(BasicModel):

    """书籍章节"""

    __table__ = 'book_chapter'

    _fields = ['book_id', 'chapter_id', 'chapter_name', 'chapter_content', 'update_date', 'word_number']

