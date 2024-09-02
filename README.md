# Self Destructing Downloader (Enhaced)
Это робот для загрузки видео, изображений и голосовых сообщений отправляемых через Telegram, с возможностью самоуничтожения.

Возможности робота:
- Высокая скорость в хранилище
- Отправляет копию сохраненных сообщений
- Оптимальное использование ресурсов

# Требуется
- Python (Последняя версия)
- Telethon (Последняя версия)

# Установка
```
git clone https://github.com/VadimChoi/Self-Destructing-Downloader-Enhaced.git
```
```
cd Self-Destructing-Downloader-Enhaced
```
```
pip install -r requirements.txt
```
# Использование
Создайте пустой .env файл через CMD:
```
type nul > .env
```
Или через PowerShell:
```
New-Item -Path ".\.env" -ItemType "File"
```
Либо через Linux/macOS терминалы:
```
touch .env
```

<br>
Откройте файл «.env» и скопируйте в него следующую информацию:

```
API_ID= API_ID_ЗДЕСЬ
API_HASH="API_HASH_ЗДЕСЬ"
MY_ID=ВАШ_ID
```
Эти значения можно получить на сайте my.telegram.org. ID можно узнать через сторонних ботов либо через веб-версию Telegram

<br>

Затем введите в терминале следующую команду и завершите процесс аутентификации:
```
python main.py
```
