import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
)
from config import BOT_TOKEN
from handlers.start import start_command, help_command
from handlers.schedule import (
    add_schedule_start,
    add_schedule_receive,
    cancel_command,
    today_schedule,
    tomorrow_schedule,
    week_schedule,
    delete_schedule,
    handle_schedule_text,
    WAITING_SCHEDULE,
)
from handlers.menu import menu_command, menu_callback_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()

    add_schedule_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_schedule_start)],
        states={
            WAITING_SCHEDULE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_schedule_receive)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(add_schedule_handler)
    application.add_handler(CommandHandler("today", today_schedule))
    application.add_handler(CommandHandler("tomorrow", tomorrow_schedule))
    application.add_handler(CommandHandler("week", week_schedule))
    application.add_handler(CommandHandler("delete", delete_schedule))

    application.add_handler(CallbackQueryHandler(menu_callback_handler))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_schedule_text)
    )

    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
