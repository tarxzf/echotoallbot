async def format_time(seconds: int) -> str:
    days_left, remainder = divmod(seconds, 86400)
    hours_left, remainder = divmod(remainder, 3600)
    minutes_left, seconds_left = divmod(remainder, 60)

    time_tuple = (days_left, hours_left, minutes_left, seconds_left)
    prefixes_tuple = ('дн', 'ч', 'мин', 'сек')
    
    result = ''
    for i in zip(time_tuple, prefixes_tuple):
        if i[0]:
            result += f'{i[0]} {i[1]} '
    return result
