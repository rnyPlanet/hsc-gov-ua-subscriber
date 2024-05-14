# HSC subscriber

## Про проєкт

Проєкт створенно для
прослуховуваня [телеграм бот ГСЦ МВС](https://hsc.gov.ua/2024/01/26/startuye-chat-bot-otrimuj-spovishhennya-pro-taloni-na-praktichni-ispiti-u-telegram/)
та автоматичного запису на практичний іспит (транспортний засіб навчального закладу) на категорії B; BE.

Запис відбувається менше ніж за 1сек (залежить від швидкості інтернету, та швидкості відповідей від сайту ГСЦ) після
сповіщення про новий наявний талон.

## Статистика

Скільки було сповіщень про нові білети за період з 2024-04-14 по 2024-05-12.

Можна зробити висновок що приблизно з 13:00 по 19:00 - мало сповіщень про нові білети, а приблизно з 5:00 по 12:00 -
спровіщень про білети більше. (Можливо у вас буде інакше)

![alt text](/content/notifications_stat/Grouped%20Data%20by%20Time%20and%20Day%20of%20Week.png)

(Свою статистику можна оформити після запуску [tg_bot_times_receiver](/notifications_stat/tg_bot_times_receiver.py)
та [grouping_by_hours_day_of_week](/notifications_stat/grouping_by_hours_day_of_week.py)).

## **[Питання\пропозиції можна писати сюди](https://github.com/rnyPlanet/hsc-gov-subscriber/issues/new)**.

### За замовчуванням працює автоматичний запис у ТСЦ МВС № 4841 м. Миколаїв, транспортний засіб навчального закладу на категорії B; BE.

### Будь який вклад в проєкт буде оцінюватися позитивно.

### важливе 1: НЕ БЕРІТЬ ТА НЕ ВІДМІНЯЙТЕ ПОСЛУГИ БІЛЬШЕ 4Х РАЗІВ - БУДЕ БЛОКУВАННЯ НА 10 ДНІВ (ТАК СКАЗАЛИ У ГСЦ КОЛИ Я ОТРИМАВ БЛОКУВАННЯ. БЛОКУВАННЯ У МЕНЕ БУЛО БІЛЬШЕ 10 ДНІВ, отримав поки дебажив код, зараз все працює ідеально)

![alt text](/content/photo_2024-05-12_20-14-30.jpg)

### важливе 2: Будьте обережні з файлами cookies після авторазиції на hsc.gov.ua через банк ID.

## Налаштування

<details>
<summary>1. Телеграм</summary>

Для прослуховування телеграма потрібні `App api_id` та `App api_hash`.

Гайд [як створити `App api_id` та `App api_hash`](/content/configs/tg/tg_api.md).

</details>

<details>
<summary>2. Конфіг файл</summary>

Опис конфіг файлу [config_file](/content/configs/config_file.md).

Гайд [де брати `OFFICE_ID` та `QUESTION_ID`](/content/configs/browser_requests/pract_ispt_id.md).

</details>

<details>
<summary>3. Файли cookies</summary>

Після вдалої авторизації на [https://eq.hsc.gov.ua/](https://eq.hsc.gov.ua/) потрібно додати кукі
в [cookies.json](/subscriber/cookies.json) для авторизованих запитів на сайт.

**Кукі злітають автоматом через 30хв якщо не оновлювати сторінку сайту.** Щоб цього уникнути
рекомендую [встановити розширення бля браузеру](https://chromewebstore.google.com/detail/easy-auto-refresh/aabcgdmkeabbnleenpncegpcngjpnjkc?hl=en-US&utm_source=ext_sidebar)
і виставити 300сек.

Опис cookies файлу [cookies.json](/content/configs/cookies.md).

Гайд [де брати `cookies`](/content/configs/cookies.md).

</details>

## Запуск

Після [налаштування](#налаштування) можна запустити [bot.py](/subscriber/bot.py).

В консолі запропонує ввести телефон, код який отримали в тг після підтвердження, пароль (якщо він є на аккаунті).
(Після кожної операції введення потрібно натискати Enter)
![alt text](/content/photo_2024-05-12_22-01-24.jpg)

Після вдалої авторизації звявиться файл `annon.session` - ФАЙЛ НІКОМУ НЕ ПЕРЕДАВАТИ.

ПІСЛЯ ВДАЛОГО ОТРИМАННЯ БІЛЕТУ ФАЙЛ ПОТРІБНО ВИДАЛИТИ ФАЙЛ `annon.session` ТА АКТИВНІ СЕСІЇЇ ТГ.
Settings -> Privacy and Security -> Active Sessions

Гайд [на `session`](/content/configs/tg/session_file.md).

## Contributing

Contributions are always welcome!

## Authors

[![portfolio](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/uknovvnuser)

#BUY_BTC
