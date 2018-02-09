# ** coding: utf-8 **
import re
import time
import random
import urllib.request
from bookspider.spider.basic import AbstractBookSpider, parse_page
from bookspider.db.models import BookModel, BookProfileModel, BookChapterModel


class QiDianBookSpider(AbstractBookSpider):

    # 基本的url
    _base_url = 'https://m.qidian.com/book/'

    # 获取书籍信息
    def get_book(self):

        print("获取第{0}本书".format(self.book_id))

        # 解析页面
        book_url = self._base_url + self.bid
        try:
            soup = parse_page(book_url)
        except RuntimeError:
            print(u'页面不存在')
        else:
            # 书名
            book_name = soup.find('h2', class_='book-title').text

            # 作者
            author = soup.find(role='option').contents[1]

            # 书籍简介
            book_describe = soup.find('content').text

            # 书籍封面
            cover = '{0}.jpeg'.format(self.book_id)

            img_url = 'https:' + str(soup.find('img', class_="book-cover")['src'])
            urllib.request.urlretrieve(img_url, cover)

            # 书籍类型
            book_type = random.randint(0, 10)

            # 更新时间
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            return BookModel(author, book_name, cover, book_describe, book_type, update_time)

    def get_book_profile(self):

        # 解析页面详情
        return BookProfileModel(self.book_id)

    def get_book_chapter(self):
        """
        book    chapter_id   chapter_name    chapter_content     update_date
        书籍      章节数         章节名            章节内容             更新日期
        """
        # 书籍id
        book_id = self.book_id

        # 章节数
        chapter_id = 0
        book_chapter = []

        book_catalog_url = self._base_url + self.bid + '/catalog'
        soup = parse_page(book_catalog_url)

        catalog_items = soup.find_all('a', class_='chapter-li-a ')

        for catalog_item in catalog_items:

            # 章节名
            catalog_name = re.sub('[： ]', '', str(catalog_item.text))
            chapter_name = re.findall("第(?:[0-9]+|[\u4E00-\u9FA5]+)章([\u4E00-\u9FA5]+)", catalog_name)

            if len(chapter_name):

                chapter_id += 1

                print("获取第{0}本书的第{1}章".format(book_id, chapter_id))

                # 章节链接
                chapter_url = self._base_url + self.bid + '/' + str(catalog_item['href']).split('/')[-1]

                # 章节内容
                chapter_content = self._get_chapter_content(chapter_url)

                # 字数
                word_number = len(chapter_content)

                # 更新时间
                update_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                book_chapter.append((book_id, chapter_id, chapter_name[0], chapter_content, update_date, word_number))

        return BookChapterModel(book_chapter)

    @ staticmethod
    def _get_chapter_content(chapter_url):
        content = []

        soup = parse_page(chapter_url)

        paragraphs = soup.find('section', class_='read-section jsChapterWrapper')

        for paragraph in paragraphs.stripped_strings:
            content.append("  " + paragraph)

        chapter_content = '\n'.join(content[1:])

        return chapter_content

if __name__ == '__main__':
    book = QiDianBookSpider(1003667321)
    book_info = book.get_book()
    book_info.save()
    book_profile = book.get_book_profile()
    book_profile.save()
    book_chapter = book.get_book_chapter()
    book_chapter.save()
