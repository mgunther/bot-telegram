from configparser import ConfigParser
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler, CallbackQueryHandler)
from telegram     import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                          InlineKeyboardButton, InlineKeyboardMarkup)
import sqlite3
#
# Initialization
# --------------
#
config = ConfigParser()
config.read("chatbot.ini")
TOKEN   = config.get("CHATBOT", "token")
NAME    = config.get("CHATBOT", "name")
DESC    = config.get("CHATBOT", "description")
VERBOSE = config.get("CHATBOT", "verbose")
DBTYPE  = config.get("DB", "type")
if(DBTYPE == 'sqlite'):
    DBPATH = config.get("DB", "path")
    DBHOST = ""
    DBNAME = ""
    DBUSER = ""
    DBPASS = ""
    # sql = sqlite3.connect(DBPATH)
    # cursor = sql.cursor()
else:
    DBPATH = ""
    DBHOST = config.get("DB", "host")
    DBNAME = config.get("DB", "name")
    DBUSER = config.get("DB", "user")
    DBPASS = config.get("DB", "pass")

print("+------------------------------------------------------------+")
print("| CHATBOT FOR TELEGRAM                                       |")
print("+------------------------------------------------------------+")
print("| By Marcio Luis Gunther <marcio@marciogunther.com>          |")
print("| Version 0.1.0 (26-06-2020)                                 |")
print("+------------------------------------------------------------+")

if(VERBOSE == '1'):
    print(" CHATBOT NAME: ", NAME)
    print(" DESCRIPTION:  ", DESC)
    print(" TOKEN:        ", TOKEN)
    print(" DBTYPE:       ", DBTYPE)
    if(DBTYPE == 'sqlite'):
        print(" DBPATH:       ", DBPATH)
    else:
        print(" DBHOST:       ", DBHOST)
        print(" DBNAME:       ", DBNAME)
        print(" DBUSER:       ", DBUSER)
        print(" DBPASS:       ", DBPASS)

STATE1 = 1
STATE2 = 2

def welcome(update, context):
    try:
        message = ("Olá " + update.message.from_user.first_name + "!\n" +
            "Em que posso ajudá-lo hoje?")
        print(message)
        context.bot.send_message(chat_id = update.effective_chat.id, text = message)
    except Exception as e:
        print(str(e))

def feedback(update, context):
    try:
        message = 'Por favor, digite um feedback para o nosso tutorial:'
        update.message.reply_text(message, reply_markup = ReplyKeyboardMarkup([], one_time_keyboard = True))
        return STATE1
    except Exception as e:
        print(str(e))

def inputFeedback(update, context):
    feedback = update.message.text
    print(feedback)
    if len(feedback) < 10:
        message = ("Seu feedback foi muito curtinho...\n" +
                   "Informa mais pra gente, por favor?")
        context.bot.send_message(chat_id = update.effective_chat.id, text = message)
        return STATE1
    else:
        message = "Muito obrigado pelo seu feedback!"
        context.bot.send_message(chat_id = update.effective_chat.id, text = message)

def inputFeedback2(update, context):
    feedback = update.message.text
    message = "Muito obrigado pelo seu feedback!"
    context.bot.send_message(chat_id = update.effective_chat.id, text = message)

def cancel(update, context):
    return ConversationHandler.END

def askForNota(update, context):
    question = 'Qual nota você dá para o tutorial?'
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("☹️ 1", callback_data = '1'),
          InlineKeyboardButton("🙁 2", callback_data = '2'),
          InlineKeyboardButton("😐 3", callback_data = '3'),
          InlineKeyboardButton("🙂 4", callback_data = '4'),
          InlineKeyboardButton("😀 5", callback_data = '5')]])
    update.message.reply_text(question, reply_markup = keyboard)

def getNota(update, context):
    query = update.callback_query
    print(str(query.data))
    message = 'Muito obrigado pela sua nota: ' + str(query.data)
    context.bot.send_message(chat_id = update.effective_chat.id, text = message)

def dblist(update, context):
    try:
        tables = ""
        sql = sqlite3.connect(DBPATH)
        cursor = sql.cursor()
        cursor.execute("SELECT tbl_name FROM sqlite_master;")
        for table in cursor.fetchall():
            tables = tables + " - " + table + "\n"
        sql.close()
        message = ("There are the tables below in the database:\n" +
                    "Database name: " + DBPATH + "\n" +
                    "------------------------------\n" + tables)
        print(message)
        context.bot.send_message(chat_id = update.effective_chat.id, text = message)
    except Exception as e:
        print(str(e))





# --------------------------------------------------
# ChatBot para o Telegram
# By Marcio Luis Gunther <marcio@marciogunther.com>
# ==================================================
def main():
    try:
        updater = Updater(token=TOKEN, use_context=True)
        updater.dispatcher.add_handler(CommandHandler('start', welcome))
        updater.dispatcher.add_handler(CommandHandler('dblist', dblist))

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('feedback', feedback)],
            states={
                STATE1: [MessageHandler(Filters.text, inputFeedback)],
                STATE2: [MessageHandler(Filters.text, inputFeedback2)]
            },
            fallbacks=[CommandHandler('cancel', cancel)])
        updater.dispatcher.add_handler(conversation_handler)

        updater.dispatcher.add_handler(CommandHandler('nota', askForNota))
        updater.dispatcher.add_handler(CallbackQueryHandler(getNota))

        updater.start_polling()
        print(' Hello, I am the updater ' + str(updater))
        updater.idle()
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
