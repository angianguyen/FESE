# Credit Scoring System - Technical Documentation

## 📋 Tổng quan

Hệ thống chấm điểm tín dụng tự động cho StreamCredit, đánh giá khả năng tín nhiệm của merchant dựa trên lịch sử giao dịch Shopify.

## 🎯 Mục tiêu

- Tự động hóa quy trình phê duyệt tín dụng
- Phát hiện gian lận thông qua Benford's Law
- Tính toán hạn mức tín dụng an toàn
- Đánh giá rủi ro merchant

## 📊 Data Structure

### Input: Transaction Data
```python
{
    "date": "YYYY-MM-DD",           # Ngày giao dịch
    "order_id": "ORD_xxxxx",        # Mã đơn hàng
    "amount": float,                # Số tiền (USD)
    "customer_id": "CUST_xxxxx",    # Mã khách hàng
    "product_count": int            # Số lượng sản phẩm
}
```

**Ví dụ:**
```python
{
    "date": "2025-12-15",
    "order_id": "ORD_45231",
    "amount": 87.50,
    "customer_id": "CUST_8723",
    "product_count": 3
}
```

### Output: Scoring Result
```python
{
    "score": int,                      # Điểm tín dụng (0, 400, 750)
    "decision": str,                   # "Approved" hoặc "Rejected"
    "credit_limit": float,             # Hạn mức tín dụng (USD)
    "monthly_avg_revenue": float,      # Doanh thu trung bình/tháng
    "avg_order_value": float,          # Giá trị đơn hàng trung bình
    "total_transactions": int,         # Tổng số giao dịch
    "fraud_check": dict,               # Kết quả phát hiện gian lận
    "reasons": list[str],              # Lý do quyết định
    "risk_level": str                  # "Low", "Medium", "High"
}
```

## 🔄 Quy trình Chấm điểm (Credit Scoring Flow)

### Bước 1: Validation
```
Input: transactions[]
↓
Kiểm tra: transactions không rỗng?
├─ ❌ NO → Return: Score 400, Rejected
└─ ✅ YES → Tiếp tục Bước 2
```

### Bước 2: Fraud Detection (Benford's Law)
```
Chạy BenfordAnalyzer trên transaction amounts
↓
Phân tích:
├─ Chi-square test (p_value)
└─ Digit-1 frequency (25-35%)
↓
Fraud Detection Logic (OR):
├─ p_value < 0.05? ────────┐
└─ digit_1 < 25% OR > 35%? ─┤
                             ↓
                    ❌ ANY True?
                    ├─ YES → Return: Score 0 (FRAUD), Rejected
                    └─ NO → Tiếp tục Bước 3
```

### Bước 3: Tính toán Metrics

#### 3.1. Monthly Average Revenue (MAR)
```python
# Công thức
MAR = Total_Revenue / Number_of_Months

# Chi tiết:
1. Group transactions by month (YYYY-MM)
2. Calculate total revenue per month
3. Sum all monthly revenues → Total_Revenue
4. Count unique months → Number_of_Months
5. MAR = Total_Revenue / Number_of_Months
```

**Ví dụ:**
```
Month 2025-10: $8,500
Month 2025-11: $9,200
Month 2025-12: $10,100
----------------------------
Total Revenue: $27,800
Months: 3
MAR = $27,800 / 3 = $9,266.67
```

#### 3.2. Average Order Value (AOV)
```python
# Công thức
AOV = Total_Amount / Total_Orders

# Chi tiết:
1. Sum all transaction amounts → Total_Amount
2. Count all transactions → Total_Orders
3. AOV = Total_Amount / Total_Orders
```

**Ví dụ:**
```
Transaction 1: $45.00
Transaction 2: $67.50
Transaction 3: $123.00
Transaction 4: $89.25
----------------------------
Total Amount: $324.75
Total Orders: 4
AOV = $324.75 / 4 = $81.19
```

### Bước 4: Apply Scoring Rules

```
Decision Logic:
IF (MAR > $5,000) AND (AOV > $30)
├─ ✅ TRUE
│   ├─ Score: 750
│   ├─ Decision: "Approved"
│   └─ Proceed to Credit Limit Calculation
└─ ❌ FALSE
    ├─ Score: 400
    ├─ Decision: "Rejected"
    └─ Credit Limit: $0
```

