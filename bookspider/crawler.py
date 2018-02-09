# ** coding: utf-8**
import re
import sys
import requests
import time
import urllib
from bs4 import BeautifulSoup
from db.client import BaseDatabaseClient
import random
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


class Crawler:
    """爬去起点中文网书籍"""

    _base_url = 'https://m.qidian.com'

    def __init__(self, url):
        self.url = url

        self.book_name = ''
        self.author = ''
        self.word_number = 0
        self.update_state = 0
        self.book_describe = ''
        self.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.book_type = random.randint(0, 10)
        self.book_rank = 0
        self.cover_path = ''

        self.book_chapters = []

        self._get_book_info()

    # 爬取书籍详情
    def _get_book_info(self):
        html = requests.get(self.url, verify=True).content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        if u"出错了_起点中文网" != soup.find('title').text:

            # 书名
            self.book_name = soup.find('h2', class_='book-title').text

            # 作者名
            self.author = soup.find(role='option').contents[1]

            word_number, update_state = str(soup.find_all('p', class_='book-meta')[1].text).split('|')

            # 书籍字数
            # self.word_number = int(float(re.match(r"[0-9]+.[0-9]+", word_number).group(0)) * 10000)

            # 书籍更新状态
            if u'连载' == update_state:
                self.update_state = 0
            else:
                self.update_state = 1

            # 书籍简介
            self.book_describe = soup.find('content').text

            # 更新时间
            update_time = str(soup.find('p', id='ariaMuLu').text)
            try:
                self.update_time = re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", update_time).group(0)
            except AttributeError:
                pass

            # 书籍评分
            try:
                self.book_rank = float(soup.find('span', 'star-score').text)
            except AttributeError:
                pass

            # 书籍封面
            self.cover_path = '{0}.jpeg'.format(1)
            img_url = 'https:' + str(soup.find('img', class_="book-cover")['src'])
            urllib.urlretrieve(img_url, self.cover_path)

            print()

            # 获取章节内容
            # catalog_url = self.url + "/catalog"
            # self._get_book_catalog(catalog_url)

    # 爬取章节目录
    def _get_book_catalog(self, catalog_url):
        # 章节数
        chapter_id = 0

        request = requests.get(catalog_url, verify=True)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

        chapters = soup.find_all('a', class_='chapter-li-a ')

        for chapter in chapters:
            # 章节名
            chapter_name = re.findall("第(?:[0-9]+|[\u4E00-\u9FA5]+)章 ([\u4E00-\u9FA5]+)", chapter.text)
            # 章节链接
            chapter_url = self._base_url + chapter['href']

            if len(chapter_name):

                chapter_id += 1
                chapter_name = chapter_name[0]
                chapter_content = self._get_book_content(chapter_url)

                print('获取第{0}章 {1}'.format(chapter_id, chapter_name))

                self.word_number += len(chapter_content)

                book_chapter = dict()
                book_chapter['chapter_id'] = chapter_id
                book_chapter['chapter_name'] = chapter_name
                book_chapter['chapter_content'] = chapter_content
                book_chapter['word_number'] = len(chapter_content)
                self.book_chapters.append(book_chapter)

        print(u"爬取完毕")

    # 爬取章节目录内容
    @ staticmethod
    def _get_book_content(chapter_url):

        content = []

        request = requests.get(chapter_url, verify=True)
        html = request.content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

        paragraphs = soup.find('section', class_='read-section jsChapterWrapper')

        for paragraph in paragraphs.stripped_strings:
            content.append("  " + paragraph)

        chapter_content = '\n'.join(content[1:])

        return chapter_content


class InsetData:

    insert_book_profile_sql = ''
    insert_book_chapter_sql = ''

    def __init__(self):

        self.author = '匿名'
        self.book_name = '天龙八部'
        self.cover = '1.jpeg'
        self.book_describe = ''
        self.book_type = 0
        self.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.db = None
        self.cursor = None

    @ staticmethod
    def make_insert_book_info_sql(args):

        insert_book_info_sql = '''
                                INSERT INTO book (author, book_name, cover, book_describe, book_type, update_time) 
                                VALUES (%s, %s, %s, %s, %s, %s)
                               '''
        client = BaseDatabaseClient()
        with client:
            client.execute(insert_book_info_sql, args)

    @ staticmethod
    def add_item(author, book_name, cover, book_describe, book_type, update_time):
        args = (author, book_name, cover, book_describe, book_type, update_time, )
        return args


if __name__ == '__main__':

    start_time = datetime.datetime.now()

    url = 'https://m.qidian.com/book/3602691'
    book = Crawler(url)
    print(book.book_chapters)

    end_time = datetime.datetime.now()
    print('共花费{0}s'.format((end_time - start_time).seconds))

    # start_time = datetime.datetime.now()
    #
    # insert = InsetData()
    # items = []
    # for i in range(1000):
    #     item = insert.add_item("马承成", "孙子兵法", "1.png", "好", 0, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     items.append(item)
    #
    # insert.make_insert_book_info_sql(items)
    #
    # end_time = datetime.datetime.now()
    # print('共花费{0}s'.format((end_time - start_time).seconds))
