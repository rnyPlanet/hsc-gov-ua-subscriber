import re

from telethon import TelegramClient
from telethon.tl.types import PeerUser

from subscriber.configs import TG_API_ID, TG_API_HASH

client = TelegramClient(session="annon", api_id=TG_API_ID, api_hash=TG_API_HASH)

times = [
]


async def main():
    bot = await client.get_entity(PeerUser(6974528785))

    pattern = r'Знайдено талони*?'

    async for message in client.iter_messages(bot):
        match = re.search(pattern, message.text)
        if match:
            time_str = message.date.strftime("%Y-%m-%d %H:%M:%S")
            times.append(time_str)

    print(times)


with client:
    client.loop.run_until_complete(main())
