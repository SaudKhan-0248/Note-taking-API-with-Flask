from pydantic import BaseModel, constr, validator


class SignUp(BaseModel):
    username: constr(min_length=3, max_length=25)
    email: str
    password: constr(min_length=8, max_length=25)
    confirm_password: str

    @validator('confirm_password')
    def pwd_match(cls, value, values):
        if 'password' in values and value != values['password']:
            raise ValueError("Passwords doesnt Match!")
        return values


class Login(BaseModel):
    email: str
    password: constr(min_length=8, max_length=25)


class Note(BaseModel):
    title: str
    content: str
