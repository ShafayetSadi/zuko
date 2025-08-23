import os
import docker
import uuid

client = docker.from_env()


def run_code(language: str, code: str, input_data: str = "", timeout: int = 3):
    filename = f"{uuid.uuid4()}.py"
    host_path = f"/tmp/{filename}"
    container_path = f"/app/{filename}"

    with open(host_path, "w") as f:
        f.write(code)

    try:
        if input_data:
            input_filename = f"{uuid.uuid4()}.txt"
            input_host_path = f"/tmp/{input_filename}"
            input_container_path = f"/app/{input_filename}"

            with open(input_host_path, "w") as f:
                f.write(input_data)

            try:
                # Run a one-off Python container with input redirection
                container = client.containers.run(
                    "python:3.12-slim",
                    f"sh -c 'python -u {container_path} < {input_container_path}'",
                    volumes={
                        "/tmp": {"bind": "/app", "mode": "rw"}
                    },  # Mount host /tmp at /app in the container
                    working_dir="/app",
                    mem_limit="128m",
                    nano_cpus=1_000_000_000,  # CPU limit (1e9 nanocpus = ~1 full CPU)
                    pids_limit=64,
                    network_disabled=True,
                    read_only=True,
                    security_opt=["no-new-privileges"],
                    remove=False,
                    detach=True,
                    stdout=True,
                    stderr=True,
                    stdin_open=False,
                    tty=False,
                )

                # Wait for container with timeout
                try:
                    result = container.wait(timeout=timeout)
                except Exception:
                    container.kill()
                    logs = container.logs().decode(errors="replace")
                    container.remove()
                    return {"status": "TIMEOUT", "output": logs}

                # Collect logs & exit code
                exit_code = result.get("StatusCode", -1)
                logs = container.logs().decode(errors="replace")

                if exit_code == 0:
                    return {"status": "OK", "output": logs}
                else:
                    return {"status": "RUNTIME_ERROR", "output": logs}

            except docker.errors.ContainerError as e:
                return {"status": "ERROR", "output": str(e)}
            except Exception as e:
                return {"status": "ERROR", "output": str(e)}
            finally:
                try:
                    os.remove(input_host_path)
                except Exception:
                    pass
        else:
            # No stdin data path: run Python without redirection
            container = client.containers.run(
                "python:3.12-slim",
                f"python -u {container_path}",  # -u for unbuffered output
                volumes={"/tmp": {"bind": "/app", "mode": "rw"}},
                working_dir="/app",
                mem_limit="128m",
                nano_cpus=1_000_000_000,
                pids_limit=64,
                network_mode="none",
                remove=False,
                detach=False,
                stdout=True,
                stderr=True,
                stdin_open=False,
                tty=False,
                read_only=True,
                security_opt=["no-new-privileges:true"],
                ulimits=[
                    docker.types.Ulimit(
                        name="fsize", soft=1024 * 1024, hard=1024 * 1024
                    )
                ],  # limit file size
            )

            output = container.decode(errors="replace")
            return {"status": "OK", "output": output}

    except docker.errors.ContainerError as e:
        return {"status": "ERROR", "output": str(e)}
    except Exception as e:
        return {"status": "ERROR", "output": str(e)}
    finally:
        try:
            os.remove(host_path)
        except Exception:
            pass
