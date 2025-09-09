from fastapi import FastAPI, Request
import requests, json, time, threading
from urllib.parse import unquote_plus

app = FastAPI()

# ===== إعداداتك =====
BOT_TOKEN    = "8311262296:AAEQ9zBMmYX5OtcTqcvmbOdoJdls6577LK0"
CHAT_ID      = "439982226"          # إذا تبي قناة: غيّرها للـ chat_id اللي يبدأ بـ -100 وخلي البوت أدمن
SECRET_TOKEN = "Ss11223344s"
PRICE_PROVIDER   = "alphavantage"   # استخدم Alpha Vantage
PRICE_API_KEY    = "Q4YI1Z4CUVJRJP7Y"  # مفتاح Alpha Vantage
POLL_SECONDS     = 30               # كل كم ثانية يشيك السعر
# =====================

open_trades = []  # نخزن الصفقات المفتوحة

def send_tg(text: str):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print("TELEGRAM_ERR:", e)

def normalize_symbol(pair: str) -> str:
    """نحوّل الرمز من FX:EURUSD إلى EURUSD"""
    return pair.split(":")[-1].replace("/", "").upper()

def get_price(pair: str) -> float:
    sym = normalize_symbol(pair)
    try:
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={sym[:3]}&to_currency={sym[3:]}&apikey={PRICE_API_KEY}"
        r = requests.get(url, timeout=10).json()
        val = r["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        return float(val)
    except Exception as e:
        print("PRICE_ERR:", e)
    return float("nan")

@app.get("/")
def home():
    return {"ok": True, "msg": "VIP 1M bot up"}

@app.get("/hook-test")
def hook_test():
    send_tg("VIP 1M-BOT GROUP\nTEST ✅ من السيرفر مباشرة")
    return {"ok": True}

@app.post("/hook")
async def hook(request: Request):
    raw = await request.body()
    txt = (raw or b"").decode("utf-8")

    data = None
    try:
        data = json.loads(txt) if txt else None
    except:
        pass
    if not data and txt.startswith("message="):
        try:
            payload = unquote_plus(txt.split("=", 1)[1])
            data = json.loads(payload)
        except:
            pass

    if not data:
        print("HOOK RAW >>>", txt[:300])
        return {"ok": False, "error": "invalid_or_empty_payload"}

    if data.get("token") != SECRET_TOKEN:
        return {"ok": False, "error": "bad_token"}

    # تفاصيل الصفقة من TradingView
    trade = {
        "pair": data.get("pair", "UNKNOWN"),
        "tf":   str(data.get("tf", "1")),
        "side": str(data.get("side", "")).upper(),
        "entry": float(data.get("entry", data.get("price", 0))),
        "tp":    float(data.get("tp", 0)),
        "sl":    float(data.get("sl", 0)),
        "open_ts": time.time(),
        "status": "OPEN"
    }
    open_trades.append(trade)

    arrow = "⬆️" if trade["side"] == "BUY" else "⬇️"
    msg = (
        "VIP 1M-BOT GROUP\n"
        f"{trade['pair'].split(':')[-1]} | {trade['tf']} | {trade['side']} {arrow}\n"
        f"Entry: {trade['entry']}\n"
        f"TP: {trade['tp']} | SL: {trade['sl']}\n"
        "#QUOTEX"
    )
    send_tg(msg)
    return {"ok": True, "stored": True}

# --- مراقبة الصفقات ---
def monitor_trades():
    while True:
        try:
            for trade in list(open_trades):
                if trade["status"] != "OPEN":
                    continue
                price = get_price(trade["pair"])
                if price != price:  # NaN
                    continue

                side = trade["side"]
                tp   = trade["tp"]
                sl   = trade["sl"]

                # تحقق TP/SL
                hit_win = (side == "BUY"  and price >= tp) or (side == "SELL" and price <= tp)
                hit_loss= (side == "BUY"  and price <= sl) or (side == "SELL" and price >= sl)

                if hit_win:
                    trade["status"] = "WIN"
                    send_tg(f"✅ WIN\n{trade['pair'].split(':')[-1]} | {trade['tf']} | {side}\nHit TP @ {tp}")
                elif hit_loss:
                    trade["status"] = "LOSS"
                    send_tg(f"❌ LOSS\n{trade['pair'].split(':')[-1]} | {trade['tf']} | {side}\nHit SL @ {sl}")

                if trade["status"] in ("WIN", "LOSS"):
                    open_trades.remove(trade)
        except Exception as e:
            print("MONITOR_ERR:", e)

        time.sleep(POLL_SECONDS)

# شغل المراقبة بخيط مستقل
threading.Thread(target=monitor_trades, daemon=True).start()
