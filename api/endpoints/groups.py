
from datetime import datetime
from datetime import timedelta
from api.utils.errors import ErrorMessage
from api.utils.messages import GetMessage

from api.utils.time import get_delta_from_string, timedelta_into_words, timedelta_to_string
from ..utils.chache import GetChacheRequest
from ..utils.parce import GetGroupPage
from api.schemas import GroupModel
from api.config import LESSON_DATETIME_FORMAT,  TIMETABLE_URL_DATETIME_FORMAT
from fastapi import APIRouter
router = APIRouter()


@router.get("/group", response_model=GroupModel)
async def get_group(faculty_id: int, group_id: int, date_start: int = None, date_end: int = None):
    try:
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        monday = now - timedelta(days=now.weekday())
        sunday = monday + timedelta(days=6)
        date_start, date_end = map(lambda _: datetime.strptime(
            str(_), TIMETABLE_URL_DATETIME_FORMAT) if _ else None, [date_start, date_end])
        if not date_start:
            date_start = monday
        if not date_end:
            date_end = sunday
        dates = [date_start, date_end]
    except ValueError:
        return ErrorMessage(message=GetMessage(404), status_code=404)
    return await GetChacheRequest(
        key=f'group_{faculty_id}_{group_id}_{date_start}_{date_end}',
        function=GetGroupPage,
        faculty_id=faculty_id,
        group_id=group_id,
        dates=dates,
        post_processing_function=highlight_current_processes,
        chache_hours=2
    )


async def highlight_current_processes(data):
    days = data.get('days')
    if days:
        today = datetime.now()
        now_timedelta = timedelta(
            hours=today.hour, minutes=today.minute, seconds=today.second)
        today_date_string = today.strftime(LESSON_DATETIME_FORMAT)
        for day_index, day in enumerate(days):
            if day['day']['date'] != today_date_string:
                continue
            days[day_index]['day']['current'] = True
            lessons = day.get('lessons')
            if not lessons:
                break
            add_timer_to_next = True
            for lesson_index, lesson in enumerate(lessons):
                time = lesson.get('time')
                if not time:
                    continue
                if is_async_lesson(lesson):
                    continue
                start = time.get('start')
                stop = time.get('stop')
                if not start or not stop:
                    continue
                start_timedelta = get_delta_from_string(start)
                stop_timedelta = get_delta_from_string(stop)
                if start_timedelta <= now_timedelta:
                    if now_timedelta <= stop_timedelta:
                        days[day_index]['lessons'][lesson_index]['time']['now'] = True
                        days[day_index]['lessons'][lesson_index]['time']['timer'] = (
                            stop_timedelta - now_timedelta).seconds
                elif add_timer_to_next:
                    days[day_index]['lessons'][lesson_index]['time']['timer'] = (
                        start_timedelta - now_timedelta).seconds
                    add_timer_to_next = False
        data['days'] = days
    return data


def is_async_lesson(lesson: dict) -> bool:
    lesson_type = lesson.get('type')
    return lesson_type and lesson_type.get(
        'on_distance') and lesson_type.get('is_async')
