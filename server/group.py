from datetime import datetime, timedelta
from server.config import (
    DAYS_OF_THE_WEEK,
    DAYS_OF_THE_WEEK_SHORT,
    LESSON_DATETIME_FORMAT,
    TIMETABLE_URL_DATETIME_FORMAT,
)
from server.http import get_tree
from fastapi import HTTPException
from server.schemas import FacultyBase, Lecturer, Day, Lesson, Group, DayWithoutDate, Time

class GroupParser:
    def __init__(self, group_id: int, faculty_id: int):
        self.group_id = group_id
        self.faculty_id = faculty_id

    async def get_group(self, dates: list[datetime], faculty_data: FacultyBase):
        dateArg = '-'.join(map(lambda date: datetime.strftime(date, TIMETABLE_URL_DATETIME_FORMAT), dates))
        self.date_start = dates[0]
        self.date_end = dates[1]
        tree = await get_tree(f'https://www.asu.ru/timetable/students/{self.faculty_id}/{self.group_id}?date={dateArg}')

        box = tree.xpath('/html/body/div[contains(@class, "box")]')
        if box:
            message = ' '.join([text.text for text in box[0].getchildren()])
            raise HTTPException(status_code=500, detail=message)

        name = tree.xpath('/html/body/div[1]/div/div/div[1]/h1/text()')
        name = ' '.join(filter(None, name[-1].strip().split(' '))) if name else None

        schedule = self.get_schedule(tree)
        date_start, date_end = dates
        result_days = []

        for i in range((date_end - date_start).days + 1):
            day = date_start + timedelta(days=i)
            week_day = datetime.weekday(day)
            day_data = Day(
                name=DAYS_OF_THE_WEEK[week_day],
                short_name=DAYS_OF_THE_WEEK_SHORT[week_day],
                date=datetime.strftime(day, LESSON_DATETIME_FORMAT),
                lessons=schedule.get(day, []),
            )
            result_days.append(day_data)

        return Group(id=self.group_id, name=name, days=result_days, faculty=faculty_data)

    def get_schedule(self, tree) -> dict[datetime, list[Lesson]]:
        alert = tree.xpath('//div[@class="l-box alert"]/text()')
        if alert:
            alert_text = alert[0].strip()
            if alert_text == 'Нет занятий':
                return {}
            raise HTTPException(status_code=404, detail=alert_text)

        schedule = tree.xpath('.//div[@class="schedule_table-body"]')
        if not schedule:
            return {}

        schedule_data = {}
        for row in schedule[0].xpath('.//div[@class="schedule_table-body-rows_group"]'):
            date_str = row.xpath('.//span[@class="schedule_table-date-dm"]/text()')[0]
            date = datetime.strptime(date_str + f'.{self.date_start.year}', LESSON_DATETIME_FORMAT)
            lessons = self.get_lessons(row)
            schedule_data[date] = lessons

        return schedule_data

    def get_lessons(self, row) -> list[Lesson]:
        lessons = []
        for lesson in row.xpath('.//div[@class="schedule_table-body-row"]'):
            num = lesson.xpath('.//div[@data-type="num"]/text()')
            num = int(num[0]) if num else None

            subject = lesson.xpath('.//div[@data-type="subject"]')[0]
            name = ''.join(subject.xpath('.//following-sibling::text()')).strip()
            additional_badge = subject.xpath('.//span[contains(@class, "schedule_table-simple_badge")]/text()')
            additional_badge = additional_badge[0] if additional_badge else None
            lesson_type = subject.xpath('.//span[contains(@class, "schedule_table-badge")]/text()')
            lesson_type = lesson_type[0].strip() if lesson_type else None

            time = lesson.xpath('.//div[@data-type="time"]/text()')
            time = self.parse_time(time)

            lecturer_data = lesson.xpath('.//div[@data-type="lecturer"]')
            lecturer = self.get_lecturer(lecturer_data)

            room = lesson.xpath('.//div[@data-type="room"]/a/text()') or lesson.xpath('.//div[@data-type="room"]/text()')
            room = room[0].strip() if room else None

            subtext = subject.xpath('.//span[contains(@class, "schedule_table-subtext")]/text()')
            on_distance, is_asynchronous = self.parse_subtext(subtext)

            if on_distance:
                room = None
            lesson = Lesson(
                num=num,
                name=name,
                lesson_type=lesson_type,
                lecturer=lecturer,
                time=time,
                room=room,
                on_distance=on_distance,
                is_asynchronous=is_asynchronous,
                lesson_info=additional_badge,
            )

            lessons.append(lesson)

        return lessons

    def parse_time(self, time_data) -> Time:
        if time_data:
            time_data = time_data[0].split(' - ')
            return Time(start=time_data[0], end=time_data[1])
        return None

    def get_lecturer(self, lecturer_data) -> Lecturer:
        if lecturer_data:
            lecturer_name = lecturer_data[0].xpath('.//a/text()')
            lecturer_name = lecturer_name[0] if lecturer_name else None
            lecturer_type = lecturer_data[0].xpath('.//span[contains(@class, "schedule_table-simple_badge")]/text()')
            lecturer_type = lecturer_type[0] if lecturer_type else None

            if lecturer_name and lecturer_type:
                return Lecturer(name=lecturer_name, type=lecturer_type)
        return None

    def parse_subtext(self, subtext) -> tuple[bool, bool]:
        on_distance = False
        is_asynchronous = False

        if subtext:
            subtext = subtext[0].lower()
            if 'дистанционно' in subtext:
                on_distance = True
            if 'асинхронно' in subtext:
                is_asynchronous = True
        return on_distance, is_asynchronous
