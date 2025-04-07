import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from modules import weather_api, user_data, scheduler

ASK_CITY_WEATHER, ASK_CITY_REPORT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(
        [["Anlık Hava Durumu"], ["Günlük Rapor Al"]],
        resize_keyboard=True
    )
    await update.message.reply_text(
        """Merhaba! Ben bir Hava Durumu Botuyum.
- "Anlık Hava Durumu": Şehrini gir, anında bilgileri al.
- "Günlük Rapor Al": Şehrini kaydet, her sabah hava durumu mesajı al.

Bir seçim yap lütfen:""",
        reply_markup=reply_markup
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == "anlık hava durumu":
        await update.message.reply_text("Lütfen hava durumunu öğrenmek istediğiniz şehri yazınız:")
        return ASK_CITY_WEATHER
    elif text == "günlük rapor al":
        await update.message.reply_text("Günlük rapor almak için lütfen şehrinizi yazınız:")
        return ASK_CITY_REPORT
    else:
        await update.message.reply_text("Lütfen geçerli bir seçim yapınız.")
        return ConversationHandler.END

async def receive_city_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    weather = weather_api.get_current_weather(city)
    await update.message.reply_text(weather)
    return ConversationHandler.END

async def receive_city_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    user_id = str(update.message.from_user.id)
    user_data.save_user_location(user_id, city)
    await update.message.reply_text(f"{city} kaydedildi. Artık her sabah bu şehir için hava durumu alacaksınız.")
    return ConversationHandler.END

if __name__ == "__main__":
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
        states={
            ASK_CITY_WEATHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_city_weather)],
            ASK_CITY_REPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_city_report)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    scheduler.setup_scheduler(app)

    print("Bot başlatılıyor...")
    app.run_polling()
