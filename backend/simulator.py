import random
import threading
import time
from datetime import datetime

from database import SessionLocal
from models.log_model import Log
from models.metric_model import Metric


services = ["auth-service", "payment-service", "order-service"]

log_levels = ["INFO", "WARN", "ERROR"]

messages = [
    "User login success",
    "Database connection slow",
    "Timeout occurred",
    "CPU spike detected",
    "Payment processing failed"
]


def generate_log():
    return Log(
        service=random.choice(services),
        level=random.choice(log_levels),
        message=random.choice(messages),
        timestamp=datetime.utcnow()
    )


def generate_metric():
    return Metric(
        service=random.choice(services),
        cpu=random.uniform(10, 95),
        memory=random.uniform(20, 90),
        latency=random.uniform(50, 500),
        timestamp=datetime.utcnow()
    )


def simulator_loop():
    db = SessionLocal()

    while True:
        log = generate_log()
        metric = generate_metric()

        db.add(log)
        db.add(metric)

        db.commit()

        print("Generated log and metric")

        time.sleep(3)


def start_simulator():
    thread = threading.Thread(target=simulator_loop)
    thread.daemon = True
    thread.start()