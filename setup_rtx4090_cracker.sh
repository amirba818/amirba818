#!/bin/bash

echo "🔥 Bitcoin Wallet Cracker Setup - RTX 4090 Edition"
echo "=================================================="
echo "System: Intel i9-13900K + RTX 4090 + 192GB RAM"
echo "Target: hasanzade wallet (3.00235583 BTC)"
echo ""

# بررسی privilage
if [[ $EUID -eq 0 ]]; then
   echo "❌ این اسکریپت را با sudo اجرا نکنید"
   exit 1
fi

# بروزرسانی سیستم
echo "📦 بروزرسانی پکیج‌ها..."
sudo apt update && sudo apt upgrade -y

# نصب dependencies اصلی
echo "🔧 نصب dependencies..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    htop \
    nvidia-utils-570 \
    opencl-headers \
    ocl-icd-opencl-dev

# نصب hashcat بهینه
echo "🚀 نصب Hashcat..."
if ! command -v hashcat &> /dev/null; then
    # نصب از source برای بهترین performance
    cd /tmp
    git clone https://github.com/hashcat/hashcat.git
    cd hashcat
    make
    sudo make install
    cd ~
    echo "✅ Hashcat نصب شد"
else
    echo "✅ Hashcat موجود است"
fi

# نصب Python libraries
echo "🐍 نصب Python libraries..."
pip3 install --upgrade pip

# کتابخانه‌های اصلی
pip3 install \
    psutil \
    gputil \
    numpy \
    hashlib \
    pycryptodome \
    bitcoinlib \
    mnemonic \
    bip32 \
    concurrent-futures

# نصب CUDA support (اگر نیاز باشد)
echo "⚡ بررسی CUDA..."
if command -v nvcc &> /dev/null; then
    echo "✅ CUDA موجود است"
    nvcc --version
else
    echo "⚠️  CUDA پیدا نشد - ممکن است نیاز به نصب باشد"
fi

# تنظیم GPU settings
echo "🎮 تنظیم GPU..."
# Enable persistence mode
sudo nvidia-smi -pm 1

# Set power limit to maximum
sudo nvidia-smi -pl 450  # RTX 4090 max power

# Set memory and core clocks (اختیاری)
# sudo nvidia-smi -ac 10501,2700  # Memory,Core MHz

# دادن مجوزها
chmod +x bitcoin_cracker_rtx4090.py
chmod +x hasanzade_wallet.hash

# ایجاد فولدر logs
mkdir -p logs

# تست سیستم
echo ""
echo "🧪 تست سیستم..."
echo "==================="

# CPU info
echo "🧠 CPU:"
lscpu | grep "Model name" | cut -d: -f2 | xargs
echo "Cores: $(nproc)"

# RAM info  
echo "💾 RAM:"
free -h | grep "^Mem:" | awk '{print $2 " total, " $3 " used, " $7 " available"}'

# GPU info
echo "🚀 GPU:"
nvidia-smi --query-gpu=name,memory.total,temperature.gpu --format=csv,noheader

# Hashcat benchmark test
echo ""
echo "🎯 تست Hashcat..."
hashcat -b -m 11300 | head -5

# نمایش دستورات
echo ""
echo "🎉 نصب کامل شد!"
echo "=================="
echo ""
echo "📋 دستورات آماده:"
echo ""
echo "1. اجرای اسکریپت اصلی (پیشنهادی):"
echo "   python3 bitcoin_cracker_rtx4090.py"
echo ""
echo "2. اجرای hashcat مستقیم:"
echo "   hashcat -m 11300 -a 3 hasanzade_wallet.hash ?l?l?l?l?l?l?l -w 4 -O"
echo ""
echo "3. تست 8 کاراکتر:"
echo "   hashcat -m 11300 -a 3 hasanzade_wallet.hash ?l?l?l?l?l?l?l?l -w 4 -O"
echo ""
echo "4. مانیتورینگ GPU:"
echo "   watch -n 1 nvidia-smi"
echo ""

# محاسبه تخمین زمان
echo "⏰ تخمین زمان با RTX 4090:"
echo "============================"

# فرض سرعت 2 میلیون H/s برای RTX 4090
declare -A combinations=(
    [7]=$((26**7))
    [8]=$((26**8))
)

gpu_speed=2000000  # H/s

for length in 7 8; do
    total=${combinations[$length]}
    seconds=$((total / gpu_speed))
    hours=$((seconds / 3600))
    days=$((hours / 24))
    
    echo "طول $length: $(printf "%'d" $total) ترکیب"
    if [ $days -gt 0 ]; then
        echo "  زمان: $days روز، $((hours % 24)) ساعت"
    else
        echo "  زمان: $hours ساعت، $(((seconds % 3600) / 60)) دقیقه"
    fi
done

echo ""
echo "💡 نکات مهم:"
echo "============="
echo "- فن GPU را روی 100% قرار دهید"
echo "- دمای GPU را زیر 83°C نگه دارید"  
echo "- از power limit maximum استفاده کنید"
echo "- حین کرک از سیستم استفاده نکنید"
echo ""
echo "🚀 آماده شروع!"