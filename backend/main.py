from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import trainscripts, summary

app = FastAPI(title="AI Trainscript App", description="AI Trainscript App", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trainscripts.router, prefix="/api/trainscripts", tags=["trainscripts"])
app.include_router(summary.router, prefix="/api/summary", tags=["summary"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the backend AI Trainscript App"}