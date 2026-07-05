from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import app, clean_ticket
import traceback

from database import (
    init_db,
    save_ticket,
    get_history
)

init_db()

api = FastAPI()


class TicketRequest(BaseModel):
    subject: str
    body: str


@api.get("/")
def home():

    return {
        "message": "AI Ticket Classification API Running"
    }


@api.post("/predict")
def predict_ticket(data: TicketRequest):

    try:

        ticket_text = clean_ticket(
            data.subject + " " + data.body
        )

        result = app.invoke({
            "ticket_text": ticket_text
        })

        save_ticket(
            data.subject,
            data.body,
            result["type"],
            result["priority"],
            result["queue"],
            result["response"]
        )

        return {
            "ticket": ticket_text,
            "predicted_type": result["type"],
            "predicted_priority": result["priority"],
            "predicted_queue": result["queue"],
            "generated_response": result["response"]
        }

    except Exception as e:

        print(traceback.format_exc())

        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@api.get("/history")
def history():

    rows = get_history()

    history_data = []

    for row in rows:

        history_data.append({
            "id": row[0],
            "subject": row[1],
            "body": row[2],
            "category": row[3],
            "priority": row[4],
            "queue": row[5],
            "response": row[6],
            "created_at": row[7]
        })

    return history_data