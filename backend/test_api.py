"""
Test script to demonstrate FESE Risk Engine API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_root():
    """Test root endpoint"""
    print("\n" + "="*70)
    print("TEST 1: Root Endpoint")
    print("="*70)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_health():
    """Test health check"""
    print("\n" + "="*70)
    print("TEST 2: Health Check")
    print("="*70)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_benford_expected():
    """Test Benford's Law expected frequencies"""
    print("\n" + "="*70)
    print("TEST 3: Benford's Law Expected Frequencies")
    print("="*70)
    response = requests.get(f"{BASE_URL}/api/v1/risk/benford-expected")
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"\nFormula: {result['formula']}")
    print("\nExpected Frequencies:")
    for digit, freq in result['expected_frequencies'].items():
        print(f"  Digit {digit}: {freq['percentage']}% (probability: {freq['probability']})")


def test_fraud_detection_legitimate():
    """Test fraud detection with legitimate data"""
    print("\n" + "="*70)
    print("TEST 4: Fraud Detection - Legitimate Transactions")
    print("="*70)
    
    # Log-normal distribution (should follow Benford's Law)
    import numpy as np
    transactions = np.random.lognormal(mean=5, sigma=1.5, size=200).tolist()
    
    payload = {
        "transactions": transactions,
        "significance_level": 0.05
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/risk/analyze-transactions",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    print(f"\n📊 Analysis Results:")
    print(f"   Total Transactions: {result['total_transactions']}")
    print(f"   Chi-square Statistic: {result['chi_square_stat']}")
    print(f"   P-value: {result['p_value']}")
    print(f"   Fraud Detected: {'❌ YES' if result['is_fraud'] else '✅ NO'}")
    print(f"   Fraud Probability: {result['fraud_probability']}%")
    print(f"   Interpretation: {result['interpretation']}")
    
    print(f"\n📈 Digit Distribution (Top 5):")
    for detail in result['details'][:5]:
        print(f"   Digit {detail['digit']}: "
              f"Observed={detail['observed_percentage']:.2f}%, "
              f"Expected={detail['expected_percentage']:.2f}%, "
              f"Deviation={detail['deviation']:+.2f}%")


def test_fraud_detection_fraudulent():
    """Test fraud detection with fraudulent data"""
    print("\n" + "="*70)
    print("TEST 5: Fraud Detection - Fraudulent Transactions")
    print("="*70)
    
    # Uniform distribution (should be flagged as fraud)
    import numpy as np
    transactions = np.random.uniform(100, 999, 200).tolist()
    
    payload = {
        "transactions": transactions,
        "significance_level": 0.05
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/risk/analyze-transactions",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    print(f"\n📊 Analysis Results:")
    print(f"   Total Transactions: {result['total_transactions']}")
    print(f"   Chi-square Statistic: {result['chi_square_stat']}")
    print(f"   P-value: {result['p_value']}")
    print(f"   Fraud Detected: {'❌ YES' if result['is_fraud'] else '✅ NO'}")
    print(f"   Fraud Probability: {result['fraud_probability']}%")
    print(f"   Interpretation: {result['interpretation']}")
    
    print(f"\n📈 Digit Distribution (Top 5):")
    for detail in result['details'][:5]:
        print(f"   Digit {detail['digit']}: "
              f"Observed={detail['observed_percentage']:.2f}%, "
              f"Expected={detail['expected_percentage']:.2f}%, "
              f"Deviation={detail['deviation']:+.2f}%")


def test_quick_fraud_check():
    """Test quick fraud check"""
    print("\n" + "="*70)
    print("TEST 6: Quick Fraud Check")
    print("="*70)
    
    transactions = [123.45, 234.56, 345.67, 456.78, 567.89, 123.11, 234.22]
    
    response = requests.post(
        f"{BASE_URL}/api/v1/risk/quick-fraud-check",
        json=transactions
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    """Run all tests"""
    print("\n🚀 FESE Risk Engine API - Test Suite")
    print("="*70)
    
    try:
        test_root()
        test_health()
        test_benford_expected()
        test_fraud_detection_legitimate()
        test_fraud_detection_fraudulent()
        test_quick_fraud_check()
        
        print("\n" + "="*70)
        print("✅ All API tests completed successfully!")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server!")
        print("   Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
