import os
import uuid

class FileManager:
    def __init__(self, code: str, input_data: str = ""):
        self.code = code
        self.input_data = input_data
        self.code_host_path = None
        self.input_host_path = None

    def __enter__(self):
        # Create code file
        code_filename = f"{uuid.uuid4()}.py"
        self.code_host_path = f"/tmp/{code_filename}"
        with open(self.code_host_path, "w") as f:
            f.write(self.code)

        # Create input file if needed
        if self.input_data:
            input_filename = f"{uuid.uuid4()}.txt"
            self.input_host_path = f"/tmp/{input_filename}"
            with open(self.input_host_path, "w") as f:
                f.write(self.input_data)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup
        try:
            if self.code_host_path and os.path.exists(self.code_host_path):
                os.remove(self.code_host_path)
            if self.input_host_path and os.path.exists(self.input_host_path):
                os.remove(self.input_host_path)
        except Exception:
            pass