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

# 3. Skip TLS verification (Minikube cert is not valid for host.docker.internal).
#    Remove the certificate-authority-data line and add insecure-skip-tls-verify: true.
$kubeconfig = $kubeconfig -replace '(?m)^\s*certificate-authority-data:.*\r?\n', ''
$kubeconfig = $kubeconfig -replace '(?m)(^\s*server:\s*https://host\.docker\.internal:\d+\s*$)', "`$1`n    insecure-skip-tls-verify: true"

# 4. Save to file (plain ASCII, no BOM)
$outputPath = Join-Path $PSScriptRoot 'jenkins-kubeconfig.yaml'
[System.IO.File]::WriteAllText($outputPath, $kubeconfig)

Write-Host ""
Write-Host "SUCCESS! Created: $outputPath" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Open Jenkins -> Manage Jenkins -> Credentials"
Write-Host "  2. DELETE the old 'kubeconfig' credential (if it exists)"
Write-Host "  3. Add new credential:"
Write-Host "       Kind: Secret file"
Write-Host "       ID:   kubeconfig"
Write-Host "       File: $outputPath"
Write-Host ""
Write-Host "File preview (first 12 lines):" -ForegroundColor Cyan
Get-Content $outputPath -TotalCount 12
