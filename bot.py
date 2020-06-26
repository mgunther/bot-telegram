from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                         RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

STATE1 = 1
STATE2 = 2

def welcome(update, context):
    try:
        message = ("Olá " + update.message.from_user.first_name + "!\n" +
            "Vamos iniciar a nossa negociação?\n" +
            "Em que posso ajudá-lo hoje?")
        print(message)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        print(str(e))

def feedback(update, context):
    try:
        message = 'Por favor, digite um feedback para o nosso tutorial:'
        update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
        return STATE1
    except Exception as e:
        print(str(e))

def inputFeedback(update, context):
    feedback = update.message.text
    print(feedback)
    if len(feedback) < 10:
        message = """Seu feedback foi muito curtinho...
                        \nInforma mais pra gente, por favor?"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return STATE1
    else:
        message = "Muito obrigado pelo seu feedback!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def inputFeedback2(update, context):
    feedback = update.message.text
    message = "Muito obrigado pelo seu feedback!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def cancel(update, context):
    return ConversationHandler.END

# --------------------------------------------------
# ChatBot para o Telegram
# By Marcio Luis Gunther <marcio@marciogunther.com>
# ==================================================
def main():
    try:
        token = '1182770672:AAE2ejI2vsG8kWLOSbpi8le0cdGbS9f09Ms'
        updater = Updater(token=token, use_context=True)
        updater.dispatcher.add_handler(CommandHandler('start', welcome))

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('feedback', feedback)],
            states={
                STATE1: [MessageHandler(Filters.text, inputFeedback)],
                STATE2: [MessageHandler(Filters.text, inputFeedback2)]
            },
            fallbacks=[CommandHandler('cancel', cancel)])
        updater.dispatcher.add_handler(conversation_handler)

        updater.start_polling()
        print('Oi, eu sou o updater ' + str(updater))
        updater.idle()
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
