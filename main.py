
"""
API Documentation for Service App
Endpoints:
----------
1. **POST /login**
    - Description: Log in or sign up a user by email.
    - Parameters:
      - email (str): The email of the user.
    - Responses:
      - 200: {"code": "exists-check-email", "user_id": str} if user exists.
      - 200: {"code": "not_exist"} if user does not exist.
    - Example using requests:
      ```python
      response = requests.post("http://localhost:8000/login", params={"email": "user@example.com"})
      print(response.json())
      ```
2. **POST /verify_otp**
    - Description: Verify the OTP for a user.
    - Parameters:
      - user_id (str): The ID of the user.
      - otp_ (int): The OTP to verify.
    - Responses:
      - 200: {"code": "success"} if OTP is valid.
      - 400: {"detail": "Invalid user_id"} if user ID is invalid.
      - 400: {"detail": "OTP expired"} if OTP is expired.
      - 400: {"detail": "Invalid OTP"} if OTP is invalid.
    - Example using requests:
      ```python
      response = requests.post("http://localhost:8000/verify_otp", params={"user_id": "user_id", "otp_": 123456})
      print(response.json())
      ```
3. **POST /login_or_signup**
    - Description: Add a new user.
    - Parameters:
      - user (User): The user details (username, email).
    - Responses:
      - 200: {"code": "check-email", "user_id": str} if user is added successfully.
      - 400: {"detail": "Email already exists"} if email already exists.
    - Example using requests:
      ```python
      response = requests.post("http://localhost:8000/login_or_signup", json={"username": "user", "email": "user@example.com"})
      print(response.json())
      ```
4. **POST /report_issue**
    - Description: Report a new issue.
    - Parameters:
      - issue_request (IssueRequest): The issue details (issue, location, phone, user_id).
    - Responses:
      - 200: IssueResponse: The response with complaint details.
      - 400: {"detail": "Invalid user_id"} if user ID is invalid.
      - 400: {"detail": "No available service engineers"} if no engineers are available.
    - Example using requests:
      ```python
      response = requests.post("http://localhost:8000/report_issue", json={"issue": "issue", "location": "location", "phone": "1234567890", "user_id": "user_id"})
      print(response.json())
      ```
5. **POST /admin_signin**
    - Description: Sign in as an admin.
    - Parameters:
      - user (Admin): The admin credentials (username, password).
    - Responses:
      - 200: {"code": "success"} if credentials are valid.
      - 400: {"detail": "Invalid admin credentials"} if credentials are invalid.
    - Example using requests:
      ```python
      response = requests.post("http://localhost:8000/admin_signin", json={"username": "admin", "password": "adminPass329"})
      print(response.json())
      ```
6. **POST /add_engineer**
    - Description: Add a new service engineer.
    - Parameters:
      - engineer (ServiceEngineer): The engineer details (name, availability).
    - Responses:
      - 200: {"code": "success"} if engineer is added successfully.
    - Example using requests:
      ```python
      response = requests.post("http://localhost:8000/add_engineer", json={"name": "engineer_name", "availability": True})
      print(response.json())
      ```
7. **GET /complaint/{user_id}/{complaint_id}**
    - Description: Get complaint details.
    - Parameters:
      - user_id (str): The ID of the user.
      - complaint_id (str): The ID of the complaint.
    - Responses:
      - 200: {'complaints_list': list} if user_id is provided.
      - 200: {'complaint_list': tuple} if complaint_id is provided.
      - 404: {"detail": "No complaints found for the user"} if no complaints are found.
      - 404: {"detail": "Complaint not found with the complaint_id"} if complaint is not found.
    - Example using requests:
      ```python
      response = requests.get("http://localhost:8000/complaint/user_id/complaint_id")
      print(response.json())
      ```
8. **DELETE /close_complaint/{complaint_id}**
    - Description: Close a complaint.
    - Parameters:
      - complaint_id (str): The ID of the complaint.
      - code (str): The payment receipt code.
    - Responses:
      - 200: {"code": "success", "complaint_id": str, "status": "closed"} if complaint is closed successfully.
      - 404: {"detail": "Complaint not found"} if complaint is not found.
    - Example using requests:
      ```python
      response = requests.delete("http://localhost:8000/close_complaint/complaint_id", params={"code": "receipt_code"})
      print(response.json())
      ```
9. **PUT /update_engineer**
    - Description: Update engineer availability.
    - Parameters:
      - engineer_name (str): The name of the engineer.
      - availability (bool): The availability status.
    - Responses:
      - 200: {"code": "success", "engineer_name": str, "availability": bool} if update is successful.
      - 404: {"detail": "Engineer not found"} if engineer is not found.
    - Example using requests:
      ```python
      response = requests.put("http://localhost:8000/update_engineer", params={"engineer_name": "engineer_name", "availability": True})
      print(response.json())
      ```
10. **GET /get_all**
     - Description: Get all data from a table.
     - Parameters:
        - table_name (str): The name of the table.
     - Responses:
        - 200: {"data": list} if data is retrieved successfully.
        - 404: {"detail": "Table not found"} if table is not found.
     - Example using requests:
      ```python
      response = requests.get("http://localhost:8000/get_all", params={"table_name": "users"})
      print(response.json())
      ```
11. **WebSocket /ws**
     - Description: WebSocket endpoint for real-time communication.
     - Messages:
        - Receives and broadcasts messages to all connected clients.
     - Example using websockets:
      ```python

      async def communicate():
          uri = "ws://localhost:8000/ws"
          async with websockets.connect(uri) as websocket:
              await websocket.send("Hello, world!")
              response = await websocket.recv()
              print(response)

      asyncio.run(communicate())
      ```
12. **GET /**
     - Description: Root endpoint.
     - Responses:
        - 200: HTML response with content 'llll'.
     - Example using requests:
      ```python
      response = requests.get("http://localhost:8000/")
      print(response.text)
      ```
13. **DELETE /delete_engineer**
    - Description: Delete an engineer from the database.
    - Parameters:
        - engineer_name (str): The name of the engineer to be deleted.
    - Responses:
        - 200: {"code": "success", "engineer_name": str, "status": "deleted"} if deletion is successful.
        - 404: {"detail": "Engineer not found"} if engineer is not found.
    - Example using requests:
        ```python
        response = requests.delete("http://localhost:8000/delete_engineer", params={"engineer_name": "engineer_name"})
        print(response.json())
        ```
"""
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

# delete engineer   
@app.delete("/delete_engineer")
def delete_engineer(engineer_name: str, db: Session = Depends(get_db)):
    stmt = select(service_engineers).where(service_engineers.c.name == engineer_name)
    engineer = db.execute(stmt).first()
    if not engineer:
        raise HTTPException(status_code=404, detail="Engineer not found")
    db.execute(service_engineers.delete().where(service_engineers.c.name == engineer_name))
    db.commit()
    return {"code": "success", "engineer_name": engineer_name, "status": "deleted"}

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
    return HTMLResponse(content=open("test.html").read(), status_code=200)

if __name__ == "__main__":
    import uvicorn
    import sys
    
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    uvicorn.run(app, host="localhost", port=8000, log_level="info")

# i