from telethon import TelegramClient
from telethon import events
from telethon.sessions import StringSession

from hsc_gov_subscriber.services.practice_subscriber import PracticeSubscriber
from hsc_gov_subscriber.services.re_registration_subscriber import ReRegistrationSubscriber
from hsc_gov_subscriber.utils.config import ConfigValidation, Config
from hsc_gov_subscriber.utils.log import logger


@events.register(events.NewMessage(
    chats=6974528785,
    incoming=True,
    func=lambda ev: "💼 На послугу: 🚗 Практичний іспит (транспортний засіб навчального закладу)" in ev.message.message)
)
async def practice_new_talon_handler(event):
    await PracticeSubscriber().subscribe(event.message.text)


@events.register(events.NewMessage(
    chats=6974528785,
    incoming=True,
    func=lambda ev: "💼 На послугу: Реєстраційні дії з транспортними засобами" in ev.message.message)
)
async def re_registration_new_talon_handler(event):
    await ReRegistrationSubscriber().subscribe(event.message.text)


services = {
    56: practice_new_talon_handler,
    # 49: re_registration_new_talon_handler
}

if __name__ == '__main__':
    ConfigValidation.validate()

    with TelegramClient(session=StringSession(), api_id=Config.API_ID.value, api_hash=Config.API_HASH.value) as client:
        question_id = int(Config.QUESTION_ID.value)
        client.add_event_handler(services[question_id])
        logger.info("Бот запустився. Чекаємо нових повідомлень...")
        client.run_until_disconnected()
