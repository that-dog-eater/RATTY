# Install .NET runtime
Write-Output "Installing 9.0 .NET Runtime..."

$DotNetVersion = "9.0.0"
$downloadUrl = "https://builds.dotnet.microsoft.com/dotnet/Sdk/9.0.203/dotnet-sdk-9.0.203-win-x64.exe";
$InstallerPath = "$env:TEMP\dotnet-runtime-$DotNetVersion-win-x64.exe"

Write-Output "Download Url: $downloadUrl" 

Invoke-WebRequest -Uri $downloadUrl -OutFile $InstallerPath
Write-Output "Downloaded In: $InstallerPath"

Start-Process -FilePath $InstallerPath -ArgumentList "/install /quiet /norestart" -Wait
Write-Output "Installed!"

dotnet --list-runtimes

# add persistance here 