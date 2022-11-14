from fastapi import APIRouter
from .endpoints import faculties, faculty, groups

main_router = APIRouter(prefix='/api')
main_router.include_router(faculties.router)
main_router.include_router(faculty.router)
main_router.include_router(groups.router)
