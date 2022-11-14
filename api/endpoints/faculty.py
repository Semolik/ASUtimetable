from fastapi import APIRouter
from api.schemas import FacultyModel
from api.config import STUDENTS_BASE_LINK
from ..utils.parce import get_faculty_page
from ..utils.chache import GetChacheRequest

router = APIRouter()


@router.get("/faculty", response_model=FacultyModel)
async def get_faculty(faculty_id: int):
    return await GetChacheRequest(key=f'faculty_{faculty_id}', url=f'{STUDENTS_BASE_LINK}{faculty_id}/', xpath='//*[@id="page-content"]/div/div[1]/table/tr/td/div/a', function=get_faculty_page)
