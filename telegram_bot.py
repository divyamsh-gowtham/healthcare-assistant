import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from prescription import extract_text, explain_prescription

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = """
🏥 Welcome to Family Health AI

You can:

• Send a prescription image
• Ask about medicines
• Ask health questions
"""

    await update.message.reply_text(message)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user_message = update.message.text

        reply = explain_prescription(user_message)

        await update.message.reply_text(reply)

    except Exception as e:

        print("Error:", e)

        await update.message.reply_text("⚠️ Something went wrong.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        file_path = "uploads/prescription.jpg"

        await file.download_to_drive(file_path)

        text = extract_text(file_path)

        result = explain_prescription(text)

        await update.message.reply_text(result)

    except Exception as e:

        print("Error:", e)

        await update.message.reply_text("⚠️ Could not read the prescription.")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot running...")

app.run_polling()