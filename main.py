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
