
import datetime


def timedelta_into_words(timedelta, include_seconds=False, splitter=False):
    days = timedelta.days
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    result = list()
    if include_seconds:
        result.append('{} секунд{}'.format(seconds, conv(seconds)))
    if minutes > 0:
        result.append('{} минут{}'.format(minutes, conv(minutes)))
    if hours > 0:
        result.append('{} час{}'.format(
            hours, conv(hours, hours=True)))
    if days > 0:
        result.append('{} {}'.format(
            days, conv(days, days=True)))
    return (splitter or ', ').join(result[::-1])


def last_updated_timedelta_to_text(delta):
    return timedelta_into_words(delta, include_seconds=True)+' назад'


def conv(n, hours=False, days=False):
    es = (['', 'a', 'ов'] if hours else ['у', 'ы', '']
          ) if not days else ['день', 'дня', 'дней']
    n = n % 100
    if n >= 11 and n <= 19:
        s = es[2]
    else:
        i = n % 10
        if i == 1:
            s = es[0]
        elif i in [2, 3, 4]:
            s = es[1]
        else:
            s = es[2]
    return s


def get_delta_from_string(time):
    time = datetime.datetime.strptime(time, "%H:%M")
    return datetime.timedelta(hours=time.hour, minutes=time.minute)


def delta_to_days_hours_minutes(timedelta):
    return timedelta.days, timedelta.seconds//3600, (timedelta.seconds//60) % 60


def timedelta_to_string(timedelta):
    return ":".join(map(lambda _: str(_).rjust(2, '0'), delta_to_days_hours_minutes(timedelta)))
