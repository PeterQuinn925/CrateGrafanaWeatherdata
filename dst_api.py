from fastapi import FastAPI

app = FastAPI()

class DST(int):
    value = 1

@app.get("/api/dst")
def dst():
    return {"dst": DST.value} #DST 0 is standard time, DST =1 is Daylight Savings Time

@app.get("/api/setdst/{newDST}")
def read_item(newDST):
   DST.value=newDST
   return {"DST": DST.value}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.0.0.11", port=8000)
