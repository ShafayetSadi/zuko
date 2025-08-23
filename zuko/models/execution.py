from pydantic import BaseModel

class ExecutionResult(BaseModel):
    status: str          # OK, RUNTIME_ERROR, TIMEOUT, ERROR
    stdout: str
    stderr: str
    exit_code: int
    time_used: float