import redis

settings_dict = {
    'HOST': '127.0.0.1',
    'PORT': '6379',
    'DB': '0'
}


def redis_client():
    pool = redis.ConnectionPool(host=settings_dict['HOST'], port=settings_dict['PORT'], db=settings_dict['DB'])
    return redis.Redis(connection_pool=pool)

# redis_client().set("book_num", 9)
