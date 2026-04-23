from fastapi import FastAPI
from .database import engine, Base
from .database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from .models import Contact
import csv
from fastapi.responses import StreamingResponse
from io import StringIO
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("app/index.html") as f:
        return f.read()

@app.get("/")
def root():
    return {"message": "API is running"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contact")
def create_or_update_contact(name: str, phone: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.name == name).first()

    if contact:
        # update if phone different
        if contact.phone_number != phone:
            contact.phone_number = phone
            db.commit()
            return {"message": "updated"}
        return {"message": "no change"}

    # insert if not exists
    new_contact = Contact(name=name, phone_number=phone)
    db.add(new_contact)
    db.commit()

    return {"message": "created"}

@app.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@app.delete("/contact/{name}")
def delete_contact(name: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.name == name).first()

    if not contact:
        return {"message": "not found"}

    db.delete(contact)
    db.commit()

    return {"message": "deleted"}

@app.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()

    output = StringIO()
    writer = csv.writer(output)

    # header
    writer.writerow(["name", "phone_number"])

    # data
    for c in contacts:
        writer.writerow([c.name, c.phone_number])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=contacts.csv"}
    )
