import aiohttp
from .urls import LINK_RANDOM, LINK_ADD, LINK_ALL_WORDS


async def get_random():
    async with aiohttp.ClientSession() as session:
        async with session.get(LINK_RANDOM) as response:
            return await response.json()
        

async def get_all():
    async with aiohttp.ClientSession() as session:
        async with session.get(LINK_ALL_WORDS) as response:
            return await response.json()


async def add_word_to_db(data):
    async with aiohttp.ClientSession() as session:
        word, pinyin, translation = str.split(data, sep=" ")
        d = {'word': word, 'pinyin': pinyin, 'translation': translation}
        await session.post(LINK_ADD, data=d)