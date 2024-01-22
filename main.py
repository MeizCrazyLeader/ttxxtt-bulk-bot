import re
import requests
from telethon.sync import TelegramClient
from telethon import functions

def extract_links(input_url, output_file, excluded_extensions):
    response = requests.get(input_url)
    text = response.text

    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    
    filtered_links = [link for link in links if not any(extension in link for extension in excluded_extensions)]
    
    with open(output_file, 'w') as file:
        file.write('\n'.join(filtered_links))

    print(f"✅ Links Extracted")

# Set up Telegram bot credentials
api_id = '18429621'
api_hash = '2034b81303744d1dd2c7ffc02e21cfe2'
bot_token = '6712155081:AAF_1L4eOuJ0h9cPIGBijv1r-7Hbbt6ZR2I'

# Example usage
input_url = input("📤 Enter Direct Link of TXT File: ")
output_file = 'ace.txt'
excluded_extensions = ['.html', '.srt', '.txt', '.png', '.jpg', '.jpeg', '.url', '.nfo', '.webp']  # Add the extensions you want to exclude in this list

extract_links(input_url, output_file, excluded_extensions)

# Upload the file to Telegram using the bot
with TelegramClient('bot', api_id, api_hash) as client:
    client.send_file('your_channel_username', output_file)

print("📝 Conversion Completed 🎉")
print(f"📩 File uploaded to Telegram channel")
