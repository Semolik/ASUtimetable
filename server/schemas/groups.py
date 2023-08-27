from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str
    id: int