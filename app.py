from fastapi import FastAPI, Request
import requests

app = FastAPI()

BOT_TOKEN = "توكن_البوت_اللي عطاك BotFather"
CHAT_ID = "معرّف القناة (chat_id)"  # لازم البوت يكون أدمن بالقناة
SECRET_TOKEN = "Ss11223344s"  # نفس اللي بالكود في TradingView

def send_tg(msg: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

@app.get("/")
def home():
    return {"ok": True, "msg": "VIP 1M bot up"}

@app.post("/hook")
async def hook(request: Request):
    data = await request.json()
    if data.get("token") != SECRET_TOKEN:
        return {"ok": False, "error": "Invalid token"}
    
    # نص الرسالة اللي يوصل التليجرام
    text = f"VIP 1M-BOT GROUP\n{data['pair']} | {data['tf']} | {data['side']} ⬆️⬇️\nPrice: {data['price']}"
    send_tg(text)
    return {"ok": True, "forwarded": True}

# مسار اختبار يدوي
@app.get("/hook-test")
def hook_test():
    test_data = {
        "pair": "EURUSD",
        "tf": "1",
        "side": "CALL",
        "price": "1.1770"
    }
    text = f"VIP 1M-BOT GROUP\n{test_data['pair']} | {test_data['tf']} | {test_data['side']} ⬆️\nPrice: {test_data['price']}"
    send_tg(text)
    return {"ok": True, "msg": "Test message sent to Telegram"}
