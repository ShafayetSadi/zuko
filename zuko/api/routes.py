from fastapi import APIRouter
from zuko.models import CodeRequest
from zuko.core.executor import run_code

router = APIRouter()

@router.post("/execute")
def execute_code(req: CodeRequest):
    result = run_code(req.language, req.code, req.input_data)
    return result