from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    address: str
    email: str
    password: str