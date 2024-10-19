from fastapi import FastAPI


# Initialize the FastAPI app
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Waste Management App"}
