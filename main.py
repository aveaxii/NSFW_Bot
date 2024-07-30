# -*- coding:utf-8 -*-
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from decouple import config
from telethon import TelegramClient, events, errors
from datetime import datetime

# Настройка логирования
log_filename = f"logs/telegram_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=5)  # Файл до 5MB, сохранять 5 резервных копий
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Чтение api_id и api_hash из файла конфигурации
api_id = config('API_ID')
api_hash = config('API_HASH')

# Имя файла сессии
session_file = 'vadimchoi'

client = TelegramClient(session_file, api_id, api_hash)

async def get_sender_info(event):
    """Получение информации об отправителе сообщения."""
    sender = await event.get_sender()
    if sender.username:
        return f"@{sender.username}"
    else:
        return f"ID: {sender.id}"

@client.on(events.NewMessage(func=lambda e: e.is_private and (e.photo or e.video or e.document) and e.media_unread))
async def downloader(event):
    try:
        sender_info = await get_sender_info(event)

        # Проверка, является ли отправитель сообщения тобой
        if event.sender_id == (await client.get_me()).id:
            logger.info(f"Пропускаем медиа от себя (отправитель: {sender_info}).")
            return
        
        logger.info(f"Новое сообщение получено от {sender_info}, загрузка медиа...")
        file_path = await event.download_media()
        logger.info(f"Путь к загруженному медиафайлу: {file_path}")
        logger.info("Медиа загружено, отправка себе...")
        await client.send_file("me", file_path, caption="Скачано @VadimChoi")
        logger.info("Медиа успешно отправлено.")
    except Exception as e:
        logger.error(f"Ошибка в загрузчике: {e}")

async def main():
    try:
        logger.info("Запуск клиента...")
        await client.start()
        logger.info("Клиент запущен")
        await client.run_until_disconnected()
    except errors.SessionRevokedError:
        logger.error("Сессия была отозвана, пожалуйста, авторизуйтесь заново.")
    except errors.FloodWaitError as e:
        logger.error(f"Ошибка ожидания: {e}")
    except errors.PhoneCodeInvalidError:
        logger.error("Введен неверный код подтверждения. Пожалуйста, проверьте и попробуйте снова.")
    except errors.PhoneNumberOccupiedError:
        logger.error("Этот номер телефона уже используется. Пожалуйста, используйте другой номер.")
    except errors.RPCError as e:
        logger.error(f"RPC ошибка: {e}")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
