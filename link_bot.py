import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# تخزين روابط الربط {رقم_الواتس: كود_الربط}
linked_codes = {}

def generate_code(length=8):
    return   .join(random.choices(string.ascii_letters + string.digits, k=length))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً! أرسل رقم واتسابك لربط البوت.\nمثال: 201234567890"
    )

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("اكتب رقم واتساب واحد فقط بعد الأمر.")
        return
    whatsapp_number = context.args[0]
    code = generate_code()
    linked_codes[whatsapp_number] = code
    await update.message.reply_text(
        f"هذا كود الربط الخاص بك:\n`{code}`\n\n"
        "اذهب إلى بوت الواتساب وأرسل الكود لربط حسابك.",
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="تم الضغط على الزر!")

def main():
    TOKEN = "8189292683:AAE53IGPbRVoe5Sc3a5saQGXHzOE-NWxPWY"  # حط توكن بوت التيليجرام هنا
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("link", link))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("بوت تيليجرام شغال...")
    app.run_polling()

if __name__ ==  __main__ :
    main()
