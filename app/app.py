from asyncio import run

from loader import bot, dp, connection
from handlers import start_handler, chat_handler
from middlewares.register_user import RegisteringUserMiddleware


@dp.shutdown()
async def on_shutdown():
    await connection.close()
    print('Telegram-Bot has been closed')


async def main():
    await connection.initialize()

    await connection.execute(
        '''CREATE TABLE IF NOT EXISTS users(
            id BIGINT PRIMARY KEY,
            name TEXT,
            registration_date TEXT NOT NULL,
            blocked BOOLEAN DEFAULT false
        );
        '''
    )
    # Таблица с пользователями

    await connection.execute(
        '''CREATE TABLE IF NOT EXISTS messages(
            id BIGINT NOT NULL,
            message_id BIGINT NOT NULL,
            unique_id BIGINT NOT NULL
        );
        '''
    )
    # Таблица с сообщениями (используется, для корректной работы реплаев)

    dp.include_routers(
        start_handler.router,
        chat_handler.router
    )
    dp.message.middleware(RegisteringUserMiddleware())

    print('Telegram-Bot has been launched successfully!')

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        ...