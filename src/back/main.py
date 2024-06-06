from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
# from starlette import status

app = FastAPI()

# Dummy database for demonstration
users = {
    "test@example.com": {"password": "hashed_password", "otp": "123456"}
}

# Allow CORS for your frontend
origins = [
    "http://localhost:8001",  # Adjust according to your frontend server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# @app.post("/login")
# async def login(request: Request):
#     payload = await request.json()
#     #TODO: change the email and password in the data base
#     if payload.get("email") == "abc123@gmail.com" and payload.get("password") == "123456":
#         return {"message": "Successfully logged in!"}
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="The email or password is incorrect or does not exist"
#     )


@app.get("/login")
async def login(email: str, password: str):
    user = users.get(email)
    if user and user["password"] == password:  # Simulating password check
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/forgotpassword")
async def forgot_password(email: str):
    if email in users:
        # Here, send OTP to the user's email
        return {"status": "success", "message": "OTP sent to email"}
    else:
        raise HTTPException(status_code=404, detail="Email not found")

@app.get("/otpcheck")
async def otp_check(email: str, otp: str):
    if users.get(email) and users[email]['otp'] == otp:
        return {"status": "success", "message": "OTP valid"}
    else:
        raise HTTPException(status_code=401, detail="Invalid OTP")

@app.post("/newpassword")
async def new_password(email: str, new_password: str):
    if email in users:
        users[email]['password'] = new_password  # Simulating password update
        return {"status": "success", "message": "Password updated"}
    else:
        raise HTTPException(status_code=404, detail="Email not found")

@app.post("/register")
async def register(email: str, password: str):
    if email not in users:
        users[email] = {"password": password}
        return {"status": "success", "message": "User registered"}
    else:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/addcustomer")
async def add_customer(customer_name: str, company_name: str, address: str):
    if customer_name and company_name and address:
        # Add customer logic here
        return {"status": "success", "customer_name": customer_name}
    else:
        raise HTTPException(status_code=400, detail="Missing information")

@app.post("/changepassword")
async def change_password(email: str, current_password: str, new_password: str):
    user = users.get(email)
    if user and user["password"] == current_password:
        users[email]['password'] = new_password  # Simulating password change
        return {"status": "success", "message": "Password changed"}
    else:
        raise HTTPException(status_code=401, detail="Invalid current password")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)




# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# @app.post("/login")
# async def login(request: Request):
#     payload = await request.json()
#     #TODO: change the email and password in the data base
#     if payload.get("email") == "abc123@gmail.com" and payload.get("password") == "123456":
#         return {"message": "Successfully logged in!"}
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="The email or password is incorrect or does not exist"
#     )


# @app.post("/register")
# async def login(request: Request):
#     payload = await request.json()
#     #TODO: change the email and password in the data base
#     if payload.get("email") == "abc123@gmail.com" and payload.get("password") == "123456":
#         return {"message": "Successfully logged in!"}
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="The email or password is incorrect or does not exist"
#     )


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app" , host="127.0.0.1", port=8001, reload=True)
    