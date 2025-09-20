import os
import asyncio
import aiohttp
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

# ---------------------------
# Настройки бота
# ---------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан! Установите переменную окружения.")

bot = Bot(token=TELEGRAM_BOT_TOKEN)


# Словарь для хранения времени последнего уведомления по каждой задаче и уведомлению
last_sent = {}
API_BASE = "http://127.0.0.1:8000"

# ---------------------------
# Асинхронная отправка сообщений
# ---------------------------
async def send_message(user_id: int, text: str):
    try:
        await bot.send_message(user_id, text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения {user_id}: {e}")

# ---------------------------
# Получение всех пользователей
# ---------------------------
async def get_all_users():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/users_with_sessions") as resp:
            if resp.status == 200:
                return await resp.json()  # [user_id, ...]
            return []

# ---------------------------
# Получение всех задач
# ---------------------------
async def get_all_tasks():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/all_tasks") as resp:
            if resp.status == 200:
                return await resp.json()
            return []

# ---------------------------
# Получение всех уведомлений
# ---------------------------
async def get_all_notifications():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/all_notifications") as resp:
            if resp.status == 200:
                return await resp.json()
            return []

# ---------------------------
# Поллинг и отправка уведомлений
# ---------------------------
async def poll_notifications():
    async with aiohttp.ClientSession() as session:
        # Берем всех пользователей
        async with session.get(f"{API_BASE}/users_with_sessions") as r:
            if r.status != 200:
                print("Не удалось получить пользователей")
                return
            users = await r.json()  # [user_id1, user_id2, ...]

        # Берем все задачи
        async with session.get(f"{API_BASE}/all_tasks") as r:
            if r.status != 200:
                print("Не удалось получить задачи")
                return
            tasks = await r.json()

        # Берем все уведомления
        async with session.get(f"{API_BASE}/all_notifications") as r:
            if r.status != 200:
                print("Не удалось получить уведомления")
                return
            all_notifications = await r.json()

        now = datetime.now()

        for task in tasks:
            task_id = task["task_id"]
            user_id = int(task["user_id"])

            # Фильтруем уведомления для этой задачи и которые via_tg
            notifications = [n for n in all_notifications if n["task_id"] == task_id and n.get("via_tg")]

            if not notifications:
                continue

            try:
                end_dt = datetime.strptime(f"{task['end_date']} {task['end_time']}", "%d.%m.%Y %H:%M")
            except:
                continue

            # пропускаем уже завершённые задачи
            if now > end_dt:
                continue

            for n in notifications:
                notif_id = n["id"]
                amount = n.get("amount", 1)
                unit = n.get("unit", "минут")

                # переводим в timedelta
                delta = None
                if unit == "минут":
                    delta = timedelta(minutes=amount)
                elif unit == "часов":
                    delta = timedelta(hours=amount)
                elif unit == "дней":
                    delta = timedelta(days=amount)
                elif unit == "недель":
                    delta = timedelta(weeks=amount)
                elif unit == "месяцев":
                    delta = timedelta(days=30*amount)
                elif unit == "лет":
                    delta = timedelta(days=365*amount)

                if delta is None:
                    continue

                # ключ для last_sent
                key = f"{task_id}_{notif_id}"

                # если ещё не отправляли или прошло больше delta, шлём
                if key not in last_sent or now - last_sent[key] >= delta:
                    # text = f"Напоминание: задача '{task['title']}'"
                    text = f"Напоминание: задача '{task['title']}' дедлайн: {end_dt}"
                    await send_message(user_id, text)
                    
                    last_sent[key] = now

                # Если осталось минут меньше или равно delta, уведомляем
                # if minutes_left <= delta_minutes:
                    
                    # await send_message(user_id, text)

# ---------------------------
# Запуск бота
# ---------------------------
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(poll_notifications, 'interval', seconds=30)
    scheduler.start()

    print("Бот запущен...")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
