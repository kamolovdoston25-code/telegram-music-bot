"""
Telegram Musiqa Bot - do'stlar va yaqinlar uchun shaxsiy loyiha
Foydalanuvchi qo'shiq nomini yozadi, bot YouTube'dan qidirib, audio yuboradi.
"""

import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# ============ SOZLAMALAR ============
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DOWNLOAD_DIR = "downloads" 

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda salomlashish xabari"""
    user_name = update.effective_user.first_name or "do'stim"
    await update.message.reply_text(
            f"Salom, {user_name}! 👋 Men Doston ismli botman 🎵\n\n"
            "Sizga kerakli qo'shiqni topib beraman!\n"
            "Menga qo'shiq matnini yoki ijrochisini yozing, "
            "men sizga mos audio faylni topib beraman. \n\n"
            "Masalan Yulduz Usmonova - Sevgi"
    )


async def search_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi yozgan matn bo'yicha qo'shiq qidiradi va yuboradi"""
    query = update.message.text
    chat_id = update.effective_chat.id

    searching_msg = await update.message.reply_text(f"🔍 Qidirilmoqda: {query}...")

    # Fayl nomi uchun xavfsiz shablon
    output_template = os.path.join(DOWNLOAD_DIR, "%(title).80s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": output_template,
        "default_search": "ytsearch1",  # faqat 1 ta eng mos natija
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            # ytsearch natijasi ro'yxat sifatida qaytishi mumkin
            if "entries" in info:
                info = info["entries"][0]

            filename = ydl.prepare_filename(info)
            # mp3 ga o'zgartirilgani uchun kengaytmani to'g'irlaymiz
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"

        await searching_msg.edit_text("📤 Yuborilmoqda...")

        with open(mp3_filename, "rb") as audio_file:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=audio_file,
                title=info.get("title", "Noma'lum"),
                performer=info.get("uploader", ""),
            )

        # Diskni tozalash uchun faylni o'chiramiz
        os.remove(mp3_filename)
        await searching_msg.delete()

    except Exception as e:
        logger.error(f"Xatolik: {e}")
        await searching_msg.edit_text(
            "❌ Kechirasiz, bu qo'shiqni topa olmadim yoki yuklashda xatolik yuz berdi."
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_and_send))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()\

    