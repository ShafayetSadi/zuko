from .files import FileManager
from .sandbox import DockerExecutor
from zuko.models import ExecutionResult


def run_code(
    language: str, code: str, input_data: str = "", timeout: int = 3
) -> ExecutionResult:
    if language != "python":
        return ExecutionResult(
            status="ERROR",
            stdout="",
            stderr=f"Unsupported language: {language}   ",
            exit_code=-1,
            time_used=0,
        )

    with FileManager(code, input_data) as fm:
        executor = DockerExecutor(timeout=timeout)
        return executor.run(fm.code_host_path, fm.input_host_path)
