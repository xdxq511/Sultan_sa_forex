from fastapi import FastAPI, Request
import requests, json
from urllib.parse import unquote_plus

app = FastAPI()

# ====== إعدادات تليجرام (مُدخلة حسب طلبك) ======
BOT_TOKEN = "8311262296:AAEQ9zBMmYX5OtcTqcvmbOdoJdls6577LK0"
CHAT_ID   = "439982226"   # هذا يبدو ID محادثة خاصة (مو قناة). لازم تبدأ محادثة مع البوت في تيليجرام /start
SECRET_TOKEN = "Ss11223344s"  # لازم يطابق اللي في Pine Script
# ===============================================

def send_tg(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

@app.get("/")
def home():
    return {"ok": True, "msg": "VIP 1M bot up"}

@app.post("/hook")
async def hook(request: Request):
    raw = await request.body()
    txt = (raw or b"").decode("utf-8")

    data = None
    if txt:
        try:
            # JSON مباشر
            data = json.loads(txt)
        except Exception:
            # message=<json>
            if txt.startswith("message="):
                try:
                    payload = unquote_plus(txt.split("=", 1)[1])
                    data = json.loads(payload)
                except Exception:
                    pass

    if not data:
        print("HOOK RAW >>>", txt[:500])  # يساعدنا بالتشخيص في الـ Logs
        return {"ok": False, "error": "invalid_or_empty_payload", "preview": txt[:120]}

    if data.get("token") != SECRET_TOKEN:
        return {"ok": False, "error": "bad_token"}

    pair  = str(data.get("pair", "UNKNOWN")).split(":")[-1]
    tf    = str(data.get("tf", "M1"))
    side  = str(data.get("side", "PUT")).upper()
    price = data.get("price")
    arrow = "⬆️" if side == "CALL" else "⬇️"

    text = f"VIP 1M-BOT GROUP\n{pair} | {tf} | {side} {arrow}\nPrice: {price}\n#QUOTEX"
    send_tg(text)
    return {"ok": True, "forwarded": True}

# اختبار سريع يرسل لك رسالة مباشرة
@app.get("/hook-test")
def hook_test():
    text = "VIP 1M-BOT GROUP\nTEST ✅ من السيرفر مباشرة"
    send_tg(text)
    return {"ok": True, "msg": "Test message sent to Telegram"}
