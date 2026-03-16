import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from dotenv import load_dotenv

from jobs import PARAMS, get_jobs

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
CHANNEL_ID: int = int(os.environ["CHANNEL_ID"])

CHECK_INTERVAL = 300
SEND_DELAY = 1.2

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logging.getLogger("aiogram").setLevel(logging.WARNING)

dp.include_router(router)

USERS_FILE = "users.json"


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def add_user(user):

    users = load_users()

    if any(u["id"] == user["id"] for u in users):
        return

    users.append(user)

    save_users(users)

    logging.info(f"New user: {user['id']}")


def load_seen():
    try:
        with open("seen_jobs.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_seen(seen):
    with open("seen_jobs.json", "w") as f:
        json.dump(list(seen), f)


async def safe_send(text):

    while True:
        try:
            await bot.send_message(CHANNEL_ID, text)
            await asyncio.sleep(SEND_DELAY)
            return

        except TelegramRetryAfter as e:
            wait_time = int(e.retry_after)
            logging.warning(f"Flood control. Sleep {wait_time}s")
            await asyncio.sleep(wait_time)

        except Exception as e:
            logging.error(f"Send error: {e}")
            await asyncio.sleep(5)


async def check_jobs():

    seen = load_seen()

    try:
        jobs = await get_jobs()
    except Exception as e:
        logging.error(f"Jobs loading error: {e}")
        return

    new_jobs = [job for job in jobs if job["id"] not in seen]

    if not new_jobs:
        logging.info("No new jobs")
        return

    logging.info(f"Found {len(new_jobs)} new jobs")

    for job in new_jobs:
        text = f"💼 Новая вакансия\n\n{job['title']}\n\n{job['url']}"

        await safe_send(text)

        seen.add(job["id"])

    save_seen(seen)


async def job_loop():

    while True:
        try:
            await check_jobs()
        except Exception as e:
            logging.error(f"Job loop error: {e}")

        await asyncio.sleep(CHECK_INTERVAL)


@router.message(Command("start"))
async def start_command(message: Message):

    user = message.from_user
    assert user is not None

    add_user(
        {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
        }
    )

    text = (
        "Мониторинг новых вакансий Яндекса.\n"
        "Публикация в канал: "
        "<a href='https://t.me/+KqI4nj7Lbm9iMWUy'>Работа в Яндекс Беларусь</a>\n\n"
        "Создатель: @freimaurerey\n\n"
        "Текущие фильтры поиска:\n"
        f"<pre>{PARAMS}\n</pre>\n\n"
        "Код доступен на GitHub."
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="GitHub",
                    url="https://github.com/printsofjoe/yandex-jobs-telegram-bot",
                )
            ]
        ]
    )

    await message.answer(
        text, reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True
    )


async def main():

    logging.info("Bot started")

    asyncio.create_task(job_loop())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
