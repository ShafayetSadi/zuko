from fastapi import FastAPI
from zuko.api.routes import router

app = FastAPI(title="Zuko - A Scalable Code Execution Engine")

app.include_router(router, prefix="/api/v1")
