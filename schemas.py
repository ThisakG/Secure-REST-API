from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    username: str
    password: constr(min_length=8, max_length=72)

class UserLogin(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str
