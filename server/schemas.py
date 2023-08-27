from __future__ import annotations
from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str
    id: int


class FacultyBase(BaseModel):
    name: str
    id: int

class Faculty(FacultyBase):
    groups: list[GroupBase]

class Lecturer(BaseModel):
    name: str
    type: str

class Lesson(BaseModel):
    num: int | None
    name: str
    lesson_type: str
    lecturer: Lecturer
    time: str | None
    room: str | None
    on_distance: bool
    is_asynchronous: bool
    variants: list[Lesson] = []

class DayWithoutDate(BaseModel):
    date: str
    lessons: list[Lesson]

class Day(DayWithoutDate):
    name: str
    short_name: str

class Group(GroupBase):
    faculty: FacultyBase
    days: list[Day]
