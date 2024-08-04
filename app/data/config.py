from environs import Env
from pathlib import Path

from data.types import StartMediaType

root_path = Path(__file__).parent.parent.parent.absolute()


env = Env()
env.read_env()

token = env.str('BOT_TOKEN')
# Телеграм токен бота

LOGGING_FILE_PATH = root_path / 'app/data/logs.log'
# Путь до файла логирования

DATABASE_PATH = root_path / 'app/data/sql.db'
# Путь до файла базы данных

USER_NAME = 'Анонимный Пользователь'
# Имя пользователя, если он его отключил



# Возможности бота

SEND_START_MEDIA = False
# Отправлять ли медиа при команде /start. Может быть либо True, либо False

START_MEDIA_TYPE = StartMediaType.GIF
# Тип медиа. Поддерживаются только StartMediaType.GIF и StartMediaType.PHOTO (GIF Анимации и фотографии)
# Для работы, SEND_START_MEDIA должен равняться True

START_MEDIA_FILE_ID = ''
# Файл айди медиа. Можно получить, если SHOW_MEDIA_FILE_ID установить значение True, а после
# отправить медиа боту. Файл айди отобразится в консоле. (P.S. Если вы запускаете бота
# на тестовом сервере, то после переноса кода, на основного бота, не забудьте сменить файл айди,
# так как он разный для каждого в медиа в каждом боте)
#
# Для работы, SEND_START_MEDIA должен равняться True

AUTODELETE_MESSAGE_INFO = True
# Автоудаление сообщений об успешной отправке сообщения

AUTODELETE_MESSAGE_INFO_DELAY = 3  # сек
# Задержка перед автоматическим удалением сообщения об успешной отправке сообщения в секундах
# Для работы, AUTODELETE_MESSAGE_INFO должен равняться True

SHOW_MEDIA_FILE_ID = False
# Выводить в консоль file_id фотографий и GIF анимаций. Может быть полезно для работы с START_MEDIA_FILE_ID
# Лучше отключать, если не используете

REPLIES_ENABLED = True
# Включена ли возможность отвечать на сообщения пользователей
# Может бить либо True, либо False

TAG_COMMAND_ENABLED = True
# Включена ли команда /tag для отображения имени
