# Create required directories for docker-compose bind mounts (PowerShell version)

New-Item -ItemType Directory -Force -Path "n8n" | Out-Null
New-Item -ItemType Directory -Force -Path "minio\data" | Out-Null
New-Item -ItemType Directory -Force -Path "ffmpeg\files\clips" | Out-Null
New-Item -ItemType Directory -Force -Path "ffmpeg\files\jobs" | Out-Null
New-Item -ItemType Directory -Force -Path "FINAL\YT_Clips" | Out-Null

# Create .gitkeep files to preserve directory structure in git
New-Item -ItemType File -Force -Path "ffmpeg\files\.gitkeep" | Out-Null
New-Item -ItemType File -Force -Path "ffmpeg\files\jobs\.gitkeep" | Out-Null
New-Item -ItemType File -Force -Path "FINAL\YT_Clips\.gitkeep" | Out-Null

Write-Host "Directories created successfully!"

