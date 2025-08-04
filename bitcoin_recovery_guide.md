# راهنمای کامل بازیابی کیف پول بیت کوین

## اطلاعات مورد نیاز بر اساس نوع backup:

### 1️⃣ اگر فایل wallet.dat دارید:

#### اطلاعات لازم:
- ✅ فایل `wallet.dat` اصلی
- ❓ رمز عبور wallet (همین که دنبالشیم!)
- 📅 تاریخ تقریبی ایجاد wallet
- 🧠 هر چیزی که از رمز یادتونه

#### فایل‌های مربوطه:
```
~/.bitcoin/
├── wallet.dat          # فایل اصلی wallet
├── wallet.dat.bak      # backup خودکار
├── database/           # فایل‌های پایگاه داده
└── debug.log          # لاگ‌ها
```

#### مراحل آماده‌سازی:
```bash
# 1. کپی backup از wallet.dat
cp wallet.dat wallet_backup.dat

# 2. تبدیل به hash برای hashcat
bitcoin2john wallet.dat > wallet.hash

# 3. اجرای اسکریپت سفارشی
python3 bitcoin_wallet_cracker.py wallet.dat
```

### 2️⃣ اگر Mnemonic Phrase دارید:

#### اطلاعات لازم:
- ✅ 12/24 کلمه mnemonic
- ❓ Passphrase (BIP39) - اختیاری
- 🏦 آدرس wallet شناخته شده
- 💰 مبلغ تقریبی bitcoin

#### مثال mnemonic:
```
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
```

#### تست mnemonic:
```python
# اسکریپت تست mnemonic
from mnemonic import Mnemonic

mnemo = Mnemonic("english")
words = "کلمات شما اینجا"

if mnemo.check(words):
    print("✅ Mnemonic صحیح است")
    
    # تولید seed با passphrase خالی
    seed = mnemo.to_seed(words, passphrase="")
    print(f"Seed: {seed.hex()}")
else:
    print("❌ Mnemonic نامعتبر")
```

### 3️⃣ اگر Private Key دارید:

#### فرمت‌های مختلف:
```
WIF Format: 5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ
Hex Format: 0x1234567890abcdef...
Mini Key: S6c56bnXQiBjk9mqSYE7ykVQ7NzrRy
```

#### تبدیل و تست:
```python
import bitcoin

# تست private key
privkey = "your_private_key_here"
pubkey = bitcoin.privkey_to_pubkey(privkey)
address = bitcoin.pubkey_to_address(pubkey)
print(f"Address: {address}")
```

### 4️⃣ اگر Paper Wallet دارید:

#### محتویات:
- 🔐 Private Key (QR Code یا متن)
- 📫 Public Address
- 🎨 طراحی تزئینی

#### اسکن QR Code:
```bash
# نصب zbar
sudo apt install zbar-tools

# خواندن QR Code
zbarimg paper_wallet.png
```

## 📋 مراحل کامل بازیابی:

### مرحله 1: شناسایی نوع wallet
```bash
# اجرای اسکریپت تشخیص
python3 -c "
import sys
file_path = sys.argv[1]

if file_path.endswith('.dat'):
    print('🏦 Bitcoin Core Wallet')
elif file_path.endswith('.json'):
    print('📱 Electrum/Mobile Wallet')  
elif file_path.endswith('.txt'):
    print('📝 Text Backup (احتمالاً mnemonic)')
else:
    print('❓ نوع نامشخص')
" your_file.dat
```

### مرحله 2: نصب ابزارها
```bash
# اجرای اسکریپت نصب
./setup_bitcoin_cracker.sh
```

### مرحله 3: انتخاب استراتژی

#### الف) اگر چیزی از رمز یادتونه:
```bash
# استفاده از BTCRecover با tokenlist
cd btcrecover
echo "possible_word1" > tokens.txt
echo "possible_word2" >> tokens.txt
echo "123" >> tokens.txt

python3 btcrecover.py \
    --wallet ../wallet.dat \
    --tokenlist tokens.txt \
    --typos 2
```

#### ب) اگر هیچی یادتون نیست:
```bash
# برای 7-8 کاراکتر lowercase
python3 bitcoin_wallet_cracker.py wallet.dat

# یا با hashcat (سریع‌تر)
hashcat -m 11300 -a 3 wallet.hash ?l?l?l?l?l?l?l?l
```

### مرحله 4: بهینه‌سازی

#### تنظیمات CPU (سیستم شما):
```python
# در bitcoin_wallet_cracker.py
CHARSET = string.ascii_lowercase  # فقط حروف کوچک
# یا
CHARSET = string.ascii_letters + string.digits  # حروف + اعداد
```

#### استفاده از الگوها:
```bash
# اگر با "my" شروع میشه:
python3 -c "
import bitcoin_wallet_cracker
cracker = bitcoin_wallet_cracker.BitcoinWalletCracker('wallet.dat')
# تغییر CHARSET به فقط کلمات با my
"
```

## 🎯 نکات مهم:

### امنیت:
- ✅ همیشه backup از فایل‌ها بگیرید
- ✅ روی سیستم offline کار کنید
- ✅ wallet رو بعد از recovery انتقال دهید

### عملکرد:
- 🔥 CPU شما: 4 هسته Intel Xeon
- 💾 RAM: 15GB (عالی برای parallel processing)
- ⚡ سرعت تقریبی: 5000-15000 H/s روی CPU

### زمان‌بندی:
```
7 کاراکتر: ~8 میلیارد ترکیب = 1-2 روز
8 کاراکتر: ~208 میلیارد ترکیب = 20-40 روز
9 کاراکتر: ~5 تریلیون ترکیب = 1-2 سال
```

## 🚀 دستورات سریع:

```bash
# 1. نصب همه چیز
./setup_bitcoin_cracker.sh

# 2. اجرای کرک سفارشی
python3 bitcoin_wallet_cracker.py wallet.dat

# 3. اجرای BTCRecover
cd btcrecover
python3 btcrecover.py --wallet ../wallet.dat

# 4. اجرای John the Ripper
bitcoin2john wallet.dat > wallet.john
john --format=bitcoin wallet.john

# 5. بازگشت به hashcat بهینه
hashcat -m 11300 -a 3 wallet.hash ?l?l?l?l?l?l?l?l -w 3 -O
```

## ❓ سؤالات کلیدی برای شما:

1. **چه نوع backup دارید؟** (wallet.dat, mnemonic, private key)
2. **چیزی از رمز یادتونه؟** (طول، حروف اول/آخر، کلمات)
3. **تاریخ ایجاد wallet چه موقع بوده؟**
4. **آیا از الگوی خاصی استفاده می‌کردید؟** (نام + عدد، تاریخ، etc.)
5. **چندتا variation ممکنه داشته باشه؟**

🎉 **با این اطلاعات، می‌تونیم بهترین استراتژی رو انتخاب کنیم!**