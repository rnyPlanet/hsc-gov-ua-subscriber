from telethon import TelegramClient, events

from subscriber.configs import TG_API_ID, TG_API_HASH
from subscriber.services.hsc_gov_subscriber import HscGovSubscriber

client = TelegramClient(session="annon", api_id=TG_API_ID, api_hash=TG_API_HASH)


@client.on(events.NewMessage(chats=6974528785, pattern="\d+\.\d+\.\d+ - \d+ 🎫 талон"))
async def my_event_handler(event):
    await HscGovSubscriber().subscribe(event.message.text)


client.start()
client.run_until_disconnected()
