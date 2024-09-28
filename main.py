import logging
import uuid
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, users, issues, service_engineers
from sqlalchemy import select, update
import test 

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User model
class User(BaseModel):
    username: str
    email: str
    password: str

# Request model for the new endpoint
class IssueRequest(BaseModel):
    issue: str
    location: str
    phone: int
    user_id: str

# Response model for the new endpoint
class IssueResponse(BaseModel):
    complaintid: str
    esttime: str
    name: str
    phone: int

# Service Engineer model
class ServiceEngineer(BaseModel):
    name: str
    availability: bool

# Admin model
class Admin(BaseModel):
    username: str
    password: str

@app.post("/signup")
def sign_up(user: User, db: Session = Depends(get_db)):
    user_id = str(uuid.uuid4())
    stmt = select(users).where(users.c.username == user.username)
    existing_user = db.execute(stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db.execute(users.insert().values(user_id=user_id, username=user.username, email=user.email, password=user.password))
    db.commit()
    return {"code": "success", "user_id": user_id}

@app.post("/signin")
def sign_in(user: User, db: Session = Depends(get_db)):
    stmt = select(users).where(users.c.username == user.username, users.c.password == user.password)
    existing_user = db.execute(stmt).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"code": "success"}

@app.post("/report_issue", response_model=IssueResponse)
def report_issue(issue_request: IssueRequest, db: Session = Depends(get_db)):
    # Check if user exists
    stmt = select(users).where(users.c.user_id == issue_request.user_id)
    existing_user = db.execute(stmt).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    # Find an available service engineer
    stmt = select(service_engineers).where(service_engineers.c.availability == True)
    available_engineer = db.execute(stmt).first()
    if not available_engineer:
        raise HTTPException(status_code=400, detail="No available service engineers")

    # Generate unique complaint ID
    complaintid = str(uuid.uuid4())

    # Dummy response data
    response_data = IssueResponse(
        complaintid=complaintid,
        esttime="2 hours",
        name=available_engineer.name,
        phone=issue_request.phone
    )

    # Insert issue into the database
    db.execute(issues.insert().values(
        issue=issue_request.issue,
        location=issue_request.location,
        phone=issue_request.phone,
        complaintid=response_data.complaintid,
        esttime=response_data.esttime,
        name=response_data.name,
        user_id=issue_request.user_id,
        status="open"
    ))

    # Update engineer availability to offline
    db.execute(update(service_engineers).where(service_engineers.c.id == available_engineer.id).values(availability=False))

    db.commit()
    return response_data

@app.post("/admin_signin")
def admin_signin(user: Admin, db: Session = Depends(get_db)):
    # Dummy admin credentials
    admin_username = "admin"
    admin_password = "adminpass"
    if user.username != admin_username or user.password != admin_password:
        raise HTTPException(status_code=400, detail="Invalid admin credentials")
    return {"code": "success"}

@app.post("/add_engineer")
def add_engineer(engineer: ServiceEngineer, db: Session = Depends(get_db)):
    db.execute(service_engineers.insert().values(name=engineer.name, availability=engineer.availability))
    db.commit()
    return {"code": "success"}

@app.get("/complaint/{user_id}/{complaint_id}")
def get_complaint(user_id: str, complaint_id: str, db: Session = Depends(get_db)):
    # Get complaint details for user_id=nil.str and complaint_id
    if user_id == 'nil':
        stmt = select(issues).where(issues.c.complaintid == complaint_id)
    # Get all complaints for the user_id | complaint_id=nil.str
    else:
        stmt = select(issues).where(issues.c.user_id == user_id)
        complaints = db.execute(stmt).fetchall()
        print(type((complaints)[0]))
        if not complaints:
            raise HTTPException(status_code=404, detail="No complaints found for the user")
        return {'complaints_list' : [tuple(_) for _ in complaints]}
    complaint = db.execute(stmt).first()
    # print(type(complaint))
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found with the complaint_id")
    return {'complaint_list' : tuple(complaint)}

@app.put("/close_complaint/{complaint_id}")
def close_complaint(complaint_id: str, code: str, db: Session = Depends(get_db)):
    stmt = select(issues).where(issues.c.complaintid == complaint_id)
    complaint = db.execute(stmt).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Update complaint status to closed and set payments_receipt code
    db.execute(update(issues).where(issues.c.complaintid == complaint_id).values(status="closed", payments_receipt=code))

    # Update engineer availability to online
    engineer_name = complaint.name
    db.execute(update(service_engineers).where(service_engineers.c.name == engineer_name).values(availability=True))

    db.commit()
    return {"code": "success", "complaint_id": complaint_id, "status": "closed"}

# if __name__ == "__main__":
#     import uvicorn
#     import sys

#     logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#     uvicorn.run(app, host="localhost", port=8000, log_level="info")