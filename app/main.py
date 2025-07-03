from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, utils
import os
from datetime import date
from PIL import Image


app = FastAPI()
database.init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@app.get("/customers/", response_model=list[schemas.Customer])
def list_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    updated = crud.update_customer(db, customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated

@app.post("/customers/{customer_id}/photo")
def upload_photo(customer_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate image
    try:
        img = Image.open(file.file)
        img.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")
    file.file.seek(0)
    # Save photo
    os.makedirs("photos", exist_ok=True)
    file_path = f"photos/{customer_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    crud.set_photo_path(db, customer_id, file_path)
    return {"msg": "Photo uploaded successfully"}

@app.get("/customers/{customer_id}/interest")
def get_interest(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    interest, months = utils.calculate_interest(customer.loan_amount, customer.loan_date)
    color = utils.loan_age_color(months)
    return {"interest": interest, "months": months, "color": color}