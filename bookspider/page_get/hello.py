import time
import asyncio
import aiohttp
import threading


def now():
    return time.time()

a = 0

async def get_page(url, i):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=100) as resp:
            global a
            a += 1
            print(resp.status, a)


async def do_some_work(url, i):
    await get_page(url, i)

start = now()

# coroutine = do_some_work('https://m.qidian.com/book/1010957891')
# coroutine2 = do_some_work('https://m.qidian.com/book/1011096075')
# coroutine3 = do_some_work('https://m.qidian.com/book/1010191960')
# coroutine4 = do_some_work('https://m.qidian.com/book/1010957891')
# coroutine5 = do_some_work('https://m.qidian.com/book/1011096075')
# coroutine6 = do_some_work('https://m.qidian.com/book/1010191960')
# coroutine7 = do_some_work('https://m.qidian.com/book/1010957891')
# coroutine8 = do_some_work('https://m.qidian.com/book/1011096075')
# coroutine9 = do_some_work('https://m.qidian.com/book/1010191960')


# tasks = [
#     asyncio.ensure_future(coroutine1),
#     asyncio.ensure_future(coroutine2),
#     asyncio.ensure_future(coroutine3),
#     asyncio.ensure_future(coroutine4),
#     asyncio.ensure_future(coroutine5),
#     asyncio.ensure_future(coroutine6),
#     asyncio.ensure_future(coroutine7),
#     asyncio.ensure_future(coroutine8),
#     asyncio.ensure_future(coroutine9),
# ]


loop = asyncio.get_event_loop()

tasks = []

for i in range():
    tasks.append(asyncio.ensure_future(do_some_work('https://m.qidian.com/book/1010957891', i+1)))


loop.run_until_complete(asyncio.wait(tasks))

# for task in tasks:
#     print(task.result())

print('Time:', now()-start)
