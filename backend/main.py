from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from simulator import start_simulator
from models.log_model import Log
from models.metric_model import Metric


app = FastAPI(
    title="AI Ops Debug Agent",
    version="1.0"
)

# Create tables
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup_event():
    print("Starting simulator...")
    start_simulator()


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).order_by(Log.timestamp.desc()).limit(20).all()
    return logs


@app.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    metrics = db.query(Metric).order_by(Metric.timestamp.desc()).limit(20).all()
    return metrics