from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.service.googly import GooglyEyes
from app.core.config import settings

# The GooglyEye service should only be loaded once as it
# will load the model into memory. We don't want
# to load the model on each request as this is inefficent and
# drains memory. This is implemented  with the lifespan
# asyncontextmanager below.
services = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    services["googly"] = GooglyEyes(settings.predictor_path)
    yield
    del services["googly"]
