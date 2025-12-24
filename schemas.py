from pydantic import BaseModel

class userCreate(BaseModel):
    username: str
    password = str

class UserLogin(BaseModel):
    username: str
    password: str