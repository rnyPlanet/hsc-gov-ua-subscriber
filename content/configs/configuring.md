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
в [cookies.json](/hsc_gov_subscriber/cookies.json) для авторизованих запитів на сайт.

**Кукі злітають автоматом через 30хв якщо не оновлювати сторінку сайту.** Щоб цього уникнути
рекомендую [встановити розширення бля браузеру](https://chromewebstore.google.com/detail/easy-auto-refresh/aabcgdmkeabbnleenpncegpcngjpnjkc?hl=en-US&utm_source=ext_sidebar)
і виставити 300сек.

Опис cookies файлу [cookies.json](/content/configs/cookies.md).

Гайд [де брати `cookies`](/content/configs/cookies.md).

</details>