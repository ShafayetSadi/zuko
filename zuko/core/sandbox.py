import docker
import time
from zuko.models import ExecutionResult

client = docker.from_env()

class DockerExecutor:
    def __init__(self, image="python:3.12-slim", timeout=3):
        self.image = image
        self.timeout = timeout

    def run(self, code_path: str, input_path: str = None) -> ExecutionResult:
        container_path = f"/app/{code_path.split('/')[-1]}"
        input_container_path = f"/app/{input_path.split('/')[-1]}" if input_path else "/dev/null"

        cmd = f"sh -c 'python -u {container_path} < {input_container_path}'"

        try:
            start = time.time()
            container = client.containers.run(
                self.image,
                cmd,
                volumes={"/tmp": {"bind": "/app", "mode": "rw"}},
                working_dir="/app",
                mem_limit="128m",
                nano_cpus=1_000_000_000,
                pids_limit=64,
                network_disabled=True,
                read_only=True,
                security_opt=["no-new-privileges"],
                remove=False,
                detach=True,
                stdout=True,
                stderr=True,
            )

            try:
                result = container.wait(timeout=self.timeout)
            except Exception:
                container.kill()
                logs = container.logs().decode(errors="replace")
                container.remove()
                return ExecutionResult(
                    status="TIMEOUT",
                    stdout=logs,
                    stderr="",
                    exit_code=-1,
                    time_used=time.time() - start,
                )

            exit_code = result.get("StatusCode", -1)
            logs = container.logs().decode(errors="replace")
            container.remove()

            if exit_code == 0:
                return ExecutionResult(
                    status="OK",
                    stdout=logs,
                    stderr="",
                    exit_code=exit_code,
                    time_used=time.time() - start,
                )
            else:
                return ExecutionResult(
                    status="RUNTIME_ERROR",
                    stdout=logs,
                    stderr="",
                    exit_code=exit_code,
                    time_used=time.time() - start,
                )

        except docker.errors.ContainerError as e:
            return ExecutionResult(
                status="ERROR",
                stdout="",
                stderr=str(e),
                exit_code=e.exit_status,
                time_used=0,
            )
        except Exception as e:
            return ExecutionResult(
                status="ERROR",
                stdout="",
                stderr=str(e),
                exit_code=-1,
                time_used=0
            )