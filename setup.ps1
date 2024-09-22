pip install -r requirements.txt

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
$env:SCLAT_PATH = (Get-Location).Path

if ($isAdmin) {
    if ([Environment]::GetEnvironmentVariable("SCLAT_PATH", [EnvironmentVariableTarget]::Machine)) {
        [Environment]::SetEnvironmentVariable("SCLAT_PATH", $null, [EnvironmentVariableTarget]::Machine)
        Write-Host "Deleted existing system environment variable: SCLAT_PATH"
    }

    [Environment]::SetEnvironmentVariable("SCLAT_PATH", $env:SCLAT_PATH, [EnvironmentVariableTarget]::Machine)
    Write-Host "Environment variable is set to system level: SCLAT_PATH = $env:SCLAT_PATH"
} else {
    if ([Environment]::GetEnvironmentVariable("SCLAT_PATH", [EnvironmentVariableTarget]::User)) {
        [Environment]::SetEnvironmentVariable("SCLAT_PATH", $null, [EnvironmentVariableTarget]::User)
        Write-Host "Deleted existing user environment variable: SCLAT_PATH"
    }

    [Environment]::SetEnvironmentVariable("SCLAT_PATH", $env:SCLAT_PATH, [EnvironmentVariableTarget]::User)
    Write-Host "Environment variable is set to user level: SCLAT_PATH = $env:SCLAT_PATH"
}

pause