### Bước 5: Calculate Credit Limit (if Approved)

```python
# Công thức
Credit_Limit = MIN(MAR × 2, $10,000)

# Logic:
1. Base_Limit = MAR × 2 (multiplier = 2.0)
2. Final_Limit = min(Base_Limit, MAX_LIMIT)
3. MAX_LIMIT = $10,000 (hard cap)
```

**Ví dụ:**
```
Case 1: MAR = $3,000
Base = $3,000 × 2 = $6,000
Limit = min($6,000, $10,000) = $6,000

Case 2: MAR = $8,000
Base = $8,000 × 2 = $16,000
Limit = min($16,000, $10,000) = $10,000 (capped)
```

### Bước 6: Risk Assessment

```
Risk Level Logic:

IF score == 0 (FRAUD)
    └─ Risk: "High"

ELSE IF fraud_check.is_fraud == True
    └─ Risk: "High"

ELSE IF score >= 750 (APPROVED)
    └─ Risk: "Low"

ELSE
    └─ Risk: "Medium"
```

## 📐 Tiêu chuẩn Đánh giá

### 1. Revenue Thresholds

| Metric | Threshold | Description |
|--------|-----------|-------------|
| **MAR** | > $5,000 | Doanh thu trung bình tháng tối thiểu |
| **AOV** | > $30 | Giá trị đơn hàng trung bình tối thiểu |

### 2. Credit Scores

| Score | Meaning | Action |
|-------|---------|--------|
| **750** | Excellent | Approved - Low Risk |
| **400** | Poor | Rejected - Insufficient Revenue |
| **0** | Fraud | Rejected - Fraud Detected |

### 3. Fraud Detection Criteria

#### Chi-square Test
- **Method**: Statistical distribution test
- **Threshold**: `p_value < 0.05`
- **Meaning**: Distribution significantly deviates from Benford's Law

#### Digit-1 Threshold
- **Expected (Benford)**: ~30.1%
- **Acceptable Range**: 25% - 35%
- **Red Flags**:
  - `< 25%`: Suspicious under-reporting
  - `> 35%`: Suspicious over-reporting or rounding

### 4. Credit Limit Calculation

| Component | Value | Notes |
|-----------|-------|-------|
| **Multiplier** | 2.0x | Credit limit = 2 × MAR |
| **Maximum Cap** | $10,000 | Hard limit |
| **Minimum** | $0 | If rejected |

## 🧪 Mock Data Generator

### Healthy Business (`is_healthy=True`)
```python
# Characteristics:
- Distribution: Log-normal (natural for financial data)
- Parameters: mean=4.5, sigma=1.2
- Trend: 5% monthly growth
- Transaction count: 100-200/month (increasing)
- Amount range: $10 - $500+
- Product count: 1-5 items/order

# Expected Results:
✅ Follows Benford's Law
✅ MAR typically > $5,000
✅ AOV typically > $30
✅ Score: 750 (Approved)
```

### Suspicious Business (`is_healthy=False`)
```python
# Characteristics:
- Distribution: Uniform (unnatural - red flag)
- Volatility: High (20-200 transactions/month)
- Amount range: $10 - $500 (uniform)
- Pattern: Random, no growth trend

# Expected Results:
❌ Violates Benford's Law
❌ Chi-square test fails
❌ Digit-1 outside threshold
❌ Score: 0 (Fraud Detected)
```

## 📊 Example Scenarios

### Scenario 1: ✅ Healthy Approved Business

**Input:**
- 12 months of data
- ~1,500 transactions
- Growing revenue trend
- Log-normal distribution

**Calculations:**
```
MAR = $8,500
AOV = $65.30
Digit-1: 29.5% (within 25-35%)
P-value: 0.42 (> 0.05)
```

**Output:**
```
Score: 750
Decision: Approved
Credit Limit: $10,000 (capped from $17,000)
Risk Level: Low
Reasons:
✅ Strong revenue: MAR $8,500 > $5,000
✅ Healthy AOV: $65.30 > $30
💰 Credit limit: $10,000 (2x MAR, capped)
```

### Scenario 2: ❌ Low Revenue Business

