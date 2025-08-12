from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(); state={"mode":"paper","kill":False}
class ModeReq(BaseModel): mode: str
@app.get("/status") def status(): return state
@app.post("/mode") def set_mode(req: ModeReq): assert req.mode in ("paper","live"); state["mode"]=req.mode; return state
@app.post("/kill") def kill(): state["kill"]=True; return state
