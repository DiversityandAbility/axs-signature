from typing import List
from pydantic import BaseModel, validator, HttpUrl, EmailStr


class CreateSessionSchema(BaseModel):
    api_key: str
    declaration: str
    signee_email: EmailStr
    redirect_uri: HttpUrl
    methods: List[str] = ["type"]

    @staticmethod
    def from_form(data):
        d = {k: v for k, v in data.items() if v}
        if "methods" in data:
            d["methods"] = data.getlist("methods")
        return d

    @validator("api_key")
    def check_api_key(cls, v):
        if v != "123":
            raise ValueError("Incorrect API Key")
        return v
