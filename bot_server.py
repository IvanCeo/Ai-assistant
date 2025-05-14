
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# TOKEN = '7748646300:AAFR7-WZqKbzyFF02JJzDu0MnUlqWwpsSZo'

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# if __name__ == '__main__':
#     application = ApplicationBuilder().token('TOKEN').build()
    
#     start_handler = CommandHandler('start', start)
#     application.add_handler(start_handler)
    
#     application.run_polling()

# username of bot @AI_assistant_tokeon_test_bot

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Вставьте сюда ваш токен, полученный от @BotFather
TOKEN = '7748646300:AAFR7-WZqKbzyFF02JJzDu0MnUlqWwpsSZo'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я эхо-бот. Отправь мне сообщение, и я повторю его.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
