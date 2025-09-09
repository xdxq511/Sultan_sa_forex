# VIP 1M Bot (Telegram + TradingView Webhook)

يطلع لك رسائل نفس الصورة:
```
VIP 1M-BOT GROUP
EURGBP | M1 | 03:37 | PUT ⬇️
#QUOTEX

VIP 1M-BOT GROUP
- WIN ✅
```

## A) تيلجرام — إنشاء بوت وجلب `chat_id`
1) افتح Telegram وروح لـ **@BotFather**.
2) أرسل `/newbot` واختر اسم وصيغة يوزر (ينتهي بـ `bot`). بيعطيك **BOT_TOKEN**.
3) سوِّ قناة أو قروب وخذ رابطها.
4) ضيف البوت كـ **Admin** في القناة/القروب.
5) للحصول على **chat_id**:
   - أسهل طريقة: استخدم بوت **@RawDataBot** داخل القناة/القروب، وارسل أي رسالة. بيعطيك `chat_id`.
   - أو استعمل: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates` لو القناة عامة وتكفيك رسائل خاصة.

## B) تجربة سريعة محليًا (إرسال يدوي)
1) ثبّت بايثون 3.10+.
2) صدّر المتغيرات:
   - على macOS/Linux:
     ```bash
     export BOT_TOKEN=ضع_توكنك
     export CHAT_ID=ضع_الشات_آي_دي
     ```
   - على Windows PowerShell:
     ```powershell
     setx BOT_TOKEN "ضع_توكنك"
     setx CHAT_ID "ضع_الشات_آي_دي"
     $env:BOT_TOKEN = "ضع_توكنك"
     $env:CHAT_ID = "ضع_الشات_آي_دي"
     ```
3) شغّل:
   ```bash
   python3 send_signal.py
   ```
بيوصلتك رسالتين (إشارة + WIN) في القناة.

## C) ربط TradingView (Webhook)
### 1) ارفع الـ API (FastAPI) على استضافة
- منصّات سهلة: **Render** أو **Railway**.
- ارفع الملفات: `app.py`, `requirements.txt`.
- أمر التشغيل (Start Command):
  ```bash
  uvicorn app:app --host 0.0.0.0 --port $PORT
  ```
- أضف Environment Variables:
  - `BOT_TOKEN`: توكن بوت تيلجرام.
  - `CHAT_ID`: رقم القناة/القروب.
  - `SECRET_TOKEN`: كلمة سر مشتركة مع TradingView.

### 2) أضف سكربت Pine في TradingView
افتح TradingView → Pine Editor → لصق السكربت (vip_rsi.pine) → Save → Add to chart.

### 3) أنشئ Alert
- من الشارت: **Add Alert** على شروط السكربت (CALL / PUT).
- اختر **Webhook URL**: رابط خادمك مثل `https://YOUR-APP.onrender.com/hook`
- في الـ Message ما تحتاج شيء؛ السكربت يرسل JSON جاهز تلقائيًا.

### 4) جرّب
- لمّا يطلع تنبيه، يوصل Webhook → خادمك → يرسل رسالة للقناة بالتنسيق المطلوب.

## ملفات المشروع
- `send_signal.py`: إرسال يدوي (إشارة/نتيجة).
- `app.py`: نقطة Webhook (FastAPI) تترجم أي JSON لإشارة تيلجرام.
- `requirements.txt`: المتطلبات.

> ملاحظة: لو تبي حساب نتيجة WIN/LOSS تلقائي، تحتاج ربط API للأسعار وتوقيت دقيقة بعد الإشارة — غير مضمّن هنا.

بالتوفيق.
