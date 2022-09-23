from typing import List
from pydantic import BaseModel, HttpUrl, EmailStr


class CreateSessionSchema(BaseModel):
    title: str
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
