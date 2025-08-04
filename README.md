# Professional Calculator

یک ماشین حساب فوق حرفه‌ای پایتون با رابط کاربری گرافیکی و خط فرمان

A comprehensive Python calculator with both GUI and CLI interfaces supporting basic arithmetic, scientific functions, and advanced mathematical operations.

## ویژگی‌ها (Features)

### 🖥️ رابط کاربری گرافیکی (GUI Interface)
- رابط کاربری مدرن و زیبا با tkinter
- دکمه‌های علمی و ریاضی کامل
- نمایش تاریخچه محاسبات
- حافظه ماشین حساب (Memory functions)
- تغییر حالت زاویه (درجه/رادیان)
- پشتیبانی از کیبورد

### 💻 رابط خط فرمان (CLI Interface)
- منوی تعاملی کامل
- ماشین حساب پایه
- ماشین حساب علمی
- ارزیابی عبارات ریاضی
- عملیات حافظه
- مشاهده تاریخچه

### 🧮 عملیات پشتیبانی شده (Supported Operations)

#### عملیات پایه (Basic Operations)
- جمع (+)
- تفریق (-)
- ضرب (×)
- تقسیم (÷)
- توان (^)
- جذر (√)

#### توابع علمی (Scientific Functions)
- توابع مثلثاتی: sin, cos, tan
- توابع مثلثاتی معکوس: asin, acos, atan
- لگاریتم طبیعی (ln)
- لگاریتم مشترک (log)
- فاکتوریل (!)

#### ثابت‌های ریاضی (Mathematical Constants)
- π (پی)
- e (عدد اویلر)

#### عملیات حافظه (Memory Operations)
- ذخیره (MS)
- فراخوانی (MR)
- جمع به حافظه (M+)
- کم از حافظه (M-)
- پاک کردن حافظه (MC)

## نصب و اجرا (Installation & Usage)

### پیش‌نیازها (Prerequisites)
```bash
Python 3.6+ with tkinter support
```

### اجرا (Running the Calculator)

#### رابط گرافیکی (GUI Interface)
```bash
python calculator.py
# یا
python3 calculator.py
# یا
./calculator.py
```

#### رابط خط فرمان (CLI Interface)
```bash
python calculator.py --cli
# یا
python3 calculator.py --cli
```

## نحوه استفاده (How to Use)

### رابط گرافیکی (GUI Usage)
1. اسکریپت را اجرا کنید
2. از دکمه‌ها برای وارد کردن اعداد و عملیات استفاده کنید
3. برای محاسبات علمی از دکمه‌های مربوطه استفاده کنید
4. حالت زاویه را از منوی کشویی تغییر دهید
5. از عملیات حافظه برای ذخیره مقادیر استفاده کنید

### رابط خط فرمان (CLI Usage)
1. از منوی اصلی گزینه مورد نظر را انتخاب کنید
2. دستورالعمل‌های نمایش داده شده را دنبال کنید
3. برای بازگشت به منوی اصلی 'back' تایپ کنید

### مثال‌های محاسبه (Calculation Examples)

#### عبارات ریاضی (Mathematical Expressions)
```
sin(30) + cos(60)
2^3 + sqrt(16)
ln(e) + log(100)
π * 2^2
(5 + 3) * 2
```

#### محاسبات علمی (Scientific Calculations)
```
sin(45)     # sine of 45 degrees
ln(2.718)   # natural logarithm
5!          # factorial of 5
2^10        # 2 to the power of 10
```

## ساختار کد (Code Structure)

```
calculator.py
├── Calculator          # موتور اصلی محاسبات
├── CalculatorGUI       # رابط کاربری گرافیکی
├── CalculatorCLI       # رابط خط فرمان
└── main()             # تابع اصلی
```

### کلاس‌ها (Classes)

#### `Calculator`
موتور اصلی محاسبات که شامل تمام توابع ریاضی و علمی است.

#### `CalculatorGUI`
رابط کاربری گرافیکی با استفاده از tkinter که شامل:
- نمایشگر اصلی
- دکمه‌های عملیاتی
- تاریخچه محاسبات
- تنظیمات حالت زاویه

#### `CalculatorCLI`
رابط خط فرمان تعاملی با منوهای مختلف.

## ویژگی‌های امنیتی (Security Features)

- ارزیابی امن عبارات با `eval()` محدود
- جلوگیری از اجرای کدهای مخرب
- کنترل ورودی و validation

## خطاها و استثناها (Error Handling)

- تقسیم بر صفر
- جذر اعداد منفی
- ورودی‌های نامعتبر
- خطاهای overflow

## توسعه‌دهندگان (Contributing)

برای کمک به توسعه این پروژه:
1. Repository را fork کنید
2. تغییرات خود را اعمال کنید
3. Pull request ارسال کنید

## لایسنس (License)

این پروژه تحت لایسنس MIT منتشر شده است.

## تماس (Contact)

برای گزارش باگ یا پیشنهادات، لطفاً issue جدید ایجاد کنید.

---

**ماشین حساب حرفه‌ای - ابزاری قدرتمند برای محاسبات روزانه و علمی**
