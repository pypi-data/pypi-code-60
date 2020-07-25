import aiohttp
import asyncio
from aio_osservaprezzi.api import API

loop = asyncio.get_event_loop()

SAMPLE = {"town": "Santa Maria Imbaro", "region": "Abruzzo", "province": "CH"}


async def test():
    async with aiohttp.ClientSession() as session:
        api = API(loop, session, data=SAMPLE,)
        data = await api.get_data()
        for s in data:
            print(s["name"])
            print(s["id"])
            print(s["dIns"])
            for c in s["carburanti"]:
                print(c)


loop.run_until_complete(test())
loop.close()
