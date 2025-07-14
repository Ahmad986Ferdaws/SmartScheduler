# app/main.py

from fastapi import FastAPI, HTTPException
from app import planner, gcal, db

app = FastAPI()

# Setup DB
db.init_db()

@app.post(\"/schedule\")
async def schedule_events(prompt: str):
    events = planner.generate_schedule(prompt)
    if not events:
        raise HTTPException(status_code=400, detail=\"Could not parse events.\")

    service = gcal.create_gcal_service()
    calendar_id = 'primary'

    results = []
    for event in events:
        link = gcal.create_event(service, calendar_id, event)
        db.save_event(event['title'], link)
        results.append({\"title\": event['title'], \"link\": link})

    return {\"scheduled_events\": results}

@app.get(\"/history\")
async def history():
    return {\"events\": db.get_all_events()}
