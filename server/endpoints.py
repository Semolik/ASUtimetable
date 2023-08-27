from fastapi import APIRouter
from server.ASU import ASU
from server.schemas.faculties import FacultyBase
router = APIRouter()
asu_api = ASU()

@router.get("/faculties", response_model=list[FacultyBase])
async def get_faculties():
    return await asu_api.get_faculties()

@router.get("/faculties/{faculty_id}")
async def get_faculty(faculty_id: int):
    return await asu_api.get_faculty(faculty_id)


@router.get("/faculties/{faculty_id}/groups/{group_id}")
async def get_group(faculty_id: int, group_id: int):
    ...