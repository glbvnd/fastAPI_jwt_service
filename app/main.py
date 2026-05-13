from contextlib import asynccontextmanager
from app.core.database import engine, Base
from fastapi import FastAPI, Depends
from fastapi_swagger import patch_fastapi


# Initial FastAPI Setups
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Start UP")
    Base.metadata.create_all(bind=engine)
    yield
    print("Application Shutdown ")

tags_metadata = [
    {
        "name": "Authentication Service",
        "version": "0.1",
        "description": "Protect of your system",
        "externalDocs": {
            "description": "More about me",
            "url": "https://fastapi.tiangolo.com/advanced/",
        }
    }
]
app = FastAPI(title="Auth Service",
              description="time will Up",
              version="0.0.1",
              terms_of_service="https://example.com/terms/",
              contact={
                  "name": "Nexus",
                  "url": "https://glbvnd.io",
                  "email": "s.golabavand1@gmail.com"
              },
              license_info={
                  "name": "MIT License"},
              docs_url=None, swagger_ui_oauth2_redirect_url=None, lifespan=lifespan, openapi_tags=tags_metadata)

patch_fastapi(app, docs_url="/swagger")


@app.get("/")
async def test(hi: str):
    return {"massege": hi}
