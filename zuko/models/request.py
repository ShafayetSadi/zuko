from pydantic import BaseModel

class CodeRequest(BaseModel):
    language: str
    code: str
    input_data: str = ""
    timeout: int = 3