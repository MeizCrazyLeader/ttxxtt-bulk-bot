import os
import json
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext


def start(update: Update, context: CallbackContext):
    """Bot start command handler"""
    update.message.reply_text(
        "Welcome to the Bulk File Downloader Bot!\n"
        "Please send me the text file containing links or send links line by line directly."
    )


def download_files(update: Update, context: CallbackContext):
    """Handle the file(s) download"""
    message = update.effective_message
    chat_id = update.effective_chat.id

    if message.document:
        file = context.bot.get_file(message.document.file_id)
        file.download(f"links_{chat_id}.txt")
    elif message.text:
        lines = message.text.strip().split("\n")
        with open(f"links_{chat_id}.txt", "w") as file:
            file.write("\n".join(lines))

    file_path = f"links_{chat_id}.txt"
    
    with open(file_path, "r") as file:
        links = file.readlines()

    for i, link in enumerate(links):
        # Perform download logic for each link
        # example: download(link.strip())

        # Replace the download function above with custom logic
        # based on your downloading requirements
        # You may use libraries like 'requests' for HTTP downloads

        update.message.reply_text(f"Downloading file {i+1}: {link}")

    os.remove(file_path)


def app_json():
    """Generates app.json for Heroku deployment"""
    app_data = {
        "Container": "Heroku",
        "Size": "Basic",
        "Quantity": "1"
    }
    with open("app.json", "w") as file:
        json.dump(app_data, file, indent=4)


def main():
    # Telegram Bot API credentials
    API_ID = "your_api_id"
    API_HASH = "your_api_hash"
    TOKEN = "your_bot_token"

    app_json()

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download_files))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
