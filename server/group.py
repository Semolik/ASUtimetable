from datetime import datetime, timedelta
from server.config import DAYS_OF_THE_WEEK, DAYS_OF_THE_WEEK_SHORT, LESSON_DATETIME_FORMAT, TIMETABLE_URL_DATETIME_FORMAT
from server.http import get_tree
from fastapi import HTTPException
from server.schemas import FacultyBase, Lecturer, Day, Lesson, Group,DayWithoutDate, Time
class GroupParser:
    def __init__(self, group_id: int, faculty_id: int):
        self.group_id = group_id
        self.faculty_id = faculty_id

    async def get_group(self, dates: list[datetime], faculty_data: FacultyBase):
        dateArg = '-'.join(map(lambda date: datetime.strftime(
                date, TIMETABLE_URL_DATETIME_FORMAT), dates))
        tree = await get_tree(f'https://www.asu.ru/timetable/students/{self.faculty_id}/{self.group_id}?date={dateArg}')
        name = tree.xpath('/html/body/div[1]/div/div/div[1]/h1/text()')
        name = ' '.join(filter(None, name[-1].strip().split(' '))) if name else None
        shedule = self.get_shedule(tree)
        date_start, date_end = dates
        days_dates = list()
        for day in shedule:
            day_date = day.date
            if day_date:
                date = datetime.strptime(
                    day_date + f'.{date_start.year}', LESSON_DATETIME_FORMAT)
                days_dates.append(date)
        result_days = list()
        for i in range((date_end - date_start).days + 1):
            day = date_start + timedelta(days=i)
            week_day = datetime.weekday(day)
            day_data = Day(
                name=DAYS_OF_THE_WEEK[week_day],
                short_name=DAYS_OF_THE_WEEK_SHORT[week_day],
                date=datetime.strftime(day, LESSON_DATETIME_FORMAT),
                lessons=shedule[days_dates.index(day)].lessons if day in days_dates else []
            )
            result_days.append(day_data)
        return Group(id=self.group_id, name=name, days=result_days, faculty=faculty_data)

    def get_shedule(self, tree) -> list[Day]:
        alert = tree.xpath('//div[@class="l-box alert"]/text()')
        if alert:
            alert_text = alert[0].strip()
            if alert_text == 'Нет занятий':
                return []
            raise HTTPException(status_code=404, detail=alert_text)
        schedule = tree.xpath('.//div[@class="schedule_table-body"]')
        if not schedule:
            return []
        days = []
        for row in schedule[0].xpath('.//div[@class="schedule_table-body-rows_group"]'):
            date = row.xpath('.//span[@class="schedule_table-date-dm"]/text()')[0]
            lessons = row.xpath('.//div[@class="schedule_table-body-row"]')
            day: list[Lesson] = []
            for lesson in lessons:
                num = lesson.xpath('.//div[@data-type="num"]/text()')
                num = int(num[0]) if num else None

                subject = lesson.xpath('.//div[@data-type="subject"]')[0]
                name = ''.join(subject.xpath('.//following-sibling::text()')).strip()

                addtional_bage = subject.xpath('.//span[contains(@class, "schedule_table-simple_badge")]/text()')
                addtional_bage = addtional_bage[0] if addtional_bage else None
                lesson_type = subject.xpath('.//span[contains(@class, "schedule_table-badge")]/text()')
                lesson_type = lesson_type[0].strip() if lesson_type else None
                time = lesson.xpath('.//div[@data-type="time"]/text()')
                if time:
                    time = time[0].split(' - ')
                    time = Time(start=time[0], end=time[1])
                else:
                    time = None
                lecturer_data = lesson.xpath('.//div[@data-type="lecturer"]')
                lecturer = None
                if lecturer_data:
                    lecturer_name = lecturer_data[0].xpath('.//a/text()')
                    lecturer_name = lecturer_name[0] if lecturer_name else None
                    lecturer_type = lecturer_data[0].xpath('.//span[contains(@class, "schedule_table-simple_badge")]/text()')
                    lecturer_type = lecturer_type[0] if lecturer_type else None
                    lecturer = Lecturer(name=lecturer_name, type=lecturer_type) if lecturer_name and lecturer_type else None
                room = lesson.xpath('.//div[@data-type="room"]/a/text()')
                room = room[0] if room else None
                subtext = subject.xpath('.//span[contains(@class, "schedule_table-subtext")]/text()')
                on_distance = False
                is_asynchronous = False
                if subtext:
                    subtext = subtext[0].lower()
                    if 'дистанционно' in subtext:
                        on_distance = True
                    if 'асинхронно' in subtext:
                        is_asynchronous = True

                lesson = Lesson(
                    num=num,
                    name=name,
                    lesson_type=lesson_type,
                    lecturer=lecturer,
                    time=time,
                    room=room,
                    on_distance=on_distance,
                    is_asynchronous=is_asynchronous
                )
                if not time and len(day) > 0:
                    prev_lesson = day[-1]
                    if prev_lesson.name == lesson.name and prev_lesson.lesson_type == lesson.lesson_type and prev_lesson.lecturer == lesson.lecturer if not lecturer else (prev_lesson.lecturer.name == lesson.lecturer.name and prev_lesson.lecturer.type == lesson.lecturer.type) and prev_lesson.room == lesson.room:
                        day[-1].room = ' \ '.join([prev_lesson.room, lesson.room])

                    else:
                        day[-1].variants.append(lesson)
                    continue
                day.append(lesson)
            days.append(DayWithoutDate(date=date, lessons=day))
        return days