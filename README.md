# ReverseShell

Dropper --> Payload --> <- C2


## Setup

### Dropper:
  Need to add 2 links, the first to the pdf that will be loaded at runtime and the other will be to downlaod the Exe and execute. Dropper will be sent on its own to the target so it must be the file zipped with a password.
  
### Payload:
  This payload is in C# so it must be built using dotnet command that keeps it as a standalone binary with no Dll's attached - command for compiling will be shown under these instructions, the shell.cs is the paylaod and will need to have the VPS servers IP added to the file. The Payload Exe after compiling will be uploaded to a github and downloaded by the dropper. 
    
  - dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true /p:IncludeNativeLibrariesForSelfExtract=true

### C2: 
  The C2 must run a on VPS server and needs to run in the background. Open ports for the Reverse shell to access the C2 server.


## Final

Have the Exe payload and the PDF on a github repo make sure the dropper is connected and the paylaod is configered to connect back to the C2 VPS server correctly. 
1. VPS running
2. Zip Dropper + Password Protected
  - Ctrl + shift + rigth click -> 7zip hover -> add to archive -> create password = zip with password
3. Send to Target!


###Cons 
- no obfuscation
- no loader
- not a certified script = smart screen pop-up
- no persistance
