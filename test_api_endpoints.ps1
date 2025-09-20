# Test API Endpoints Script
Write-Host "Testing Law Agent Backend API Endpoints" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Test 1: Main page
Write-Host "`n1. Testing main page..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://law-agent-by-grok-1.onrender.com/" -Method GET -TimeoutSec 30
    Write-Host "   Status: $($response.StatusCode) - OK" -ForegroundColor Green
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Ping endpoint
Write-Host "`n2. Testing /api/ping endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://law-agent-by-grok-1.onrender.com/api/ping" -Method GET -TimeoutSec 30
    $content = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($response.StatusCode) - OK" -ForegroundColor Green
    Write-Host "   Message: $($content.message)" -ForegroundColor Cyan
    Write-Host "   Service: $($content.service)" -ForegroundColor Cyan
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: API endpoints list
Write-Host "`n3. Testing /api endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://law-agent-by-grok-1.onrender.com/api" -Method GET -TimeoutSec 30
    $content = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($response.StatusCode) - OK" -ForegroundColor Green
    Write-Host "   Available endpoints:" -ForegroundColor Cyan
    $content.endpoints | Get-Member -MemberType NoteProperty | ForEach-Object {
        Write-Host "     $($_.Name): $($content.endpoints.($_.Name))" -ForegroundColor Cyan
    }
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Health check
Write-Host "`n4. Testing /api/health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://law-agent-by-grok-1.onrender.com/api/health" -Method GET -TimeoutSec 30
    $content = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($response.StatusCode) - OK" -ForegroundColor Green
    Write-Host "   Service Status: $($content.status)" -ForegroundColor Cyan
    Write-Host "   Success: $($content.success)" -ForegroundColor Cyan
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Test endpoint (GET)
Write-Host "`n5. Testing /api/test endpoint (GET)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://law-agent-by-grok-1.onrender.com/api/test" -Method GET -TimeoutSec 30
    $content = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($response.StatusCode) - OK" -ForegroundColor Green
    Write-Host "   Success: $($content.success)" -ForegroundColor Cyan
    Write-Host "   Message: $($content.message)" -ForegroundColor Cyan
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Test endpoint (POST)
Write-Host "`n6. Testing /api/test endpoint (POST)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://law-agent-by-grok-1.onrender.com/api/test" -Method POST -Body "{}" -ContentType "application/json" -TimeoutSec 30
    $content = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($response.StatusCode) - OK" -ForegroundColor Green
    Write-Host "   Success: $($content.success)" -ForegroundColor Cyan
    Write-Host "   Message: $($content.message)" -ForegroundColor Cyan
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 7: CORS Preflight Request
Write-Host "`n7. Testing CORS preflight request..." -ForegroundColor Yellow
try {
    $headers = @{
        "Origin" = "https://example.com"
        "Access-Control-Request-Method" = "POST"
        "Access-Control-Request-Headers" = "Content-Type"
    }
    $response = Invoke-WebRequest -Uri "https://law-agent-by-grok-1.onrender.com/api/ping" -Method OPTIONS -Headers $headers -TimeoutSec 30
    Write-Host "   Status: $($response.StatusCode) - OK" -ForegroundColor Green
    Write-Host "   CORS preflight request successful" -ForegroundColor Cyan
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nAll tests completed!" -ForegroundColor Green