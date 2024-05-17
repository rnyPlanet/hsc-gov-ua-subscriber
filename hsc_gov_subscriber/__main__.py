from telethon import TelegramClient
from telethon import events
from telethon.sessions import StringSession

from hsc_gov_subscriber.services.practice.practice_subscriber import PracticeSubscriber
from hsc_gov_subscriber.services.re_registration.re_registration_subscriber import ReRegistrationSubscriber
from hsc_gov_subscriber.utils.config import ConfigValidation, Config


@events.register(events.NewMessage(chats=6974528785,
                                   pattern="💼 На послугу: 🚗 Практичний іспит \(транспортний засіб навчального закладу\)"))
async def practice_new_talon_handler(event):
    await PracticeSubscriber().subscribe(event.message.text)


@events.register(events.NewMessage(chats=6974528785,
                                   pattern="💼 На послугу: Реєстраційні дії з транспортними засобами"))
async def re_registration_new_talon_handler(event):
    await ReRegistrationSubscriber().subscribe(event.message.text)


if __name__ == '__main__':
    ConfigValidation.validate()

    with TelegramClient(session=StringSession(), api_id=Config.API_ID.value, api_hash=Config.API_HASH.value) as client:
        client.add_event_handler(practice_new_talon_handler)
        client.add_event_handler(re_registration_new_talon_handler)
        client.run_until_disconnected()
