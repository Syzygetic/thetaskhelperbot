from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from secrets import TOKEN

TOKEN: Final = TOKEN
BOT_USERNAME: Final = '@thetaskhelperbot'



# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Let us get started on your tasks!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here are all my available commands and their descriptions.')

async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Tell me what you want to note down, and I will jot it down for you!')

async def reminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Tell me what you want to be reminded of and when, and I will remind you when the time comes!')



# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    
    if 'how are you' in processed:
        return 'I am good!'
    
    if 'i love python' in processed:
        return 'Remember to subcribe!'
    
    return 'I do not understand what you wrote ...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "(text)"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
    print('Starting bot ...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('note', note_command))
    app.add_handler(CommandHandler('reminder', reminder_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling ...')
    app.run_polling(poll_interval=1)