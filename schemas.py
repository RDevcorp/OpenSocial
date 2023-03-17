from datetime import datetime
from pydantic import BaseModel

class UserBaseSchema(BaseModel):
    id: str | None = None
    email: str
    password: str
    first_name: str
    second_name: str
    status: str | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class UserLoginSchema(BaseModel):
    email: str
    password: str

