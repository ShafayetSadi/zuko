from fastapi import FastAPI
from pydantic import BaseModel
from zuko.core.executor import run_code

app = FastAPI(title="Zuko - A Scalable Code Execution Engine")

class CodeRequest(BaseModel):
    language: str
    code: str
    input_data: str = ""

@app.post("/execute")
def execute_code(req: CodeRequest):
    result = run_code(req.language, req.code, req.input_data)
    return result