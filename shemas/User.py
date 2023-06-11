from pydantic import BaseModel, EmailStr, Field, Required

class User(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="John Doe")
    username: str = Field(example="jhondoe")
    email: EmailStr = Field(example="jhon@gmail.com")
    address: str = Field(example="123 Main St")
    phone: str = Field(example="000000000000")
    password: str = Field(example="password")
    disabled: bool
