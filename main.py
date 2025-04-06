from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from modules import weather_api, user_data, scheduler

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# Kullanım kılavuzu metni
def get_help_text():
    return (
        "Merhaba! Ben bir Hava Durumu Botuyum.

"
        "Butonları kullanarak aşağıdaki işlemleri yapabilirsin:
"
        "- Anlık hava durumunu öğren
"
        "- Günlük hava raporlarını al
"
        "- Konumunu kaydet

"
        "Başlamak için aşağıdaki butonları kullan."
    )

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Anlık Hava Durumu", callback_data="current_weather")],
        [InlineKeyboardButton("Günlük Rapor Al", callback_data="daily_report")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(get_help_text(), reply_markup=reply_markup)

# Callback buton işleyici
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "current_weather":
        await query.edit_message_text("Lütfen şehir adını yaz (örnek: İstanbul):")
        context.user_data["awaiting_location"] = "current_weather"

    elif query.data == "daily_report":
        await query.edit_message_text("Günlük rapor için şehir gir (örnek: Ankara):")
        context.user_data["awaiting_location"] = "daily_report"

# Kullanıcının mesajlarını ele al (örneğin şehir adı)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    intent = context.user_data.get("awaiting_location")

    if intent == "current_weather":
        weather = weather_api.get_current_weather(user_input)
        await update.message.reply_text(weather)
        context.user_data["awaiting_location"] = None

    elif intent == "daily_report":
        user_id = str(update.effective_user.id)
        user_data.save_user_location(user_id, user_input)
        await update.message.reply_text(f"{user_input} için günlük hava raporları gönderilecek.")
        context.user_data["awaiting_location"] = None

# Botu başlat
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("weather", start))
    app.add_handler(CommandHandler("forecast", start))
    app.add_handler(CommandHandler("setlocation", start))
    app.add_handler(CommandHandler("getlocation", start))
    app.add_handler(CommandHandler("removelocation", start))
    app.add_handler(CommandHandler("commands", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("reset", start))
    app.add_handler(CommandHandler("guide", start))
    app.add_handler(CommandHandler("usage", start))
    app.add_handler(CommandHandler("buttons", start))
    app.add_handler(CommandHandler("options", start))

    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    scheduler.setup_scheduler(app)  # Otomatik bildirim zamanlayıcısı
    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
