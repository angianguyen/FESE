# FESE Risk Engine - Quick Start Guide

## 🚀 Khởi động Backend Server

```powershell
# Từ thư mục gốc project
cd E:\FESE\project_fese
.\.venv\Scripts\Activate.ps1
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Server sẽ chạy tại: **http://127.0.0.1:8000**

## 📚 API Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧪 Test Risk Engine

### Option 1: Sử dụng test script
```powershell
# Terminal mới (giữ server chạy ở terminal khác)
cd E:\FESE\project_fese
.\.venv\Scripts\Activate.ps1
cd backend
python test_api.py
```

### Option 2: Test trực tiếp module
```powershell
cd E:\FESE\project_fese
.\.venv\Scripts\Activate.ps1
cd backend
python src/risk_engine/benford.py
```

### Option 3: Sử dụng curl/PowerShell
```powershell
# Test health check
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get

# Test fraud detection
$body = @{
    transactions = @(123.45, 234.56, 345.67, 456.78)
    significance_level = 0.05
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/risk/analyze-transactions" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

## 📊 Available API Endpoints

### Health & Info
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/` - API v1 root

### Risk Analysis
- `GET /api/v1/risk/benford-expected` - Get Benford's Law expected frequencies
- `POST /api/v1/risk/analyze-transactions` - Analyze transactions for fraud
- `POST /api/v1/risk/quick-fraud-check` - Quick fraud check (simplified)

## 💡 Example Request

```json
POST /api/v1/risk/analyze-transactions
{
  "transactions": [
    123.45, 234.56, 345.67, 456.78, 567.89,
    123.11, 234.22, 345.33, 456.44, 567.55
  ],
  "significance_level": 0.05
}
```

## 📈 Example Response

```json
{
  "chi_square_stat": 2.5432,
  "p_value": 0.9234,
  "is_fraud": false,
  "total_transactions": 10,
  "fraud_probability": 7.66,
  "interpretation": "Data follows Benford's Law - No fraud detected",
  "details": [
    {
      "digit": 1,
      "observed_count": 2,
      "expected_count": 3.01,
      "observed_percentage": 20.0,
      "expected_percentage": 30.1,
      "deviation": -10.1
    },
    ...
  ]
}
```
