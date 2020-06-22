from telegram.ext import Updater, CommandHandler

def welcome(update, context):
    message = ("Olá " + update.message.from_user.first_name + "!\n" +
        "Vamos iniciar a nossa negociação?\n" +
        "Em que posso ajudá-lo hoje?")
    print(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    token = '1182770672:AAE2ejI2vsG8kWLOSbpi8le0cdGbS9f09Ms'
    updater = Updater(token=token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', welcome))
    updater.start_polling()
    print('Oi, eu sou o updater ' + str(updater))
    updater.idle()

if __name__ == "__main__":
    main()
