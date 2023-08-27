
from functools import reduce
from server.http import get_tree
from server.schemas.faculties import FacultyBase, GroupBase, Faculty
from server.cache import cache
from datetime import timedelta

import re
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
        groups = []
        for link in groups_links:
            group_id = int(link.attrib['href'].split('/')[0])
            groups.append(GroupBase(id=group_id, name=link.text.strip()))
        return Faculty(id=faculty_id, name=name, groups=groups)