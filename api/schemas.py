from typing import List
from xmlrpc.client import Boolean
from pydantic import BaseModel


class ItemModel(BaseModel):
    id: int
    name: str


class Info(BaseModel):
    last_updated: str
    message: str | None


class FacultyData(Info):
    name: str | None
    type: str | None
    location: str | None
    address: str | None


class ItemsModel(Info):
    items: List[ItemModel]


class FacultyModel(FacultyData, ItemsModel):
    pass


class DayInfo(BaseModel):
    day_of_week: str
    date: str
    month: str
    current: bool = False
    hide: bool = False


class LessonTimeModel(BaseModel):
    start: str
    stop: str
    now: bool = False
    timer: int = False


class LessonTypeModel(BaseModel):
    name: str = None
    on_distance: bool = False
    is_async: bool = False
    is_lecture: bool = False
    is_practice: bool = False
    is_laboratory_work: bool = False


class LecturerModel(BaseModel):
    id: str
    faculty_id: str
    department_id: str
    name: str
    type: str = None


class AudienceModel(BaseModel):
    location: str
    number: list[str] = None


class ChangesModel(BaseModel):
    date: str
    free_rooms_url: str = None


class LessonModel(BaseModel):
    number: str = None
    time: LessonTimeModel = None
    name: str = None
    type: LessonTypeModel = None
    lecturer: LecturerModel = None
    audience: AudienceModel = None
    changes: ChangesModel = None


class TimetableDay(BaseModel):
    day: DayInfo
    lessons: List[LessonModel]


class AddressModel(BaseModel):
    letter: str = None
    address: str = None
    faculties: str = None


class GroupModel(FacultyData):
    header_text: str = None
    group_name: str = None
    addresses: list[AddressModel]
    days: List[TimetableDay]
