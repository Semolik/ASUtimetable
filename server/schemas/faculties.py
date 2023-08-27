from pydantic import BaseModel
from server.schemas.groups import GroupBase
class FacultyBase(BaseModel):
    name: str
    id: int

class Faculty(FacultyBase):
    groups: list[GroupBase]