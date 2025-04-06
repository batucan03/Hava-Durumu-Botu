from apscheduler.schedulers.background import BackgroundScheduler
from modules import user_data, weather_api
from telegram import Bot
import asyncio

# Sabah 08:00'de gönderim yapan görev
async def send_daily_reports(app):
    bot: Bot = app.bot
    users = user_data.get_all_users()

    for user_id, city in users:
        weather = weather_api.get_current_weather(city)
        try:
            await bot.send_message(chat_id=int(user_id), text=f"Günlük hava raporun:

{weather}")
        except Exception as e:
            print(f"{user_id} kullanıcısına mesaj gönderilemedi: {e}")

# Scheduler kurulumu
def setup_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(send_daily_reports(app)), 'cron', hour=8, minute=0)
    scheduler.start()
