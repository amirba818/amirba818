#!/bin/bash

echo "🔧 نصب ابزارهای بازیابی کیف پول بیت کوین"
echo "========================================="

# بروزرسانی سیستم
echo "📦 بروزرسانی پکیج‌ها..."
sudo apt update

# نصب Python dependencies
echo "🐍 نصب Python libraries..."
pip3 install --upgrade pip

# نصب کتابخانه‌های اصلی
pip3 install mnemonic
pip3 install bip32
pip3 install bitcoinlib
pip3 install pycryptodome
pip3 install hashlib

# نصب BTCRecover (ابزار تخصصی)
echo "🔐 نصب BTCRecover..."
if [ ! -d "btcrecover" ]; then
    git clone https://github.com/gurnec/btcrecover.git
    cd btcrecover
    pip3 install -r requirements.txt
    cd ..
    echo "✅ BTCRecover نصب شد"
else
    echo "✅ BTCRecover قبلاً نصب شده"
fi

# نصب John the Ripper
echo "🔓 نصب John the Ripper..."
if ! command -v john &> /dev/null; then
    sudo apt install -y john
    echo "✅ John the Ripper نصب شد"
else
    echo "✅ John the Ripper قبلاً نصب شده"
fi

# دادن مجوز اجرا به اسکریپت
chmod +x bitcoin_wallet_cracker.py

echo ""
echo "🎉 نصب کامل شد!"
echo ""
echo "📋 دستورات مفید:"
echo "=================="
echo "1. اجرای اسکریپت سفارشی:"
echo "   python3 bitcoin_wallet_cracker.py wallet.dat"
echo ""
echo "2. استفاده از BTCRecover:"
echo "   cd btcrecover"
echo "   python3 btcrecover.py --wallet ../wallet.dat"
echo ""
echo "3. استفاده از John the Ripper:"
echo "   bitcoin2john wallet.dat > wallet.john"
echo "   john --format=bitcoin wallet.john"
echo ""

# نمایش اطلاعات سیستم
echo "💻 اطلاعات سیستم شما:"
echo "======================="
echo "CPU: $(nproc) هسته"
echo "RAM: $(free -h | awk '/^Mem:/ {print $2}')"
echo "نسخه Python: $(python3 --version)"
echo ""