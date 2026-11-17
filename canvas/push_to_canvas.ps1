# Push canvas/home.html to the Canvas course home (front) page via the Canvas REST API.
#
# One-time setup:
#   1. Canvas -> Account -> Settings -> "+ New Access Token", copy the token.
#   2. Save it (single line, no quotes) to:  canvas\.canvas_token   (git-ignored)
#   3. Set $CourseId below to the number in your course URL:
#      https://canvas.fsu.edu/courses/<CourseId>
#
# Usage:  powershell -File canvas\push_to_canvas.ps1

param(
    [string]$CanvasBase = "https://canvas.fsu.edu",
    [string]$CourseId   = "380530",
    [string]$HtmlPath   = "$PSScriptRoot\home.html"
)

$ErrorActionPreference = "Stop"

# --- token ---
$token = $env:CANVAS_TOKEN
$tokenFile = Join-Path $PSScriptRoot ".canvas_token"
if (-not $token -and (Test-Path $tokenFile)) {
    $token = (Get-Content $tokenFile -Raw).Trim()
}
if (-not $token) {
    Write-Error "No Canvas token. Put it in canvas\.canvas_token or set `$env:CANVAS_TOKEN."
}
if ($CourseId -eq "REPLACE_ME") {
    Write-Error "Set -CourseId (the number in https://canvas.fsu.edu/courses/<id>)."
}

# --- body ---
$html = Get-Content $HtmlPath -Raw -Encoding UTF8
$json = ConvertTo-Json @{ wiki_page = @{ body = $html } } -Depth 3 -Compress
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)

# --- update the course front page ---
$uri = "$CanvasBase/api/v1/courses/$CourseId/front_page"
$resp = Invoke-RestMethod -Method Put -Uri $uri `
    -Headers @{ Authorization = "Bearer $token" } `
    -ContentType "application/json; charset=utf-8" `
    -Body $bytes

Write-Host "Updated: '$($resp.title)' (page '$($resp.url)', edited $($resp.updated_at))"
Write-Host "View: $CanvasBase/courses/$CourseId/pages/$($resp.url)"
