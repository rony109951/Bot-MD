import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7735819374:AAGYHa59FZwXq21vNCccyMqj684CV4pJCe8"

# يخزن الربط مؤقتاً {رقم الواتس: كود}
linked_numbers = {}

def generate_code(length=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك في بوت جمايكا!\n"
        "ارسل رقم واتسابك لربطه مع البوت."
    )

async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.isdigit():
        code = generate_code()
        linked_numbers[text] = code
        await update.message.reply_text(
            f"تم إنشاء كود الربط لرقم {text}:\n\n"
            f"{code}\n\n"
            "انسخ هذا الكود واستخدمه في بوت الواتساب لتفعيل الربط."
        )
    else:
        await update.message.reply_text("من فضلك ارسل رقم واتساب صحيح فقط.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    print("بوت التليجرام شغال...")
    app.run_polling()
