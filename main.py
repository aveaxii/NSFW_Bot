# -*- coding:utf-8 -*-
import asyncio
import logging
from decouple import config
from telethon import TelegramClient, events, errors

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # Установлен уровень INFO для уменьшения подробности логирования
logger = logging.getLogger(__name__)

# Чтение api_id и api_hash из файла конфигурации
api_id = config('API_ID')
api_hash = config('API_HASH')

# Имя файла сессии
session_file = 'vadimchoi'

client = TelegramClient(session_file, api_id, api_hash)

@client.on(events.NewMessage(func=lambda e: e.is_private and (e.photo or e.video or e.document) and e.media_unread))
async def downloader(event):
    try:
        logger.info("Новое сообщение получено, загрузка медиа...")
        file_path = await event.download_media()
        logger.debug(f"Путь к загруженному медиафайлу: {file_path}")  # Это сообщение теперь не будет отображаться
        logger.info("Медиа загружено, отправка себе...")
        await client.send_file("me", file_path, caption="Загружено @VadimChoi")
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
