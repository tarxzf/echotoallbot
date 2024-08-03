from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import Message
from typing import NewType, Union, Tuple

from data.messages import Messages

ReceiverId = NewType('ReceiverId', int)
# Айди получателя

MessageId = NewType('MessageId', Union[int | bool | None])
# Айди сообщения. Может быть либо числом, либо False, либо None. Если айди сообщения равно None,
# то это значит, что сообщение не было доставлено по каким-то причинам. Если равно False,
# то сообщение не было доставлено из-за того, что пользователь заблокировал бота
# и его нужно заблокировать

MessageResponse = NewType('MessageResponse', Tuple[ReceiverId, MessageId])


async def send_message(message: Message, bot: Bot, receiver_id: int) -> MessageResponse:
    try:
        # Отправляем сообщение пользователю
        received_message = await message.copy_to(receiver_id)

    except TelegramForbiddenError:
        # Пользователь заблокировал бота
        return (receiver_id, False)
    
    except TelegramBadRequest as _ex:
        # Произошла ошибка связанная с TelegramBadRequest
        try:
            await bot.send_message(Messages.echo_error_message.format(error=_ex.message))
        except Exception as _ex:
            # Произошла другая ошибка
            print(f'An error occured while sending the message. Description: {_ex}')
            return (receiver_id, None)
        return (receiver_id, None)
    
    except Exception as _ex:
        # Произошла другая ошибка
        print(f'An error occured while sending the message. Description: {_ex}')
        return (receiver_id, None)
        
    return (receiver_id, received_message.message_id)

