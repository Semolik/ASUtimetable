from fastapi import APIRouter
from api.schemas import ItemsModel
from api.config import STUDENTS_BASE_LINK
from ..utils.chache import GetChacheRequest
router = APIRouter()


@router.get("/faculties", response_model=ItemsModel)
async def get_faculties():
    return await GetChacheRequest(key='faculties', url=STUDENTS_BASE_LINK, xpath='//*[@id="page-content"]/div/div[1]/div[2]/div/a')
