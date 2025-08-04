# بهینه‌سازی Hashcat برای بازیابی کیف پول بیت کوین

## تنظیمات فعلی شما (خوب):
```bash
hashcat -m 11300 -a 3 wallet_fixed.hash ?l?l?l?l?l?l?l?l \
--increment --increment-min=7 -O -w 2 \
--session=wallet_crack \
--status --status-timer=30 \
-d 1
```

## پیشنهادات بهینه‌سازی:

### 1. تنظیمات workload (-w)
```bash
# فعلی: -w 2 (متعادل)
# پیشنهاد برای سرعت بیشتر:
-w 3  # حداکثر performance
-w 4  # nightmare mode (خطرناک برای سیستم)
```

### 2. بهینه‌سازی GPU
```bash
# اضافه کردن tune برای GPU:
--gpu-temp-abort=85    # متوقف شدن در دمای بالا
--gpu-temp-retain=75   # حفظ دمای ایده‌آل
--force               # اجبار استفاده از optimized kernel
```

### 3. تنظیمات حافظه
```bash
# اگر RAM کافی دارید:
--segment-size=512    # یا 1024
```

### 4. کامند بهینه شده پیشنهادی:
```bash
hashcat -m 11300 -a 3 wallet_fixed.hash ?l?l?l?l?l?l?l?l \
--increment --increment-min=7 -O -w 3 \
--session=wallet_crack_optimized \
--status --status-timer=30 \
--gpu-temp-abort=85 --gpu-temp-retain=75 \
--force \
-d 1
```

### 5. اگر pattern رمز را می‌دانید:
```bash
# مثال: اگر می‌دانید رمز با "my" شروع می‌شود:
?l?l?l?l?l?l?l?l  →  my?l?l?l?l?l?l

# اگر ترکیب حروف و اعداد:
?l?l?l?l?d?d?d?d  # 4 حرف + 4 عدد
```

## نکات مهم:
- **فعلاً صبر کنید!** شما 96% پیش رفتید، احتمالاً تا 1 ساعت دیگه تموم میشه
- دمای GPU (77°C) ایمن هست ولی زیر نظر بگیرید
- اگر رمز پیدا نشد، طول بیشتری امتحان کنید (8-9 کاراکتر)

## بعد از تمام شدن این round:
```bash
# برای 8 کاراکتر:
hashcat -m 11300 -a 3 wallet_fixed.hash ?l?l?l?l?l?l?l?l \
--increment --increment-min=8 --increment-max=8 -O -w 3
```

## Monitor کردن:
```bash
# چک کردن وضعیت:
hashcat --session=wallet_crack --restore

# متوقف کردن موقت:
Ctrl + C (یکبار)

# ادامه دادن:
hashcat --session=wallet_crack --restore
```