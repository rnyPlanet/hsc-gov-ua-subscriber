import asyncio

from hsc_gov_subscriber.services.practice_subscriber import PracticeSubscriber

if __name__ == '__main__':
    text = """🎫 Знайдено талони 🏛️ ТСЦ МВС № 4841 м. Миколаїв, пров. Транспортний, 1а/1
    💼 На послугу: 🚗 Практичний іспит (транспортний засіб навчального закладу)
    ✅ Талони наявні на наступні дати :
    📆 28.5.2024 - 1 🎫 талон 
    📆 29.5.2024 - 1 🎫 талон 
    📆 30.5.2024 - 1 🎫 талон 
    📆 7.6.2024 - 1 🎫 талон"""

    asyncio.run(PracticeSubscriber().subscribe(text))
