from fastapi import HTTPException
from server.config import TIMETABLE_URL_DATETIME_FORMAT
from server.http import get_tree
from server.schemas import FacultyBase, GroupBase, Faculty
from server.cache import cache
from datetime import datetime, timedelta
import re
from server.group import GroupParser
class ASU:

    @cache(ttl=timedelta(days=1))
    async def get_faculties(self):
        tree = await get_tree('https://www.asu.ru/timetable/students/')
        faculties_links = tree.xpath('/html/body/div[1]/div/div/div[1]/ul[2]/li/a')
        faculties = []
        for link in faculties_links:
            faculty_id = int(link.attrib['href'].split('/')[0])
            name = link.text.strip()
            faculties.append(FacultyBase(id=faculty_id, name=name))
        return faculties
    
    @cache(ttl=timedelta(days=1))
    async def get_faculty(self, faculty_id: int):
        tree = await get_tree(f'https://www.asu.ru/timetable/students/{faculty_id}/')
        name_raw = ''.join(tree.xpath('/html/body/div[1]/div/div/div[1]/div[1]/div/text()'))
        name = re.sub(r'\((.*?)\)', r'\1', name_raw).strip()
        groups_links = tree.xpath('/html/body/div[1]/div/div/div[1]/div[2]/ul/li/a')
        if not groups_links:
            raise HTTPException(status_code=404, detail="Факультет не найден")
        groups = []
        for link in groups_links:
            group_id = int(link.attrib['href'].split('/')[0])
            groups.append(GroupBase(id=group_id, name=link.text.strip()))
        return Faculty(id=faculty_id, name=name, groups=groups)
    
    @cache.soft(ttl=timedelta(hours=5), soft_ttl=timedelta(days=1))
    async def get_group(self, faculty_id: int, group_id: int, date_start: datetime, date_end: datetime):
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
            raise HTTPException(status_code=400, detail="Неверный формат даты")
        if date_start > date_end:   
            raise HTTPException(status_code=400, detail="Дата начала больше даты конца")
        return await GroupParser(group_id=group_id, faculty_id=faculty_id).get_group(dates=dates, faculty_data=await self.get_faculty(faculty_id=faculty_id))

