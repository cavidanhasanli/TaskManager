from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from task.api.controller import router as task_router
from user.api.controller import router as user_router


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, docs_url="/")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
app.include_router(user_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")
