from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.lifespan import lifespan

app = FastAPI(title=settings.app_name, version=settings.version, debug=settings.debug, lifespan=lifespan)
app.include_router(router)

