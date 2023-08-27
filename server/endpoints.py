from fastapi import APIRouter
from server.ASU import ASU
from server.schemas import FacultyBase,Faculty
router = APIRouter()
asu_api = ASU()

@router.get("/faculties", response_model=list[FacultyBase])
async def get_faculties():
    return await asu_api.get_faculties()

@router.get("/faculties/{faculty_id}", response_model=Faculty)
async def get_faculty(faculty_id: int):
    return await asu_api.get_faculty(faculty_id=faculty_id)


@router.get("/faculties/{faculty_id}/groups/{group_id}")
async def get_group(faculty_id: int, group_id: int, date_start: int = None, date_end: int = None):
    return await asu_api.get_group(faculty_id=faculty_id, group_id=group_id, date_start=date_start, date_end=date_end)