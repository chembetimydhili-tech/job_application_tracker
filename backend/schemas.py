from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Literal
Status = Literal["Applied", "Interview", "Assessment", "Offer", "Rejected"]
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
class ApplicationIn(BaseModel):
    company: str = Field(min_length=1, max_length=160)
    role: str = Field(min_length=1, max_length=160)
    status: Status = "Applied"
    location: str = Field(default="", max_length=160)
    job_url: str = Field(default="", max_length=500)
    notes: str = Field(default="", max_length=5000)
    applied_on: str = Field(default="", max_length=10)
class ApplicationOut(ApplicationIn):
    id: int
    model_config = ConfigDict(from_attributes=True)
class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=160)
    role: str | None = Field(default=None, min_length=1, max_length=160)
    status: Status | None = None
    location: str | None = Field(default=None, max_length=160)
    job_url: str | None = Field(default=None, max_length=500)
    notes: str | None = Field(default=None, max_length=5000)
    applied_on: str | None = Field(default=None, max_length=10)
