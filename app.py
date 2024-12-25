import os
import requests
from flask import Flask, request, jsonify
from telegram import Bot
import logging

app = Flask(__name__)

# Telegram bot token
TOKEN = '846266536:AAEpIsFIFRHneECFXsj_Rj3PWmKK2R3ufMY'
bot = Bot(token=TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    download_link = data['link']
    chat_id = data['chat_id']

    # Log the received chat_id and download link
    app.logger.info(f"Received chat_id: {chat_id}")
    app.logger.info(f"Download link: {download_link}")

    # Скачать MP3 файл
    response = requests.get(download_link)
    file_name = download_link.split('/')[-1].split('?')[0]

    with open(file_name, 'wb') as file:
        file.write(response.content)

    # Отправить MP3 файл в Telegram бота
    with open(file_name, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)

    # Удалить загруженный файл
    os.remove(file_name)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
