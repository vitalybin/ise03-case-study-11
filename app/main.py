from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.presentation.api.routes import router as api_router
from app.container import Container, container as app_container
import app.container as container_module


templates = Jinja2Templates(directory='app/presentation/web/templates')


@asynccontextmanager
async def lifespan(app: FastAPI):
    container_module.container = Container()
    yield
    await container_module.container.api_client.close()


app = FastAPI(title='DDD Vehicle Control', version='1.0.0', lifespan=lifespan)
app.mount('/static', StaticFiles(directory='app/presentation/web/static'), name='static')
app.include_router(api_router)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
