from contextlib import asynccontextmanager
from app.core.database import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_swagger import patch_fastapi
from app.routers.auth_routers import router as auth_router

# Initial FastAPI Setups


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Application Start UP")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("🛑 Application Shutdown")
    await engine.dispose()


tags_metadata = [
    {
        "name": "Authentication Service",
        "version": "0.1",
        "description": "Protect of your system",
        "externalDocs": {
            "description": "More about me",
            "url": "https://fastapi.tiangolo.com/advanced/",
        },
    }
]
app = FastAPI(
    title="Auth Service",
    description="time will Up",
    version="0.0.1",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "Nexus",
        "url": "https://glbvnd.io",
        "email": "s.golabavand1@gmail.com",
    },
    license_info={"name": "MIT License"},
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

patch_fastapi(app, docs_url="/swagger")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_router, prefix="/AuthService")
