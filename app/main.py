from fastapi import FastAPI, Request


app = FastAPI()


@app.get("/")
async def root(request: Request):
    print(request.__dict__)
    return {"message": "Hello World"}
