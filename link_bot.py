import json
import random
import string
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === إعداد توكن البوت ===
BOT_TOKEN = "7735819374:AAGYHa59FZwXq21vNCccyMqj684CV4pJCe8"

# === توليد كود عشوائي ===
def generate_code(length=6):
    return   .join(random.choices(string.ascii_letters + string.digits, k=length))

# === تحميل أكواد موجودة مسبقًا ===
def load_codes():
    try:
        with open("link_codes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# === حفظ الأكواد الجديدة ===
def save_codes(codes):
    with open("link_codes.json", "w") as f:
        json.dump(codes, f, indent=2)

# === عند استقبال رسالة من المستخدم ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if user_input.startswith("01") or user_input.startswith("201"):
        phone = user_input.replace("+", "")
        code = generate_code()
        codes = load_codes()
        codes[code] = phone
        save_codes(codes)
        await update.message.reply_text(f"✅ تم إنشاء كود الربط بنجاح!\n\n📞 الرقم: {phone}\n🔗 الكود: `{code}`\n\nانسخه وارسله في بوت الواتساب.\nمثال: `.ربط {code}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("📱 من فضلك أرسل رقم الواتساب بشكل صحيح.\nمثال: 201234567890")

# === أمر /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بيك في بوت ربط واتساب.\n\nارسل رقم واتسابك لعمل كود ربط.\nمثال: `201234567890`", parse_mode="Markdown")

# === تشغيل البوت ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 بوت التليجرام شغال...")
    app.run_polling()