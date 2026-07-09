from fastapi import FastAPI

from backend.api.routes import router

app = FastAPI(
    title="CodeAtlas API",
    version="1.0.0",
    description="AI-powered GitHub Repository Assistant",
)

app.include_router(router)