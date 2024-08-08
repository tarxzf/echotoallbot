class Messages:
    # {user_name} - имя пользователя
    start_message = (
        'Привет, <i>{user_name}</i>! Это EchoToAll - бот, который анонимно отправит твоё сообщение '
        'всем пользователям бота'
        '\n  — Напиши сообщение, а я отправлю его всем пользователям'
    )

    # {error} - описание ошибки
    echo_error_message = (
        '⚠️ Во время отправки сообщения пользователя, произошла ошибка!'
        '\n  — Описание: <i>{error}</i>'
    )

    # {users_received} - количество получивших сообщение пользователей
    message_received_info = (
        'Сообщение получило <i>{users_received}</i> чел.'
    )

    tag_message_no_name = (
        '❌ Ваш тег <b>выключен</b>!'
        '\n  — Нажмите на кнопку ниже, чтобы включить его'
    )

    tag_message = (
        '✅ Ваш тег <b>включен</b>!'
        '\n  — Нажмите на кнопку ниже, чтобы выключить его'
    )

    # {user_name} - имя пользователя
    name_message = (
        '✅ Ваше имя: <i>{user_name}</i>'
        '\n  — Нажмите на кнопку ниже, чтобы изменить имя'
    )

    name_message_without_name = (
        '❕ У вас нет имени!'
        '\n  — Нажмите на кнопку ниже, чтобы установить его'
    )

    name_message_change = (
        '❔ Введите новое имя пользователя'
        '\n  — Нажмите на кнопку ниже, чтобы скрыть имя полностью'
    )

    name_message_canceled = (
        '✅ Вы успешно отменили изменение имени'
    )

    # {user_name} - имя пользователя
    name_message_changed = (
        '✅ Вы успешно изменили имя на "{user_name}"'
    )

    name_message_covered_up = (
        '✅ Вы успешно скрыли имя'
    )

    # {time_left} - оставшееся время
    early_message = (
        '🚀 Не так быстро! Попробуйте снова через {time_left}'
    )


    # Callback messages


    user_name_callback_message = (
        'ℹ️ Это имя пользователя'
    )

    user_name_no_url_callback_message = (
        '❌ Пользователь не включил отображение URL'
    )

    cannot_switch_url_callback_message = (
        '❌ Вы не можете включить отображение URL, так как у вас нет юзернейма'
    )

    custom_tag_callback_message = (
        'ℹ️ Это пользовательский тег админа'
    )
