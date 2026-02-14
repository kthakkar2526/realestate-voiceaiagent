from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.routers import auth, chat, properties, bookings, leads, vapi_webhook, vapi_config
from app.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_tables()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="Real Estate AI Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(properties.router)
app.include_router(bookings.router)
app.include_router(leads.router)
app.include_router(vapi_webhook.router)
app.include_router(vapi_config.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
