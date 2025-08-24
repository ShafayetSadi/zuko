import re
import docker
from typing import Tuple
from zuko.models import ExecutionResult


client = docker.from_env()


class DockerExecutor:
    def __init__(self, image="zuko-python:3.12", timeout=3):
        self.image = image
        self.timeout = timeout

    def run(self, code_path: str, input_path: str = None) -> ExecutionResult:
        container_path = f"/app/{code_path.split('/')[-1]}"
        input_container_path = (
            f"/app/{input_path.split('/')[-1]}" if input_path else "/dev/null"
        )

        python_cmd = f"python -u {container_path} < {input_container_path}"
        cmd = f'/usr/bin/time -f "ZUKO_TIME:%U:%S ZUKO_MEMORY:%M" {python_cmd}'

        try:
            container = client.containers.run(
                self.image,
                ["sh", "-c", cmd],
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
                    time_used=0,
                    memory_used=0,
                )

            exit_code = result.get("StatusCode", -1)
            logs = container.logs(stdout=True, stderr=True).decode(errors="replace")
            cpu_time_ms, memory_used_kb, clean_logs = self._parse_time_output(logs)
            container.remove()

            if exit_code == 0:
                return ExecutionResult(
                    status="OK",
                    stdout=clean_logs,
                    stderr="",
                    exit_code=exit_code,
                    time_used=cpu_time_ms,
                    memory_used=memory_used_kb,
                )
            else:
                return ExecutionResult(
                    status="RUNTIME_ERROR",
                    stdout=clean_logs,
                    stderr="",
                    exit_code=exit_code,
                    time_used=cpu_time_ms,
                    memory_used=memory_used_kb,
                )

        except docker.errors.ContainerError as e:
            return ExecutionResult(
                status="ERROR",
                stdout="",
                stderr=str(e),
                exit_code=e.exit_status,
                time_used=0,
                memory_used=0,
            )
        except Exception as e:
            return ExecutionResult(
                status="ERROR",
                stdout="",
                stderr=str(e),
                exit_code=-1,
                time_used=0,
                memory_used=0,
            )

    def _parse_time_output(self, logs: str) -> Tuple[float, int, str]:
        """
        Parse /usr/bin/time output and clean logs
        Returns: (cpu_time_ms, memory_kb, clean_logs)
        """

        # Look for ZUKO_TIME:user:system ZUKO_MEMORY:memory pattern
        time_pattern = r"ZUKO_TIME:(\d+\.?\d*):(\d+\.?\d*)\s+ZUKO_MEMORY:(\d+)"
        match = re.search(time_pattern, logs)

        if match:
            user_time = float(match.group(1))  # seconds
            system_time = float(match.group(2))  # seconds
            memory_kb = int(match.group(3))  # KB

            total_cpu_time = user_time + system_time
            cpu_time_ms = total_cpu_time * 1000 

            clean_logs = re.sub(time_pattern, "", logs).strip()

            return cpu_time_ms, memory_kb, clean_logs
        else:
            return 0.0, 0, logs
