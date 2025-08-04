#!/usr/bin/env python3
"""
Bitcoin Core Wallet Password Cracker
بهینه شده برای سیستم شما: Intel Xeon 4 cores, 15GB RAM
"""

import itertools
import multiprocessing as mp
import string
import time
import sys
import hashlib
import struct
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import signal

# تنظیمات کلی
CHARSET = string.ascii_lowercase  # a-z
MIN_LENGTH = 7
MAX_LENGTH = 8
CHUNK_SIZE = 100000  # تعداد رمزهای هر chunk
SAVE_PROGRESS_EVERY = 1000000  # ذخیره پیشرفت هر میلیون رمز
PROGRESS_FILE = "wallet_crack_progress.txt"

class BitcoinWalletCracker:
    def __init__(self, wallet_file, backup_file=None):
        self.wallet_file = wallet_file
        self.backup_file = backup_file
        self.start_time = time.time()
        self.total_tried = 0
        
        # تشخیص نوع فایل
        if wallet_file.endswith('.dat'):
            self.wallet_type = 'core'
        elif backup_file and backup_file.endswith('.txt'):
            self.wallet_type = 'mnemonic'
        else:
            self.wallet_type = 'unknown'
            
        print(f"🔍 نوع کیف پول تشخیص داده شده: {self.wallet_type}")
        
        # بارگذاری پیشرفت قبلی
        self.load_progress()
    
    def load_progress(self):
        """بارگذاری پیشرفت از فایل"""
        try:
            with open(PROGRESS_FILE, 'r') as f:
                self.start_position = int(f.read().strip())
                print(f"📂 ادامه از موقعیت: {self.start_position:,}")
        except:
            self.start_position = 0
            print("🆕 شروع جدید")
    
    def save_progress(self, position):
        """ذخیره پیشرفت"""
        with open(PROGRESS_FILE, 'w') as f:
            f.write(str(position))
    
    def index_to_password(self, index, length):
        """تبدیل index به password"""
        charset_len = len(CHARSET)
        password = ""
        
        for _ in range(length):
            password = CHARSET[index % charset_len] + password
            index //= charset_len
            
        return password
    
    def test_bitcoin_core_wallet(self, password):
        """تست رمز برای Bitcoin Core wallet.dat"""
        try:
            # این قسمت نیاز به bitcoin library داره
            # فعلاً mock implementation
            # شما باید wallet.dat رو به hash تبدیل کرده باشید
            
            # اگر hashcat hash دارید:
            if hasattr(self, 'wallet_hash'):
                return self.verify_hash(password)
            
            # در غیر این صورت direct wallet test
            return self.test_wallet_direct(password)
            
        except Exception as e:
            return False
    
    def test_mnemonic_wallet(self, password):
        """تست رمز برای mnemonic backup"""
        try:
            from mnemonic import Mnemonic
            from bip32 import BIP32
            
            # خواندن mnemonic از backup file
            with open(self.backup_file, 'r') as f:
                mnemonic_words = f.read().strip()
            
            # تست با password
            mnemo = Mnemonic("english")
            if mnemo.check(mnemonic_words):
                # تست passphrase
                seed = mnemo.to_seed(mnemonic_words, passphrase=password)
                # اگر wallet address مشخصی دارید، اینجا چک کنید
                return True
                
        except Exception as e:
            return False
    
    def test_wallet_direct(self, password):
        """تست مستقیم wallet (نیاز به bitcoin-python)"""
        try:
            # این قسمت نیاز به نصب bitcoin library داره
            # pip install bitcoin-python
            import bitcoin
            
            # اینجا کد تست مستقیم wallet
            # این قسمت بستگی به نوع wallet دارد
            
            return False  # موقت
        except:
            return False
    
    def verify_hash(self, password):
        """تست رمز با hash (اگر از hashcat استفاده کردید)"""
        # اگر hash از hashcat دارید، اینجا verify کنید
        # مثال برای Bitcoin hash:
        try:
            # کد hash verification
            pass
        except:
            return False
    
    def worker_process(self, start_idx, end_idx, length, result_queue):
        """فرآیند worker برای تست رمزها"""
        passwords_tested = 0
        
        for i in range(start_idx, end_idx):
            password = self.index_to_password(i, length)
            passwords_tested += 1
            
            # تست رمز بر اساس نوع wallet
            if self.wallet_type == 'core':
                if self.test_bitcoin_core_wallet(password):
                    result_queue.put(('found', password, i))
                    return
            elif self.wallet_type == 'mnemonic':
                if self.test_mnemonic_wallet(password):
                    result_queue.put(('found', password, i))
                    return
            
            # گزارش پیشرفت
            if passwords_tested % 10000 == 0:
                result_queue.put(('progress', passwords_tested, i))
        
        result_queue.put(('done', passwords_tested, end_idx))
    
    def calculate_total_combinations(self, length):
        """محاسبه تعداد کل ترکیبات"""
        return len(CHARSET) ** length
    
    def estimate_time(self, combinations_left, speed):
        """تخمین زمان باقی مانده"""
        if speed == 0:
            return "نامشخص"
        
        seconds_left = combinations_left / speed
        hours = int(seconds_left // 3600)
        minutes = int((seconds_left % 3600) // 60)
        
        if hours > 24:
            days = hours // 24
            hours = hours % 24
            return f"{days} روز، {hours} ساعت"
        else:
            return f"{hours} ساعت، {minutes} دقیقه"
    
    def crack_passwords(self):
        """شروع فرآیند کرک"""
        print(f"🚀 شروع کرک با {mp.cpu_count()} هسته CPU")
        print(f"📁 فایل wallet: {self.wallet_file}")
        if self.backup_file:
            print(f"📁 فایل backup: {self.backup_file}")
        
        for length in range(MIN_LENGTH, MAX_LENGTH + 1):
            total_combinations = self.calculate_total_combinations(length)
            print(f"\n🔢 تست طول {length}: {total_combinations:,} ترکیب")
            
            if self.crack_length(length, total_combinations):
                return True
        
        print("\n❌ رمز پیدا نشد!")
        return False
    
    def crack_length(self, length, total_combinations):
        """کرک برای طول مشخص"""
        start_position = max(self.start_position, 0)
        
        # تقسیم کار بین CPU cores
        num_processes = mp.cpu_count()
        chunk_size = max(CHUNK_SIZE, total_combinations // (num_processes * 100))
        
        manager = mp.Manager()
        result_queue = manager.Queue()
        processes = []
        
        current_position = start_position
        passwords_tested = 0
        last_save_time = time.time()
        
        try:
            while current_position < total_combinations:
                # ایجاد processes
                for i in range(num_processes):
                    if current_position >= total_combinations:
                        break
                    
                    end_pos = min(current_position + chunk_size, total_combinations)
                    
                    p = mp.Process(
                        target=self.worker_process,
                        args=(current_position, end_pos, length, result_queue)
                    )
                    p.start()
                    processes.append(p)
                    
                    current_position = end_pos
                
                # بررسی نتایج
                active_processes = len(processes)
                
                while active_processes > 0:
                    try:
                        result_type, data1, data2 = result_queue.get(timeout=1)
                        
                        if result_type == 'found':
                            password = data1
                            position = data2
                            
                            print(f"\n🎉 رمز پیدا شد: {password}")
                            print(f"📍 موقعیت: {position:,}")
                            
                            # پاک کردن فایل پیشرفت
                            try:
                                os.remove(PROGRESS_FILE)
                            except:
                                pass
                            
                            # خاتمه processes
                            for p in processes:
                                p.terminate()
                            
                            return True
                        
                        elif result_type == 'progress':
                            passwords_tested += data1
                            self.total_tried += data1
                            
                            # نمایش پیشرفت
                            elapsed = time.time() - self.start_time
                            speed = self.total_tried / elapsed if elapsed > 0 else 0
                            progress_percent = (data2 / total_combinations) * 100
                            
                            remaining = total_combinations - data2
                            eta = self.estimate_time(remaining, speed)
                            
                            print(f"\r⚡ سرعت: {speed:.0f} H/s | "
                                  f"پیشرفت: {progress_percent:.2f}% | "
                                  f"تست شده: {self.total_tried:,} | "
                                  f"ETA: {eta}", end="")
                            
                            # ذخیره پیشرفت
                            if time.time() - last_save_time > 60:  # هر دقیقه
                                self.save_progress(data2)
                                last_save_time = time.time()
                        
                        elif result_type == 'done':
                            active_processes -= 1
                            passwords_tested += data1
                    
                    except:
                        continue
                
                # انتظار برای تمام processes
                for p in processes:
                    p.join()
                
                processes.clear()
        
        except KeyboardInterrupt:
            print(f"\n\n⏸️ متوقف شد توسط کاربر")
            print(f"💾 ذخیره پیشرفت در موقعیت: {current_position}")
            self.save_progress(current_position)
            
            for p in processes:
                p.terminate()
            
            return False
        
        return False

def main():
    print("🔐 Bitcoin Wallet Password Cracker")
    print("=" * 50)
    
    # بررسی آرگومان‌ها
    if len(sys.argv) < 2:
        print("❌ استفاده:")
        print("python3 bitcoin_wallet_cracker.py wallet.dat [backup.txt]")
        print("\nمثال:")
        print("python3 bitcoin_wallet_cracker.py wallet.dat")
        print("python3 bitcoin_wallet_cracker.py wallet.dat mnemonic_backup.txt")
        sys.exit(1)
    
    wallet_file = sys.argv[1]
    backup_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # بررسی وجود فایل
    if not os.path.exists(wallet_file):
        print(f"❌ فایل پیدا نشد: {wallet_file}")
        sys.exit(1)
    
    if backup_file and not os.path.exists(backup_file):
        print(f"❌ فایل backup پیدا نشد: {backup_file}")
        sys.exit(1)
    
    # شروع کرک
    cracker = BitcoinWalletCracker(wallet_file, backup_file)
    
    # نصب signal handler برای Ctrl+C
    def signal_handler(sig, frame):
        print("\n\n⏸️ متوقف شدن...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # شروع
    cracker.crack_passwords()

if __name__ == "__main__":
    main()