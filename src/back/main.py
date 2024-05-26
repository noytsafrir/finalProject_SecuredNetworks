from fastapi import FastAPI, HTTPException, Request
from starlette import status

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/login")
async def login(request: Request):
    payload = await request.json()
    #TODO: change the email and password in the data base
    if payload.get("email") == "abc123@gmail.com" and payload.get("password") == "123456":
        return {"message": "Successfully logged in!"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The email or password is incorrect or does not exist"
    )


@app.post("/register")
async def login(request: Request):
    payload = await request.json()
    #TODO: change the email and password in the data base
    if payload.get("email") == "abc123@gmail.com" and payload.get("password") == "123456":
        return {"message": "Successfully logged in!"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The email or password is incorrect or does not exist"
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app" , host="127.0.0.1", port=8001, reload=True)
    