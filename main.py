from fastapi import FastAPI
from zuko.models import CodeRequest
from zuko.core.executor import run_code

app = FastAPI(title="Zuko - A Scalable Code Execution Engine")


@app.post("/execute")
def execute_code(req: CodeRequest):
    result = run_code(req.language, req.code, req.input_data)
    return result