import asyncio
from datetime import datetime, timedelta
import json
import aiohttp
from aiohttp import client_exceptions
from api.containers import Container
from api.services import Service
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from api.config import BASE_URL, DATETIME_FORMAT, DAYS_OF_THE_WEEK, LESSON_DATETIME_FORMAT, MONTHS_IN_THE_GENITIVE_CASE, STUDENTS_BASE_LINK, session_timeout, TIMETABLE_URL_DATETIME_FORMAT
from lxml import etree
from bs4 import BeautifulSoup


@inject
async def GetPage(key, url, xpath, return_before_caching=False, service: Service = Depends(Provide[Container.service])):
    try:
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            response = await session.get(url)
            if response.status != 200:
                return response.status
            html = await response.text()
            tree = etree.HTML(html)
            items = tree.xpath(xpath)
            if not items:
                return 404
            items_list = [
                {
                    'id': a.get('href')[:-1],
                    'name': " ".join(a.text.split())
                }
                for a in items]
            if return_before_caching:
                return tree, items_list
            await service.SetCache(key, json.dumps({
                'items': items_list,
                'date': datetime.now().strftime(DATETIME_FORMAT)
            }), time=0)
            return {'items': items_list}
    except asyncio.exceptions.TimeoutError:
        return 504
    except client_exceptions.ClientConnectorError:
        return 502
    except:
        return 500


async def GetGroupPage(faculty_id, group_id, key, dates, service: Service = Depends(Provide[Container.service])):
    try:
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            dateArg = '-'.join(map(lambda date: datetime.strftime(
                date, TIMETABLE_URL_DATETIME_FORMAT), dates))
            response = await session.get(f'{STUDENTS_BASE_LINK}{faculty_id}/{group_id}/?date={dateArg}')
            if response.status != 200:
                return response.status
            html = await response.text()
            tree = etree.HTML(html)
            data = await AddFacultyData(root_node=tree, return_status_if_not_founded=True, timetable_page=True, include_group_data=True)
            if isinstance(data, int):  # если ссылка не корректная то данных о факультете не будет
                return data
            soup = BeautifulSoup(html, 'lxml')
            data['addresses'] = await get_locations_addresses(soup=soup)
            data['date'] = datetime.now().strftime(DATETIME_FORMAT)
            data['days'] = await get_shedule(soup=soup, dates=dates)
            await service.SetCache(key, json.dumps(data), time=0)
            return data
    except asyncio.exceptions.TimeoutError:
        return 504
    except client_exceptions.ClientConnectorError:
        return 502
    except Exception as e:
        return 500


async def get_locations_addresses(soup):
    addresses = soup.select(
        '.l-content-main > .padding_left_x.padding_right_x.t_gray')
    if not addresses:
        return []
    addresses_list = list()
    for address_node in addresses:
        address = {}
        address_letter_node = address_node.find(
            class_='inline_block t_red')
        if address_letter_node:
            address_letter = clear_whitespaces(address_letter_node.text)
            if address_letter:
                address['letter'] = address_letter
        separator_node = address_node.find(class_='t_gray_light', text='—')
        if separator_node:
            address_text = separator_node.next_sibling
            if address_text:
                address['address'] = clear_whitespaces(address_text)
        faculties_node = address_node.find(
            class_='t_small_x t_gray_light')
        if faculties_node:
            faculties_text = clear_whitespaces(faculties_node.text)
            if faculties_text:
                address['faculties'] = clear_whitespaces(
                    faculties_text.replace('(', '').replace(')', ''))
        addresses_list.append(address)
    return addresses_list


