import re

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerUser

from hsc_gov_subscriber.utils.config import Config

client = TelegramClient(session="annon", api_id=Config.API_ID.value, api_hash=Config.API_HASH.value)

times = [
]


async def main():
    dialogs = await client.get_dialogs()
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
