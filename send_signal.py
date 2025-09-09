import os, requests, datetime as dt

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID   = os.environ.get("CHAT_ID")
API=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_signal(pair, timeframe, side):  # side = "PUT" or "CALL"
    now = dt.datetime.now().strftime("%H:%M")
    arrow = "⬇️" if side.upper()=="PUT" else "⬆️"
    text = f"VIP 1M-BOT GROUP\n{pair} | {timeframe} | {now} | {side.upper()} {arrow}\n#QUOTEX"
    requests.post(API, json={"chat_id": CHAT_ID, "text": text})

def send_result(win=True):
    text = "VIP 1M-BOT GROUP\n- WIN ✅" if win else "VIP 1M-BOT GROUP\n- LOSS ❌"
    requests.post(API, json={"chat_id": CHAT_ID, "text": text})

if __name__ == "__main__":
    # أمثلة تشغيل سريعة للتجربة:
    # export BOT_TOKEN=xxxx ; export CHAT_ID=123456 ; python3 send_signal.py
    send_signal("EURGBP", "M1", "PUT")
    send_result(True)
