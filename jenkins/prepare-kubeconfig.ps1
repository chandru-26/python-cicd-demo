# =============================================================================
# Prepare a Jenkins-compatible kubeconfig file for Minikube
# =============================================================================

$ErrorActionPreference = 'Stop'

Write-Host "Generating Jenkins-compatible kubeconfig..." -ForegroundColor Cyan

# 1. Flatten kubeconfig (embeds all certs inline so it is self-contained)
$kubeconfig = kubectl config view --flatten --minify --raw | Out-String

# 2. Replace localhost/127.0.0.1 with host.docker.internal so the Jenkins
#    container can reach the host's Minikube API server.
$kubeconfig = $kubeconfig -replace 'https://127\.0\.0\.1:', 'https://host.docker.internal:'
$kubeconfig = $kubeconfig -replace 'https://localhost:',    'https://host.docker.internal:'

# 3. Save to file (plain ASCII, no BOM)
$outputPath = Join-Path $PSScriptRoot 'jenkins-kubeconfig.yaml'
[System.IO.File]::WriteAllText($outputPath, $kubeconfig)

Write-Host ""
Write-Host "SUCCESS! Created: $outputPath" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Open Jenkins -> Manage Jenkins -> Credentials -> (global) -> Add Credentials"
Write-Host "  2. Kind: Secret file"
Write-Host "  3. ID:   kubeconfig"
Write-Host "  4. File: $outputPath"
Write-Host ""
Write-Host "Verify the file content (first 5 lines):" -ForegroundColor Cyan
Get-Content $outputPath -TotalCount 5
