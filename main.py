# best auto sticker bot

from os import remove as delete_file

from PIL import Image

from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update

from secret_key import KEY



def start(update: Update, context: CallbackContext):
    print(f"@{update.message.from_user.username}: /start")
    update.message.reply_text("Hellow uwu! Thiss bot cyan duu smt kawai UwU.\n\nIn case you are casual, type or click /help")



def help(update: Update, context: CallbackContext):
    print(f"@{update.message.from_user.username}: /help")
    update.message.reply_text("Yooo! Get Japanese Goblin'd:\n\nhttps://youtu.be/UIp6_0kct_U")



def photo(update: Update, context: CallbackContext):
    print(f"@{update.message.from_user.username}: photo")

    message = update.message
    photo = message.photo[-1]
    # TODO: process file without saving it locally
    # bytes_io = BytesIO(file.download_as_bytearray())
    file = context.bot.get_file(photo.file_id)
    file_path_in = photo.file_id + ".jpg"
    file_path_out = photo.file_id + "_edited.webp"
    file.download(file_path_in)

    image_in = Image.open(file_path_in)
    W, H = image_in.size

    # crop: left, top, right, bottom
    if W == H:
        image_out = image_in.crop((0, 0, W, H))
    elif W > H:
        image_out = image_in.crop(((W-H)//2, 0, W-(W-H)//2, H))
    else:
        image_out = image_in.crop((0, (H-W)//2, W, H-(H-W)//2))

    image_out_resized = image_out.resize((512, 512), resample=Image.BICUBIC)

    image_out_resized.save(file_path_out, format="webp")

    context.bot.send_sticker(chat_id=message.chat_id, sticker=open(file_path_out, "rb"))

    delete_file(file_path_in)
    delete_file(file_path_out)



def main():
    print("Started bot.")
    updater = Updater(KEY, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    # updater.dispatcher.add_handler(CommandHandler("test", test))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo))
    # updater.dispatcher.process_update()

    updater.start_polling()
    # TODO: enable it for release?
    # updater.idle()



if __name__ == "__main__":
    main()



