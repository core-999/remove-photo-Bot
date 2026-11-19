import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================

# ==========================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
_owner_id_raw = os.environ.get("OWNER_ID", "").strip()

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing.")

try:
    OWNER_ID = int(_owner_id_raw)
except ValueError:
    raise ValueError("OWNER_ID environment variable must be a valid integer.")
# ==========================================


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("remove phone&video  bot")


async def handle_media_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    
    if message.chat.type in ["group", "supergroup"]:
        user = message.from_user

        if user:
            
            
            if user.id != OWNER_ID:
                if message.photo or message.video or message.animation:
                    try:
                        await message.delete()
                        logger.info(
                            f"Deleted media from user {user.id} ({user.full_name}) in group {message.chat.title}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to delete message: {e}. Make sure the bot has full admin rights."
                        )


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))

    media_filter = filters.PHOTO | filters.VIDEO | filters.ANIMATION
    application.add_handler(MessageHandler(media_filter, handle_media_messages))

    print("Bot is running and ready to delete media from non-owners (including admins)...")
    application.run_polling()


if __name__ == "__main__":
    main()
