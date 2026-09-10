from fastapi import FastAPI

from src.features.health.route import router as health_router

app = FastAPI(
    title="text-to-sql agent",
    description="let user query db using natural language",
)


app.include_router(health_router)
