import os
from telegram import Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from pytube import Channel

bot=Bot(os.environ['token'])

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! .welcome to @Eritybot . run /channel command to upload all videos to this chat.')
  

def channel(update: Update, context: CallbackContext) -> None:
    c = Channel(context.args[0])
    #for url in c.video_urls:
    #  print(url)
    for video in c.videos:
      fi=video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
      print(fi)
      bot.send_video(update.effective_message.chat_id,open(fi, 'rb'))
      os.remove(fi)

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    
    my_secret = os.environ['token']
    updater = Updater(my_secret)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("channel", channel,pass_args=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()