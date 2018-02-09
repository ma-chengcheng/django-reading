import random

first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)


class FakeChromeUA:

    """伪造chrome User-Agent"""

    os_type = [
                '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
                '(Macintosh; Intel Mac OS X 10_12_6)'
               ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )

headers = {
    'Connection': 'keep-alive',
    'User-Agent': FakeChromeUA.get_ua(),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
