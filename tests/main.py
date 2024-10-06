import asyncio

from hsc_gov_subscriber.services.practice_subscriber import PracticeSubscriber
from hsc_gov_subscriber.utils.config import ConfigValidation

if __name__ == '__main__':
    text = """🎫 Знайдено талони 🏛️ ТСЦ МВС № 4841 м. Миколаїв, пров. Транспортний, 1а/1
    💼 На послугу: 🚗 Практичний іспит (транспортний засіб навчального закладу)
    ✅ Талони наявні на наступні дати :
    📆 26.10.2024 - 1 🎫 талон"""

    ConfigValidation.validate()
    asyncio.run(PracticeSubscriber().subscribe(text))
