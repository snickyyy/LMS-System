from pydantic import BaseModel


class MessageResponse(BaseModel):
    msg: str

class ErrorResponse(BaseModel):
    msg: str
