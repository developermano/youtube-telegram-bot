import os
import shutil
from telegram import Update,Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from pytube import Channel
import sched, time
from replit import db
import string
import random
from pytube import YouTube


bot=Bot(os.environ['token'])

def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    #context.bot.send_message(job.context, text='Beep!')
    for i in db.keys():
      print(i)
      try:
        c=Channel(db[i]['url'])
        print(db[i]['totalvideos'])
        print(len(c.video_urls))
        print(c.video_urls)
        if db[i]['totalvideos'] < len(c.video_urls):
          video=c.video_urls[0]
          try:
            yt = YouTube(video)
            fi=yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("out/")
          except:
            bot.send_message(db[i]['chatid'],"something goes wrong")
            shutil.rmtree('out')
          bot.send_video(db[i]['chatid'],open(fi, 'rb'))
          shutil.rmtree('out')
          chatid=db[i]['chatid']
          channelurl=db[i]['url']
          totalvideos=db[i]['totalvideos']+1
          
          del db[i]
          db[i] = {"chatid":chatid,"url":channelurl,"totalvideos":totalvideos}
      except:
        pass

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)





def rejesterping(channelurl,chat_id,total_videos):
  N = 7
  res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
  
  db[str(res)] = {"chatid":chat_id,"url":channelurl,"totalvideos":total_videos}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! .welcome to @Eritybot . run /channel command to upload all videos to this chat.')
  

def channel(update: Update, context: CallbackContext) -> None:
  if not str(context.args[0]).startswith("https://www.youtube.com"):
     update.message.reply_text('the youtube url must start with https://www.youtube.com')
     return 
  try:
    
    c = Channel(context.args[0])
    #for url in c.video_urls:
    #  print(url)
    avi=True
    for i in db.keys():
      print(i)
      if db[i]['url']==context.args[0]:
        if db[i]['chatid']==update.effective_message.chat_id:
          avi=False
    if avi==True:
      rejesterping(context.args[0],update.effective_message.chat_id,len(c.video_urls))
    else:
      update.message.reply_text('the channel is added already')
      return 
    for video in c.videos:
      try:
        fi=video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("out/")
      except:
        update.message.reply_text('the bot does not have enough space to download the video')
        shutil.rmtree('out')
      bot.send_video(update.effective_message.chat_id,open(fi, 'rb'))
      shutil.rmtree('out')
    

  except:
    update.message.reply_text('your video downloading may go wrong')


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.

    
    my_secret = os.environ['token']
    updater = Updater(my_secret)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("channel", channel,pass_args=True))

    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()