async def get_shedule(soup, dates):
    schedule = soup.find_all(class_='align_top schedule_table')
    if not schedule:
        return []
    temp_day = {}
    days = []
    for tr in schedule[0].find_all('tr'):
        if 'schedule_table-date' in tr.get('class'):
            if temp_day:
                days.append(temp_day)
            temp_day = {
                "day": {
                    "day_of_week":  tr.find(class_='t_bold').text,
                    "date": tr.find(class_='date t_small_x t_gray_light').text,
                },
                "lessons": list(),
            }
        else:
            tds = tr.find_all('td')
            tds_count = len(tds)
            lesson = {}
            if tds_count > 0:
                number_node = tds[0]
                if number_node and number_node.text:
                    lesson['number'] = clear_whitespaces(number_node.text)
            if tds_count > 1:
                time_node = tds[1].find('nobr')
                if time_node:
                    time_text = time_node.text
                    if time_text:
                        time = time_text.split('-')
                        if len(time) == 2:
                            lesson['time'] = {
                                'start': clear_whitespaces(time[0]),
                                'stop': clear_whitespaces(time[1])
                            }
            if tds_count > 2:
                lesson_type_options = {}
                lesson_type_name = tds[2].find('span', class_='t_gray_light')
                if lesson_type_name:
                    lesson_type_name_text = lesson_type_name.text
                    if lesson_type_name_text:
                        lesson_type_name_text = clear_whitespaces(
                            lesson_type_name_text)
                        lesson_type_options['name'] = lesson_type_name_text
                        lesson_type_options['is_lecture'] = lesson_type_name_text == 'лек.'
                        lesson_type_options['is_practice'] = lesson_type_name_text == 'пр.з.'
                        lesson_type_options['is_laboratory_work'] = lesson_type_name_text == 'лаб.'
                name = list(filter(lambda _: _ != '\n', tds[2].findAll(
                    text=True, recursive=False)))
                if name:
                    lesson['name'] = clear_whitespaces(name[0])
                lesson_type = tds[2].find('span', class_='t_small')
                if lesson_type:
                    lesson_type_text = lesson_type.text
                    if lesson_type_text:
                        lesson_type_text_chapters = lesson_type_text.split(' ')
                        lesson_type_options['on_distance'] = 'дистанционно' in lesson_type_text_chapters
                        lesson_type_options['is_async'] = 'асинхронно' in lesson_type_text_chapters
                lesson['type'] = lesson_type_options
            if tds_count > 3:
                lecturer_nobr_tag = tds[3].find('nobr')
                if lecturer_nobr_tag:
                    lecturer_a_tag = lecturer_nobr_tag.find('a')
                    if lecturer_a_tag:
                        link_chapters = lecturer_a_tag.get('href').split('/')
                        if len(link_chapters) > 4:
                            lecturer = {
                                'faculty_id': link_chapters[-4],
                                'department_id': link_chapters[-3],
                                'id':  link_chapters[-2],
                                'name': lecturer_a_tag.text,
                            }
                            lecturer_type = lecturer_nobr_tag.find(
                                class_='t_gray_light_x')
                            if lecturer_type:
                                lecturer_type_text = lecturer_type.text
                                if lecturer_type_text and lecturer_type_text != 'преп.':
                                    lecturer['type'] = lecturer_type.text
                            lesson['lecturer'] = lecturer
            if tds_count > 4:
                classroom_node = tds[4].find('a')
                if classroom_node:
                    classroom_node_text = classroom_node.text
                    if classroom_node_text:
                        classroom_chapters = classroom_node_text.split('\xa0')
                        if len(classroom_chapters) == 2:
                            audience = {
                                'location': classroom_chapters[1],
                            }
                            number = classroom_chapters[0]
                            if number:
                                if not lesson.get('time'):
                                    lessons = temp_day.get("lessons")
                                    if lessons:
                                        last_lesson = lessons[-1]
                                        last_lesson_name = last_lesson.get(
                                            'name')
                                        last_lesson_audience = last_lesson.get(
                                            'audience')
                                        if last_lesson_audience:
                                            last_lesson_audience_number = last_lesson_audience.get(
                                                'number')
                                            if last_lesson_audience_number:
                                                if not last_lesson_name:
                                                    last_lesson = merge_lessons(
                                                        lesson, last_lesson)
                                                last_lesson_audience['number'] = [
                                                    *last_lesson_audience_number, number]
                                                last_lesson['audience'] = last_lesson_audience
                                                lessons[-1] = last_lesson
                                                temp_day.update(
                                                    {"lessons": lessons})
                                                continue
                                else:
                                    audience['number'] = [number]
                            lesson['audience'] = audience
            if tds_count > 5:
                change_date_node = tds[5].find(class_='t_gray_light')
                if change_date_node:
                    changes = {
                        'date': clear_whitespaces(change_date_node.next_sibling),
                    }
                    freerooms_node = tds[5].find('a', class_='schedule_nav')
                    if freerooms_node:
                        changes['free_rooms_url'] = BASE_URL + \
                            freerooms_node.get('href')
                    lesson['changes'] = changes
            lessons = temp_day.get("lessons")
            if lessons is not None:
                lessons.append(lesson)
                temp_day.update({"lessons": lessons})
    if temp_day:
        days.append(temp_day)
    if days:
        date_start, date_end = dates
        days_dates = list()
        for day in days:
            day_date = day['day'].get('date')
            if day_date:
                days_dates.append(datetime.strptime(
                    day_date, LESSON_DATETIME_FORMAT))
        result_days = list()
        for i in range((date_end - date_start).days + 1):
            day = date_start + timedelta(days=i)
            if day in days_dates:
                day_data = days[days_dates.index(day)]
            else:
                week_day = datetime.weekday(day)
                day_data = {
                    'day': {
                        'date': datetime.strftime(day, LESSON_DATETIME_FORMAT),
                        'day_of_week': DAYS_OF_THE_WEEK[week_day],
                        'hide': week_day == 6,
                    },
                    'lessons': []
                }
            day_data['day']['month'] = MONTHS_IN_THE_GENITIVE_CASE[day.month - 1]
            result_days.append(day_data)
        return result_days
    return []


