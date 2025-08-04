#!/usr/bin/env python3
"""
Bitcoin Core Wallet Password Cracker - RTX 4090 Optimized
بهینه شده برای: Intel i9-13900K (24 cores) + RTX 4090 + 192GB RAM
Wallet info: hasanzade wallet با 3.00235583 BTC
"""

import hashlib
import itertools
import multiprocessing as mp
import string
import time
import sys
import os
import signal
import subprocess
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import psutil
import numpy as np

# اطلاعات wallet شما
WALLET_HASH = "$bitcoin$64$62633a66c002b04a614c78620cc2b1f37b1bc9c7ed37619d32911f63058dc5d762a4c60d5dffa7972d5b0ecbe307008e84a39a21"
WALLET_NAME = "hasanzade"
BALANCE = "3.00235583 BTC"
SALT = "0d5dffa7972d5b0e"
ENCRYPTED_KEY = "66c002b04a614c78620cc2b1f37b1bc9c7ed37619d32911f63058dc5d762a4c6"

# تنظیمات بهینه‌سازی
CHARSET = string.ascii_lowercase  # a-z
MIN_LENGTH = 7
MAX_LENGTH = 8
CHUNK_SIZE = 1000000  # چانک بزرگ‌تر برای سیستم قدرتمند
PROGRESS_FILE = "hasanzade_wallet_progress.txt"
LOG_FILE = "hasanzade_wallet_log.txt"

# تنظیمات GPU
USE_HASHCAT = True
HASHCAT_WORKLOAD = 4  # nightmare mode برای RTX 4090
GPU_TEMP_LIMIT = 83  # دمای ایمن برای RTX 4090

