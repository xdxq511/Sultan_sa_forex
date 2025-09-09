import os, time, requests
from fastapi import FastAPI, Request, HTTPException

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
SECRET    = os.environ["SECRET_TOKEN"]  # لازم يطابق اللي بتحطه في TradingView

TG_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = FastAPI()

def send_tg(text):
    requests.post(TG_URL, json={"chat_id": CHAT_ID, "text": text})

@app.get("/")
def root():
    return {"ok": True, "msg": "VIP 1M bot up"}

@app.post("/hook")
async def hook(req: Request):
    data = await req.json()
    if data.get("token") != SECRET:
        raise HTTPException(status_code=403, detail="Bad token")

    pair = data.get("pair","UNKNOWN")
    tf   = data.get("tf","M1")
    side = data.get("side","PUT").upper()  # CALL/PUT
    ts   = int(data.get("ts", time.time()))
    hhmm = time.strftime("%H:%M", time.localtime(ts))
    arrow = "⬆️" if side=="CALL" else "⬇️"
    text = f"VIP 1M-BOT GROUP\n{pair} | {tf} | {hhmm} | {side} {arrow}\n#QUOTEX"
    send_tg(text)
    return {"ok": True}
