# ابزارهای بازیابی کیف پول بیت کوین - مقایسه کامل

## 1. BTCRecover (پیشنهاد اول)
### مزایا:
- **تخصصی برای Bitcoin wallets**
- **پشتیبانی از typos و variations**
- **GPU acceleration بهتر**
- **Memory optimization عالی**
- **پشتیبانی از partial passwords**

### نصب و استفاده:
```bash
# نصب
git clone https://github.com/gurnec/btcrecover.git
cd btcrecover
pip3 install -r requirements.txt

# استفاده ساده:
python3 btcrecover.py --wallet wallet.dat --typos 2 --tokenlist tokens.txt

# GPU mode:
python3 btcrecover.py --wallet wallet.dat --tokenlist tokens.txt --enable-gpu --gpu-names 0
```

### تنظیمات پیشرفته:
```bash
# برای 8 کاراکتر lowercase:
python3 btcrecover.py \
    --wallet wallet.dat \
    --passwordlist-case lower \
    --min-password-length 7 \
    --max-password-length 8 \
    --enable-gpu \
    --gpu-names 0 \
    --threads 4
```

## 2. John the Ripper (جان)
### مزایا:
- **سرعت بالا**
- **Rule-based attacks**
- **OpenCL support**

```bash
# تبدیل wallet.dat به john format:
bitcoin2john wallet.dat > wallet.john

# اجرا:
john --format=bitcoin --wordlist=rockyou.txt wallet.john
john --format=bitcoin --incremental=Lower wallet.john

# GPU mode:
john --format=bitcoin-opencl --incremental=Lower wallet.john
```

## 3. پایتون اسکریپت سفارشی (بهترین گزینه)
### چرا بهتره:
- **کنترل کامل روی الگوریتم**
- **بهینه‌سازی برای hardware شما**
- **پشتیبانی از multiprocessing**
- **کم کردن overhead**

```python
# bitcoin_cracker.py
import hashlib
import itertools
import multiprocessing as mp
from bitcoinlib.wallets import Wallet
import string

def crack_password_range(start, end, wallet_path, charset, length):
    """کرک کردن رمز در محدوده مشخص"""
    for i in range(start, end):
        # تولید password از index
        password = index_to_password(i, charset, length)
        
        if test_password(wallet_path, password):
            return password
    return None

def index_to_password(index, charset, length):
    """تبدیل index به password"""
    password = ""
    for _ in range(length):
        password = charset[index % len(charset)] + password
        index //= len(charset)
    return password

def test_password(wallet_path, password):
    """تست کردن password"""
    try:
        wallet = Wallet(wallet_path, password=password)
        return True
    except:
        return False

def main():
    wallet_path = "wallet.dat"
    charset = string.ascii_lowercase  # a-z
    length = 8
    
    total_combinations = len(charset) ** length
    num_processes = mp.cpu_count()
    chunk_size = total_combinations // num_processes
    
    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else total_combinations
        
        p = mp.Process(target=crack_password_range, 
                      args=(start, end, wallet_path, charset, length))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
```

## 4. تنظیمات بهینه Hashcat برای 8 کاراکتر

```bash
# روش 1: تقسیم کار به چند session
hashcat -m 11300 -a 3 wallet_fixed.hash ?l?l?l?l?l?l?l?l \
--increment-min=8 --increment-max=8 \
--session=wallet_8char_1 \
--skip=0 --limit=100000000 \
-O -w 3 --force

# روش 2: استفاده از mask attack تقسیم شده
# a-m در اول:
hashcat -m 11300 -a 3 wallet_fixed.hash -1 abcdefghijklm ?1?l?l?l?l?l?l?l

# n-z در اول:
hashcat -m 11300 -a 3 wallet_fixed.hash -1 nopqrstuvwxyz ?1?l?l?l?l?l?l?l
```

## 5. ابزارهای تخصصی دیگر

### A) Passware Kit (تجاری)
- GUI داره
- سرعت بالا
- ولی پولیه

### B) Wallet Recovery Services
- برخی سرویس‌های آنلاین
- خطرناک (trust issue)

## 6. استراتژی پیشنهادی برای 8 کاراکتر

### مرحله 1: تحلیل احتمالات
```bash
# محاسبه زمان تقریبی:
# 8 کاراکتر lowercase: 26^8 = 208,827,064,576 ترکیب
# با سرعت 86K H/s: حدود 28 روز!
```

### مرحله 2: تقسیم‌بندی هوشمند
```bash
# اگر چیزی یادتونه:
# - حرف اول مشخص؟
# - حروف آخر مشخص؟
# - کلمات common؟

# مثال: اگر با 'a' شروع میشه:
hashcat -m 11300 -a 3 wallet_fixed.hash a?l?l?l?l?l?l?l
```

### مرحله 3: Wordlist + Rules
```bash
# استفاده از کلمات common + تغییرات:
hashcat -m 11300 -a 0 wallet_fixed.hash rockyou.txt -r best64.rule
hashcat -m 11300 -a 0 wallet_fixed.hash common_passwords.txt
```

## 7. نکات مهم برای 8 کاراکتر:

1. **تقسیم کار**: چند ماشین استفاده کنید
2. **Cloud Computing**: AWS/Google Cloud با GPU
3. **Pattern Analysis**: اگر چیزی یادتونه استفاده کنید
4. **Hybrid Attack**: ترکیب wordlist + brute force

## 8. محاسبه زمان و هزینه:

| طول رمز | ترکیبات | زمان (86K H/s) | پیشنهاد |
|---------|----------|----------------|----------|
| 7 کاراکتر | 8.0B | 1 روز | ✅ فعلی |
| 8 کاراکتر | 208B | 28 روز | ⚠️ نیاز به optimization |
| 9 کاراکتر | 5.4T | 2 سال | ❌ غیرعملی |

## نتیجه‌گیری:
1. **فعلاً صبر کنید** تا 7 کاراکتر تموم شه
2. **BTCRecover** رو برای 8 کاراکتر امتحان کنید
3. اگر **pattern** یادتونه، حتماً استفاده کنید
4. **Cloud GPU** در نظر بگیرید

آیا چیزی از pattern رمزتون یادتونه؟