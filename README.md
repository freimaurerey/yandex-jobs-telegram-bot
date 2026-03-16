# Yandex Jobs Bot

Телеграм-бот для отслеживания новых вакансий Яндекса.  
Бот регулярно проверяет страницу вакансий и публикует новые позиции в Telegram-канал.

Источник вакансий:  
https://yandex.ru/jobs/vacancies?work_modes=remote&cities=minsk&pro_levels=intern&pro_levels=junior

Бот написан на Python с использованием aiogram.

---

## Возможности

- проверка вакансий каждые 5 минут
- публикация новых вакансий в Telegram-канал
- защита от Telegram flood limit
- хранение уже отправленных вакансий
- регистрация пользователей при `/start`
- ссылка на репозиторий и описание через `/start`

---

## Пример сообщения

💼 Новая вакансия
Junior Python Developer
https://yandex.ru/jobs/vacancies/xxxxx

---

## Установка

Клонировать репозиторий:
git clone https://github.com/yourrepo/yandex-jobs-bot.git
cd yandex-jobs-bot

Создать виртуальное окружение:
python -m venv venv
source venv/bin/activate

Установить зависимости:
pip install -r requirements.txt

---

## Настройка

Создать файл `.env` в корне проекта.
BOT_TOKEN=your_telegram_bot_token
CHANNEL_ID=-100xxxxxxxxxx

Где:

`BOT_TOKEN` — токен бота из BotFather  
`CHANNEL_ID` — id канала, куда бот будет публиковать вакансии

---

## Запуск
python main.py

После запуска бот начинает:

1. слушать команды Telegram
2. каждые 5 минут проверять новые вакансии

---

## Файлы проекта
main.py
jobs.py
requirements.txt
users.json
seen_jobs.json
.env

### main.py

Основная логика бота:

- запуск aiogram
- команда `/start`
- отправка вакансий
- цикл проверки вакансий
- сохранение пользователей

### jobs.py

Работа с API вакансий Яндекса:

- запрос вакансий
- пагинация
- формирование списка вакансий

---

## Настройка фильтров вакансий

Фильтры находятся в файле `jobs.py`.
PARAMS = {
"cities": "minsk",
"work_modes": "remote",
"pro_levels": ["intern", "junior"],
"page_size": 20,
}

Параметры соответствуют фильтрам на сайте:

https://yandex.ru/jobs/vacancies

Например можно изменить:

город:
"cities": "moscow"

или уровень:
"pro_levels": ["junior"]

---

## Хранение данных

Бот использует два json файла.

`users.json`
[
{
"id": 123456789,
"username": "user",
"first_name": "Name"
}
]

Список пользователей, которые запускали бота.

---

`seen_jobs.json`
[12345, 12346, 12347]

ID вакансий, которые уже были отправлены.

---

## Используемые библиотеки

- aiogram
- aiohttp
- python-dotenv

Все зависимости указаны в `requirements.txt`.

---

## Автор

Telegram:  
https://t.me/freimaurerey
