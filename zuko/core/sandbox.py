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
        input_container_path = (
            f"/app/{input_path.split('/')[-1]}" if input_path else "/dev/null"
        )

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

            stats_stream = container.stats(stream=True, decode=True)
            try:
                result = container.wait(timeout=self.timeout)
                stats = next(stats_stream)
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
                    memory_used=0,
                )
            finally:
                stats_stream.close()

            exit_code = result.get("StatusCode", -1)

            if stats and stats.get("memory_stats"):
                memory_used_bytes = stats["memory_stats"].get("max_usage", 0)
                if memory_used_bytes == 0:
                    memory_used_bytes = stats["memory_stats"].get("usage", 0)
                memory_used_kb = memory_used_bytes // 1024  # convert to KB
            else:
                memory_used_kb = 0

            if stats and stats.get("cpu_stats", {}).get("cpu_usage"):
                cpu_total = stats["cpu_stats"]["cpu_usage"]["total_usage"]
                cpu_time_ms = cpu_total / 1e6  # convert to ms
            else:
                cpu_time_ms = 0

            logs = container.logs().decode(errors="replace")
            container.remove()

            if exit_code == 0:
                return ExecutionResult(
                    status="OK",
                    stdout=logs,
                    stderr="",
                    exit_code=exit_code,
                    time_used=cpu_time_ms,
                    memory_used=memory_used_kb,
                )
            else:
                return ExecutionResult(
                    status="RUNTIME_ERROR",
                    stdout=logs,
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
