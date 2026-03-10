from fastapi import FastAPI
from database import start_db
from routers.species import router as species_router
from routers.birds import router as birds_router
from routers.birdspotting import router as birdspotting_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    start_db()


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(species_router)
app.include_router(birds_router)
app.include_router(birdspotting_router)