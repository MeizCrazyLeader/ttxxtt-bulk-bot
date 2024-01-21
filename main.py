import telegram
import requests

# Set up your bot with API id and hash
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

# Create an instance of the Telegram bot
bot = telegram.Bot(token=bot_token)

# Function to handle incoming messages
def handle_message(update, context):
    message = update.message

    # Check if the message contains any links
    urls = get_urls_from_message(message)
    if urls:
        for url in urls:
            download_file(url, message.chat_id)
    else:
        message.reply_text('No download links found.')

# Function to extract URLs from a text message
def get_urls_from_message(message):
    entities = message.entities
    urls = []
    if entities:
        for entity in entities:
            if entity.type == 'url':
                urls.append(message.text[entity.offset:entity.offset + entity.length])
    return urls

# Function to download a file from a given URL
def download_file(url, chat_id):
    filename = url.split('/')[-1]
    response = requests.get(url, stream=True)

    # Save the file to disk
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

    # Send the file to the Telegram chat
    with open(filename, 'rb') as file:
        bot.send_document(chat_id, document=file)

    # Remove the temporarily saved file
    os.remove(filename)

# Set up the bot's message handler
from telegram.ext import MessageHandler, Filters, Updater
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot
updater.start_polling()
