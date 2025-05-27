"""
Central module that runs the migrations and aggregate all the routes
"""

# pylint: disable=import-error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from personavix.src.routes import (
    answers,
    questionary,
    unique_access_links,
    users,
)
from personavix.src.database.database import engine, Base


Base.metadata.create_all(bind=engine)

description = """
## Welcome to PersonaVix API
PersonvaVix is a system developed to apply the DISC test, helping managers and the
HR team to better understand the behavioral profiles and personality traits of
employees and candidates. This API offers comprehensive features for login management,
user administration, obtaining DISC characteristics, as well as saving and storing test
results directly in the database.
"""

tags_metadata = [
    {
        "name": "Answers",
        "description": "operations related to answers of the disc test. This includes "
        "creating and obtaining answers.",
    },
    {
        "name": "Questionary",
        "description": "Operations related to disc questionary. This includes "
        "obtaining all disc characteristics and questions.",
    },
    {
        "name": "Unique Access Links",
        "description": "Operations related to unique access links. This includes "
        "creating and obtaining unique access links.",
    },
    {
        "name": "Users",
        "description": "Operations related to users. This includes creating and "
        "obtaining users.",
    },
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="PeronaVix API",
    description=description,
    version="1.0.0",
    contact={
        "name": "PersonaVix",
        "url": "https://personavix.com.br/",
    },
)

origins = [
    "http://localhost:5173",  # Temporary solution for CORS error
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(answers.router)
app.include_router(questionary.router)
app.include_router(unique_access_links.router)
app.include_router(users.router)


instrumentator = Instrumentator().instrument(app)


@app.on_event("startup")
async def _startup():
    instrumentator.expose(app)
