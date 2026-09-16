"""Validation service FastAPI application: bootstrap y montaje de componentes."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="PDF Validation Service", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "validation-service"}


app.include_router(router)