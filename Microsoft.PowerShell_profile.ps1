# PowerShell Profile - DNF Aliases
# This file is automatically loaded when PowerShell starts

# DNF (Directory Name Fixer) Aliases
function start-work {
    <#
    .SYNOPSIS
    Start repository work by renaming exkontakt -> xk
    
    .DESCRIPTION
    Executes dnf.bat 1 to prepare the repository for work.
    This command renames "exkontakt" to "xk" in files and directories.
    #>
    
    $dnfPath = "C:\prv\dnf.bat"
    if (Test-Path $dnfPath) {
        & $dnfPath 1
    } else {
        Write-Host "Error: dnf.bat not found at $dnfPath" -ForegroundColor Red
        Write-Host "Please run this command from the C:\prv directory or update the path in your PowerShell profile." -ForegroundColor Yellow
    }
}

function finish-work {
    <#
    .SYNOPSIS
    Finish repository work by renaming sxky -> exkontakt
    
    .DESCRIPTION
    Executes dnf.bat 2 to restore the repository after work.
    This command renames "sxky" to "sexkontakty" in files and directories.
    #>
    
    $dnfPath = "C:\prv\dnf.bat"
    if (Test-Path $dnfPath) {
        & $dnfPath 2
    } else {
        Write-Host "Error: dnf.bat not found at $dnfPath" -ForegroundColor Red
        Write-Host "Please run this command from the C:\prv directory or update the path in your PowerShell profile." -ForegroundColor Yellow
    }
}

# Alternative shorter aliases
Set-Alias sw start-work
Set-Alias ew finish-work  # "end work" instead of "finish work" to avoid conflicts

# DNF direct access function
function dnf {
    <#
    .SYNOPSIS
    Direct access to DNF script
    
    .DESCRIPTION
    Provides direct access to the DNF Python script with all its features.
    
    .PARAMETER Arguments
    Arguments to pass to dnf.py
    
    .EXAMPLE
    dnf 1           # Same as start-work
    dnf 2           # Same as finish-work
    dnf --help      # Show help
    dnf rename 1 old new  # Direct rename
    #>
    
    $dnfPath = "C:\prv\dnf.py"
    if (Test-Path $dnfPath) {
        python $dnfPath @args
    } else {
        Write-Host "Error: dnf.py not found at $dnfPath" -ForegroundColor Red
    }
}

# Display available DNF commands when profile loads
Write-Host "DNF Aliases Loaded:" -ForegroundColor Green
Write-Host "  start-work (sw)  - Begin repository work" -ForegroundColor Cyan
Write-Host "  finish-work (ew) - End repository work" -ForegroundColor Cyan
Write-Host "  dnf <args>       - Direct access to DNF script" -ForegroundColor Cyan
Write-Host ""
