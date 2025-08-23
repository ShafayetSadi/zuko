from pydantic import BaseModel


class ExecutionResult(BaseModel):
    status: str  # OK, TLE, TRE, CE
    stdout: str
    stderr: str
    exit_code: int
    time_used: float # in ms
    memory_used: int  # in KB