def merge_lessons(lesson_one, lesson_two):
    lesson = {}
    for key in set([*lesson_one.keys(), *lesson_two.keys()]):
        value_1 = lesson_one.get(key)
        value_2 = lesson_two.get(key)
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            lesson[key] = merge_lessons(value_1, value_2)
        else:
            lesson[key] = value_2 if value_1 is None else value_1
    return lesson


@inject
async def get_faculty_page(key, url, xpath, service: Service = Depends(Provide[Container.service])):
    GetPage_result = await GetPage(key=key, url=url, xpath=xpath, service=service, return_before_caching=True)
    if isinstance(GetPage_result, int):
        return GetPage_result
    tree, result = GetPage_result
    now = datetime.now()
    data = await AddFacultyData(json_data={
        'items': result,
        'date': now.strftime(DATETIME_FORMAT)
    }, root_node=tree)
    await service.SetCache(key, json.dumps(data), time=0)
    del data['date']
    return data


async def AddFacultyData(root_node, json_data={}, timetable_page=False, return_status_if_not_founded=False, include_group_data=False):
    faculty_data = root_node.xpath(
        f'//*[@id="page-content"]/div/div[1]/div[1]{"/div[1]" if not timetable_page else ""}')
    if faculty_data:
        faculty_data = faculty_data[0]
        faculty_data_string = ' '.join(
            ' '.join(list(filter(None, faculty_data.itertext()))).split())
        chapters = faculty_data_string.split(':', maxsplit=1)
        data = GetFacultyData(chapters)
        if not list(filter(None, data)):
            return 404
        if include_group_data:
            header = root_node.xpath('/html/body/div[1]/div/div/div[1]/h1')
            if header:
                header_text = header[0].text
                if header_text:
                    json_data['header_text'] = header_text
            group_name = root_node.xpath(
                '/html/body/div[1]/div/div/div[1]/ul/li')
            if group_name:
                group_name_text = group_name[-1].text
                if group_name_text:
                    json_data['group_name'] = clear_whitespaces(
                        group_name_text)
        name, tip, location, address = data
        if not name:
            name = tip
            tip = None
        json_data['name'] = name
        json_data['type'] = tip
        json_data['location'] = location
        json_data['address'] = address
    elif return_status_if_not_founded:
        return 404
    return json_data


def GetFacultyData(chapters):
    if len(chapters) == 2:
        chapters_ = chapters[1].split('(', maxsplit=1)
        nameone = clear_whitespaces(chapters_[0]) or None
        if len(chapters_) == 2:
            nametwo, namethree = clear_whitespaces(
                chapters_[1].split(')')[0]).split(',', maxsplit=1)
            nametwo = clear_whitespaces(nametwo) or None
            namethree = clear_whitespaces(namethree) or None
            chapters__ = chapters_[1].split(')', maxsplit=1)
            if len(chapters__) == 2:
                return nameone, nametwo, namethree, clear_whitespaces(chapters__[1].replace('\n', '')) or None
            return nameone, nametwo, namethree, None
        return nameone, None, None, None
    return None, None, None, None


def clear_whitespaces(text):
    return ' '.join(text.split(' ')).strip()
