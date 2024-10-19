import logging
import uuid
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, users, issues, service_engineers, otp
from sqlalchemy import select, update
# import test 
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import mail
import datetime
from datetime import timedelta


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

# User model for signin
class UserSignIn(BaseModel):
    username: str
    password: str

# Request model for the new endpoint
class IssueRequest(BaseModel):
    issue: str
    location: str
    phone: str
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


@app.post("/login")
def login_or_signup(email: str, db: Session = Depends(get_db)):
    '''``log-in``'''
    # Check if email already exists
    stmt = select(users).where(users.c.email == email)
    existing_user = db.execute(stmt).first()
    if existing_user:
        # send the otp to the email
        otp_ = mail.generate_otp()
        # add the otp to the database
        db.execute(update(otp).where(otp.c.user_id == existing_user.user_id).values(otp=otp_[0], UTC=otp_[1]))
        db.commit()
        mail.send_mail(otp_[0], email=email, name=existing_user.username)
        return {"code": "exists-check-email", "user_id": existing_user.user_id}
    else:
        return {"code": "not_exist"}
    
@app.post("/verify_otp")
def verify_otp(user_id: str, otp_: int, db: Session = Depends(get_db)):
    # Check if user exists
    stmt = select(otp).where(otp.c.user_id == user_id)
    existing_otp = db.execute(stmt).first()
    # print(existing_otp)
    if not existing_otp:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    if existing_otp.otp == otp_:
        # Check if the OTP is within the valid time frame (3 minutes)
        otp_creation_time = datetime.datetime.fromisoformat(existing_otp.UTC) #formating str to the datetime object
        current_time = datetime.datetime.now(datetime.UTC)
        if current_time - otp_creation_time <= timedelta(minutes=5):
            return {"code": "success"}
        else:
            raise HTTPException(status_code=400, detail="OTP expired")
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")

@app.post("/login_or_signup")
def add_user(user: User, db: Session = Depends(get_db)):
    user_id = str(uuid.uuid4())
    # Check if email already exists
    stmt = select(users).where(users.c.email == user.email)
    existing_user = db.execute(stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    db.execute(users.insert().values(user_id=user_id, username=user.username, email=user.email))
    db.commit()
    # send the otp to the email
    # login_or_signup(email=user.email)
    otp_ = mail.generate_otp()
    # add the otp to the database
    db.execute(otp.insert().values(user_id=user_id, otp=otp_[0], UTC=otp_[1]))
    db.commit()
    mail.send_mail(otp_[0], email=user.email, name=user.username)
    return {"code": "check-email", "user_id": user_id}
    # return {"code": "success", "user_id": user_id}


@app.post("/report_issue", response_model=IssueResponse)
async def report_issue(issue_request: IssueRequest, db: Session = Depends(get_db)):
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
    admin_password = "adminPass329"
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
        # print(type((complaints)[0]))
        if not complaints:
            raise HTTPException(status_code=404, detail="No complaints found for the user")
        return {'complaints_list' : [tuple(_) for _ in complaints]}
    complaint = db.execute(stmt).first()
    # print(type(complaint))
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found with the complaint_id")
    return {'complaint_list' : tuple(complaint)}

@app.delete("/close_complaint/{complaint_id}")
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

# func to modify engineer availability | params: engineer_name, availability
@app.put("/update_engineer")
def update_engineer(engineer_name: str, availability: bool, db: Session = Depends(get_db)):
    stmt = select(service_engineers).where(service_engineers.c.name == engineer_name)
    engineer = db.execute(stmt).first()
    if not engineer:
        raise HTTPException(status_code=404, detail="Engineer not found")
    db.execute(update(service_engineers).where(service_engineers.c.name == engineer_name).values(availability=availability))
    db.commit()
    return {"code": "success", "engineer_name": engineer_name, "availability": availability}

# func to get all db data | params: table_name
@app.get("/get_all")
def get_all(table_name: str, db: Session = Depends(get_db)):
    # Get all complaints
    tables = {'users': users, 'issues': issues, 'service_engineers': service_engineers, 'otp': otp}
    if table_name not in tables:
        # print(type(tables[_]))
        return {"data": "Table not found"}
    for _ in tables:
        # print(_)
        if _ == table_name : 
            print((tables[_]))
            break
    try:
        stmt = select(tables[_])
        data = db.execute(stmt).fetchall()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Table not found")  
    # print(data)
    return {"data": 
        [dict(zip(tables[_].columns.keys(), row)) for row in data]
    }

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def get():
    return HTMLResponse(content='llll', status_code=200)

if __name__ == "__main__":
    import uvicorn
    import sys
    
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    uvicorn.run(app, host="localhost", port=8000, log_level="info")