class RTX4090BitcoinCracker:
    def __init__(self):
        self.wallet_hash = WALLET_HASH
        self.start_time = time.time()
        self.total_tried = 0
        self.cpu_cores = psutil.cpu_count(logical=True)  # 32 threads
        self.physical_cores = psutil.cpu_count(logical=False)  # 24 cores
        
        print(f"🔥 Bitcoin Wallet Cracker - RTX 4090 Edition")
        print(f"=" * 60)
        print(f"💰 Target Wallet: {WALLET_NAME}")
        print(f"💎 Balance: {BALANCE}")
        print(f"🧠 CPU: Intel i9-13900K ({self.physical_cores} cores, {self.cpu_cores} threads)")
        print(f"🚀 GPU: NVIDIA RTX 4090")
        print(f"💾 RAM: 192GB")
        print(f"🎯 Target Hash: {self.wallet_hash}")
        print(f"=" * 60)
        
        self.load_progress()
        self.setup_logging()
    
    def load_progress(self):
        """بارگذاری پیشرفت قبلی"""
        try:
            with open(PROGRESS_FILE, 'r') as f:
                self.start_position = int(f.read().strip())
                print(f"📂 ادامه از موقعیت: {self.start_position:,}")
        except:
            self.start_position = 0
            print(f"🆕 شروع جدید")
    
    def save_progress(self, position):
        """ذخیره پیشرفت"""
        with open(PROGRESS_FILE, 'w') as f:
            f.write(str(position))
    
    def log_message(self, message):
        """لاگ کردن پیام"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
        
        print(message)
    
    def setup_logging(self):
        """راه‌اندازی لاگ"""
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                f.write(f"Bitcoin Wallet Recovery Log - {WALLET_NAME}\n")
                f.write(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target Hash: {WALLET_HASH}\n\n")
    
    def check_gpu_temp(self):
        """بررسی دمای GPU"""
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True)
            temp = int(result.stdout.strip())
            
            if temp > GPU_TEMP_LIMIT:
                self.log_message(f"⚠️  دمای GPU بالا: {temp}°C - متوقف شدن موقت...")
                time.sleep(30)
                return False
            return True
        except:
            return True
    
    def run_hashcat_gpu(self, length):
        """اجرای hashcat با RTX 4090"""
        mask = "?l" * length
        
        hashcat_cmd = [
            'hashcat',
            '-m', '11300',  # Bitcoin mode
            '-a', '3',      # Mask attack
            self.wallet_hash,
            mask,
            f'--increment-min={length}',
            f'--increment-max={length}',
            '-O',           # Optimized kernels
            f'-w', str(HASHCAT_WORKLOAD),  # Workload 4 (nightmare)
            '--force',
            f'--gpu-temp-abort={GPU_TEMP_LIMIT + 2}',
            f'--gpu-temp-retain={GPU_TEMP_LIMIT - 5}',
            '--status',
            '--status-timer=10',
            f'--session=hasanzade_gpu_{length}',
            '--potfile-disable',  # جلوگیری از ذخیره در potfile
            '--quiet'
        ]
        
        # اگر موقعیت شروع دارید
        if self.start_position > 0:
            hashcat_cmd.extend(['--skip', str(self.start_position)])
        
        self.log_message(f"🚀 شروع GPU cracking برای {length} کاراکتر...")
        self.log_message(f"📋 Command: {' '.join(hashcat_cmd)}")
        
        try:
            # اجرای hashcat
            process = subprocess.Popen(
                hashcat_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # مانیتورینگ real-time
            while process.poll() is None:
                # بررسی دمای GPU
                if not self.check_gpu_temp():
                    process.terminate()
                    time.sleep(30)
                    continue
                
                time.sleep(5)
            
            # بررسی نتیجه
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                # رمز پیدا شد!
                self.log_message("🎉 رمز پیدا شد!")
                return self.extract_password_from_hashcat()
            
            return None
            
        except KeyboardInterrupt:
            self.log_message("⏸️  متوقف شد توسط کاربر")
            process.terminate()
            return None
        except Exception as e:
            self.log_message(f"❌ خطا در hashcat: {e}")
            return None
    
    def extract_password_from_hashcat(self):
        """استخراج رمز از نتیجه hashcat"""
        try:
            # بررسی hashcat potfile
            result = subprocess.run(['hashcat', '--show', self.wallet_hash], 
                                  capture_output=True, text=True)
            
            if result.stdout:
                password = result.stdout.split(':')[-1].strip()
                self.log_message(f"🔑 رمز پیدا شده: {password}")
                return password
        except:
            pass
        
        return None
    
    def run_cpu_backup(self, length):
        """CPU backup برای مواقع اضطراری"""
        self.log_message(f"🖥️  فعال‌سازی CPU backup ({self.cpu_cores} threads)")
        
        total_combinations = 26 ** length
        chunk_size = max(CHUNK_SIZE, total_combinations // (self.cpu_cores * 4))
        
        with ProcessPoolExecutor(max_workers=self.cpu_cores) as executor:
            futures = []
            current_pos = self.start_position
            
            while current_pos < total_combinations:
                end_pos = min(current_pos + chunk_size, total_combinations)
                
                future = executor.submit(
                    self.cpu_worker, 
                    current_pos, 
                    end_pos, 
                    length
                )
                futures.append(future)
                current_pos = end_pos
            
            # بررسی نتایج
            for future in futures:
                try:
                    result = future.result(timeout=1)
                    if result:
                        return result
                except:
                    continue
        
        return None
    
    def cpu_worker(self, start, end, length):
        """Worker برای CPU"""
        charset_len = len(CHARSET)
        
        for i in range(start, end):
            password = self.index_to_password(i, length)
            
            if self.verify_password(password):
                return password
            
            # گزارش پیشرفت هر 100K
            if (i - start) % 100000 == 0:
                self.save_progress(i)
        
        return None
    
    def index_to_password(self, index, length):
        """تبدیل index به password"""
        charset_len = len(CHARSET)
        password = ""
        
        for _ in range(length):
            password = CHARSET[index % charset_len] + password
            index //= charset_len
        
        return password
    
    def verify_password(self, password):
        """تست رمز (simplified برای سرعت)"""
        # این بخش باید با کتابخانه bitcoin implement شود
        # فعلاً mock implementation
        return False
    
    def estimate_time_gpu(self, combinations, gpu_speed):
        """تخمین زمان برای GPU"""
        if gpu_speed == 0:
            return "نامشخص"
        
        seconds = combinations / gpu_speed
        
        if seconds < 3600:
            return f"{int(seconds // 60)} دقیقه"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} ساعت"
        else:
            return f"{int(seconds // 86400)} روز"
    
    def run_hybrid_attack(self):
        """حمله ترکیبی GPU + CPU"""
        self.log_message("🚀 شروع حمله ترکیبی...")
        
        for length in range(MIN_LENGTH, MAX_LENGTH + 1):
            total_combinations = 26 ** length
            
            # تخمین سرعت RTX 4090
            estimated_gpu_speed = 2000000 if length <= 8 else 1500000  # H/s
            eta = self.estimate_time_gpu(total_combinations, estimated_gpu_speed)
            
            self.log_message(f"🔢 طول {length}: {total_combinations:,} ترکیب")
            self.log_message(f"⏰ تخمین زمان: {eta}")
            
            # سعی در استفاده از GPU (hashcat)
            if USE_HASHCAT:
                self.log_message("🎮 تلاش GPU (Hashcat)...")
                password = self.run_hashcat_gpu(length)
                
                if password:
                    self.log_message(f"🎉 SUCCESS! Password: {password}")
                    self.cleanup()
                    return password
            
            # Fallback به CPU
            self.log_message("🖥️  Fallback به CPU...")
            password = self.run_cpu_backup(length)
            
            if password:
                self.log_message(f"🎉 SUCCESS! Password: {password}")
                self.cleanup()
                return password
        
        self.log_message("❌ رمز پیدا نشد در محدوده مشخص شده")
        return None
    
    def cleanup(self):
        """پاکسازی فایل‌های موقت"""
        try:
            os.remove(PROGRESS_FILE)
            self.log_message("🧹 فایل‌های موقت پاک شدند")
        except:
            pass
    
    def show_system_info(self):
        """نمایش اطلاعات سیستم"""
        import GPUtil
        
        print(f"\n💻 اطلاعات سیستم:")
        print(f"CPU Usage: {psutil.cpu_percent()}%")
        print(f"Memory Usage: {psutil.virtual_memory().percent}%")
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                print(f"GPU: {gpu.name}")
                print(f"GPU Usage: {gpu.load * 100:.1f}%")
                print(f"GPU Memory: {gpu.memoryUtil * 100:.1f}%")
                print(f"GPU Temp: {gpu.temperature}°C")
        except:
            pass

def main():
    print("🔐 Bitcoin Wallet Password Cracker - RTX 4090 Edition")
    
    # بررسی دسترسی‌ها
    if not os.path.exists('/usr/bin/hashcat') and not os.path.exists('/usr/local/bin/hashcat'):
        print("⚠️  Hashcat not found. نصب کنید:")
        print("sudo apt install hashcat")
        return
    
    cracker = RTX4090BitcoinCracker()
    
    # Signal handler
    def signal_handler(sig, frame):
        cracker.log_message("⏸️  متوقف شدن...")
        cracker.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # نمایش اطلاعات سیستم
    cracker.show_system_info()
    
    # شروع کرک
    result = cracker.run_hybrid_attack()
    
    if result:
        print(f"\n🎉 موفقیت آمیز!")
        print(f"🔑 Password: {result}")
        print(f"💰 Balance: {BALANCE}")
        print(f"🏦 Wallet: {WALLET_NAME}")
    else:
        print(f"\n😔 ناموفق")

if __name__ == "__main__":
    main()