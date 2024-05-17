from telethon import TelegramClient, events
from telethon.sessions import StringSession

from hsc_gov_subscriber.services.practice.practice_subscriber import PracticeSubscriber
from hsc_gov_subscriber.utils.config import Config

client = TelegramClient(session=StringSession(), api_id=Config.API_ID.value, api_hash=Config.API_HASH.value)


@client.on(events.NewMessage(chats=6974528785, pattern="\d+\.\d+\.\d+ - \d+ 🎫 талон"))
async def my_event_handler(event):
    await PracticeSubscriber().subscribe(event.message.text)


client.start()
client.run_until_disconnected()
