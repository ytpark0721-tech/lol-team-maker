from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from routers import players, teams, matches

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="LOL Team Maker", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(matches.router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "LOL Team Maker API"}
