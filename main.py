import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! .welcome to @Eritybot . run /channel command to upload all videos .')
  

def channel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('ss')

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    
    my_secret = os.environ['token']
    updater = Updater(my_secret)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("channel", channel))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()