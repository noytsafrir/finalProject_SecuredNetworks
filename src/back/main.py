# src/back/main.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the frontend

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(f'Got email: {email}\nGot password: {password}')
    
    # Add your login logic here, for example:
    if email == 'user@example.com' and password == 'password123':
        return jsonify({"message": "Login successful", "status": "success"}), 200
    else:
        return jsonify({"message": "Invalid credentials", "status": "error"}), 401

if __name__ == '__main__':
    app.run(debug=True)


# from fastapi import FastAPI, HTTPException, Request
# from starlette import status

# app = FastAPI()

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



# if _name_ == "_main_":
#     import uvicorn
#     uvicorn.run("main:app" , host="127.0.0.1", port=8001, reload=True)