**Input:**
- 3 months of data
- ~200 transactions
- Small business

**Calculations:**
```
MAR = $2,100
AOV = $45.50
Digit-1: 28.0% (within threshold)
P-value: 0.35 (> 0.05)
```

**Output:**
```
Score: 400
Decision: Rejected
Credit Limit: $0
Risk Level: Medium
Reasons:
❌ Insufficient revenue: MAR $2,100 ≤ $5,000
✅ Healthy AOV: $45.50 > $30
```

### Scenario 3: 🚨 Fraud Detected

**Input:**
- 12 months of data
- ~1,200 transactions
- Uniform distribution (suspicious)

**Calculations:**
```
MAR = $6,800
AOV = $52.00
Digit-1: 18.5% (< 25% - RED FLAG!)
P-value: 0.0001 (< 0.05 - RED FLAG!)
```

**Output:**
```
Score: 0
Decision: Rejected
Credit Limit: $0
Risk Level: High
Reasons:
🚨 FRAUD DETECTED
❌ Statistical anomaly detected
❌ Digit-1 frequency suspicious (18.5% outside 25-35%)
```

## 🔧 Configuration

### Adjustable Parameters

```python
# In CreditScorer class
MAR_THRESHOLD = 5000.0        # Monthly revenue requirement
AOV_THRESHOLD = 30.0          # Average order value requirement
CREDIT_MULTIPLIER = 2.0       # Credit limit multiplier
MAX_CREDIT_LIMIT = 10000.0    # Maximum credit limit cap

# In BenfordAnalyzer
DIGIT_1_MIN_THRESHOLD = 25.0  # Minimum digit-1 %
DIGIT_1_MAX_THRESHOLD = 35.0  # Maximum digit-1 %
significance_level = 0.05      # Chi-square p-value threshold
```

## 📈 Usage Examples

### Basic Usage
```python
from src.risk_engine.scoring import CreditScorer, generate_mock_shopify_data

# Initialize scorer
scorer = CreditScorer()

# Generate or load transaction data
transactions = generate_mock_shopify_data(months=12, is_healthy=True)

# Calculate score
result = scorer.calculate_score(transactions)

# Check result
if result['decision'] == 'Approved':
    print(f"Approved! Credit Limit: ${result['credit_limit']:,.2f}")
else:
    print(f"Rejected. Reasons: {result['reasons']}")
```

### API Integration
```python
# In FastAPI endpoint
@app.post("/api/v1/credit/evaluate")
async def evaluate_credit(shopify_data: ShopifyData):
    scorer = CreditScorer()
    result = scorer.calculate_score(shopify_data.transactions)
    return result
```

## ⚠️ Important Notes

1. **Fraud Check Priority**: Fraud detection chạy TRƯỚC scoring rules
2. **Auto-Reject on Fraud**: Nếu fraud detected → Score = 0, bỏ qua tất cả checks khác
3. **Both Conditions Required**: Cần CẢ HAI MAR và AOV pass mới approved
4. **Credit Limit Cap**: Luôn có hard cap $10,000 dù MAR cao
5. **Minimum Amount**: Mock data có minimum $10 để tránh outliers

## 🔍 Testing

```bash
# Run scoring tests
python src/risk_engine/scoring.py

# Expected output:
# - Test Case 1: Healthy → Approved
# - Test Case 2: Low Revenue → Rejected
# - Test Case 3: Suspicious → Fraud
```

## 📚 Dependencies

```python
numpy          # Statistical distributions
scipy          # Chi-square test (via BenfordAnalyzer)
datetime       # Date handling
dataclasses    # Data structures
```

## 🎓 Mathematical Foundations

### Benford's Law
$$P(d) = \log_{10}\left(1 + \frac{1}{d}\right)$$

For digit 1: $P(1) = \log_{10}(2) \approx 0.301$ (30.1%)

### Log-normal Distribution
Healthy business data follows:
$$f(x) = \frac{1}{x\sigma\sqrt{2\pi}} e^{-\frac{(\ln x - \mu)^2}{2\sigma^2}}$$

Parameters: $\mu = 4.5$, $\sigma = 1.2$

---

**Version**: 1.0  
**Last Updated**: January 2, 2026  
**Author**: FESE StreamCredit Team
