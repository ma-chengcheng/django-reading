# ** coding: utf-8 **
import requests
from abc import ABCMeta, abstractmethod
from bookspider.db import redis_db
from bookspider.config.headers import headers
from bs4 import BeautifulSoup


def parse_page(url):
    html = requests.get(url=url, verify=True, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    if u"出错了_起点中文网" != soup.find('title').text:
        return soup
    else:
        raise RuntimeError("Page no found")


class AbstractBookSpider(metaclass=ABCMeta):

    """
    输入书籍id
    """

    # 基本的url
    _base_url = ''

    def __init__(self, bid):
        rc = redis_db.redis_client()
        rc.incr(name="book_num", amount=1)

        self.book_id = int(rc.get(name="book_num"))

        self.bid = str(bid)

    @abstractmethod
    def get_book(self):
        pass

    @abstractmethod
    def get_book_profile(self):
        pass

    @abstractmethod
    def get_book_chapter(self):
        pass


