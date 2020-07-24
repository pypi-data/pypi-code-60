import urllib.parse

import asyncio
import aiohttp
import time

from tqdm import tqdm

import fast_bitrix24.correct_asyncio

##########################################
#
#   SemaphoreWrapper class
#
##########################################


class SemaphoreWrapper():

    def __init__(self, custom_pool_size, cautious):
        if cautious:
            self._stopped_time = time.monotonic()
            self._stopped_value = 0
        else:
            self._stopped_time = None
            self._stopped_value = None
        self._REQUESTS_PER_SECOND = 2
        self._pool_size = custom_pool_size


    async def __aenter__(self):
        self._sem = asyncio.BoundedSemaphore(self._pool_size)
        if self._stopped_time:
            '''
-----v-----------------------------v---------------------
     ^ - _stopped_time             ^ - current time
     |-------- time_passed --------|
     |- step -|- step -|- step |          - add_steps (whole steps to add)
                               |---|      - unused step fraction
                               |- step -| - additional 1 step added
                                   |-aw-| - additional waiting time
            '''
            time_passed = time.monotonic() - self._stopped_time
            
            # сколько шагов должно было пройти
            add_steps = time_passed / self._REQUESTS_PER_SECOND // 1
            
            # сколько шагов могло пройти с учетом ограничений + еще один
            real_add_steps = min(self._pool_size - self._stopped_value, 
                 add_steps + 1)

            # добавляем пропущенные шаги
            self._sem._value += real_add_steps
                      
            # ждем время, излишне списанное при добавлении дополнительного шага
            await asyncio.sleep((add_steps + 1) / self._REQUESTS_PER_SECOND - time_passed)
            self._stopped_time = None
            self._stopped_value = None
        self.release_task = asyncio.create_task(self._release_sem())


    async def __aexit__(self, a1, a2, a3):
        self._stopped_time = time.monotonic()
        self._stopped_value = self._sem._value
        self.release_task.cancel()


    async def _release_sem(self):
        while True:
            if self._sem._value < self._sem._bound_value:
                self._sem.release()
            await asyncio.sleep(1 / self._REQUESTS_PER_SECOND)


    async def acquire(self):
        return await self._sem.acquire()


##########################################
#
#   Bitrix class
#
##########################################


class Bitrix:
    def __init__(self, webhook, custom_pool_size = 50, cautious=False):
        self.webhook = webhook
        self._sw = SemaphoreWrapper(custom_pool_size, cautious)

##########################################
#
#   get_list() group of methods
#
##########################################

    async def _get_paginated_list(self, method, payload_details=None, custom_start=0):
        async with self._sw, aiohttp.ClientSession(raise_for_status=True) as session:
            results, total = await self._get_list_starting(session, custom_start, method, payload_details)
            tasks = []
            if not total or total <= 50:
                return results
            with tqdm(total=total, initial=custom_start + len(results)) as pbar:
                for start in range(custom_start + len(results), total, 50):
                    tasks.append(asyncio.create_task(self._get_list_starting(
                        session, start, method, payload_details, pbar)))
                for x in asyncio.as_completed((*tasks, self._sw.release_task)):
                    r = await x
                    results.extend(r[0])
                    if len(results) >= total: break
            results = [dict(t) for t in {tuple(d.items()) for d in results}] 
            if len(results) == total: 
                return results
#            else:
#                raise RuntimeWarning (
#                    f'Got {len(results)} entries, while expecting {total}')
        

    async def _get_list_starting(self, session, start, method, payload_details=None, pbar=None):
        url = self.webhook + method

        # log (f'Downloading list "{method}": {start}')
        payload = [('start', start)] + \
            (payload_details if payload_details else [])

        await self._sw.acquire()
        async with session.get(url, params=payload) as response:
            r = await response.json(encoding='utf-8')
        if pbar:
            pbar.update(len(r['result']))
        return r['result'], (r['total'] if 'total' in r.keys() else None)


    def get_list(self, method, payload_details=None):
        return asyncio.run(self._get_paginated_list(method, payload_details))


##########################################
#
#   get_items_by_ID_list() group of methods
#
##########################################


    async def _get_item_by_ID (self, method, payload_details, ID, session):
        url = self.webhook + method
        payload = [('ID', ID)] + \
            (payload_details if payload_details else [])
        await self._sw.acquire()
        async with session.get(url, params=payload) as response:
            r = await response.json() 
        return r['result']

    async def _get_items_by_ID_list (self, method, ID_list, payload_details):
        async with self._sw, aiohttp.ClientSession(raise_for_status=True) as session:
            tasks = [asyncio.create_task(self._get_item_by_ID(method, payload_details, ID, session)) for ID in ID_list]
            if len(ID_list) == 1:
                r = await tasks[0]
                return [r]
            results = []
            with tqdm(total=len(ID_list)) as pbar:
                for x in asyncio.as_completed((*tasks, self._sw.release_task)):
                    results.append(await x)
                    pbar.update()
                    if len(results) == len(ID_list): break
        return results

    def get_items_by_ID_list(self, method, ID_list, payload_details = None):
        return asyncio.run(self._get_items_by_ID_list(method, ID_list, payload_details))


##########################################
#
#   post_list() group of methods
#
##########################################


    async def _post_item (self, method, item, session):
        url = f'{self.webhook}{method}?{http_build_query(item)}'
        await self._sw.acquire()
        async with session.post(url) as response:
            r = await response.json() 
        return r['result']


    async def _post_list (self, method, item_list):
        async with self._sw, aiohttp.ClientSession(raise_for_status=True) as session:
            tasks = [asyncio.create_task(self._post_item(method, i, session)) for i in item_list]
            if len(item_list) == 1:
                r = await tasks[0]
                return [r]
            results = []
            with tqdm(total=len(item_list)) as pbar:
                for x in asyncio.as_completed((*tasks, self._sw.release_task)):
                    results.append(await x)
                    pbar.update()
                    if len(results) == len(item_list): break
        return results


    def post_list(self, method, item_list):
        return asyncio.run(self._post_list(method, item_list))


##########################################
#
#   internal functions
#
##########################################


def http_build_query(data):
    parents = list()
    pairs = dict()

    def renderKey(parents):
        depth, outStr = 0, ''
        for x in parents:
            s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
            outStr += s % str(x)
            depth += 1
        return outStr

    def r_urlencode(data):
        if isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                parents.append(i)
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs[renderKey(parents)] = str(data)

        return pairs
    return urllib.parse.urlencode(r_urlencode(data))
