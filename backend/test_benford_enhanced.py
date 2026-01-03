"""
Enhanced Test for Benford's Law with Digit-1 Threshold Logic
Demonstrates the new fraud detection system with dual criteria
"""
import sys
from pathlib import Path
import numpy as np

# Add src to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from src.risk_engine.benford import BenfordAnalyzer


def print_result(title: str, result: dict):
    """Print analysis result in formatted way"""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   Total Transactions: {result['total_transactions']}")
    print(f"   Chi-square Stat: {result['chi_square_stat']}")
    print(f"   P-value: {result['p_value']}")
    
    print(f"\n🎯 DIGIT-1 ANALYSIS:")
    d1 = result['digit_1_analysis']
    print(f"   Observed: {d1['observed_percentage']}%")
    print(f"   Expected: {d1['expected_percentage']}%")
    print(f"   Threshold Range: [{d1['threshold_min']}%, {d1['threshold_max']}%]")
    print(f"   Within Threshold: {'✅ YES' if d1['is_within_threshold'] else '❌ NO'}")
    
    print(f"\n🚨 RED FLAGS:")
    flags = result['red_flags']
    print(f"   Chi-square Violation: {'❌ YES' if flags['chi_square_violation'] else '✅ NO'}")
    print(f"   Digit-1 Threshold Violation: {'❌ YES' if flags['digit_1_threshold_violation'] else '✅ NO'}")
    
    print(f"\n⚖️ FINAL VERDICT:")
    print(f"   Fraud Detected: {'🔴 YES' if result['is_fraud'] else '🟢 NO'}")
    print(f"   Fraud Probability: {result['fraud_probability']}%")
    print(f"   Interpretation: {result['interpretation']}")


def test_case_1_legitimate():
    """Test Case 1: Legitimate data (log-normal distribution)"""
    print("\n" + "🧪 TEST CASE 1: LEGITIMATE DATA (Log-Normal Distribution)")
    
    analyzer = BenfordAnalyzer()
    transactions = np.random.lognormal(mean=5, sigma=1.5, size=500).tolist()
    result = analyzer.analyze(transactions)
    
    print_result("Expected: ✅ NO FRAUD (Both checks should pass)", result)


def test_case_2_chi_square_only():
    """Test Case 2: Violates chi-square but digit-1 is OK"""
    print("\n" + "🧪 TEST CASE 2: CHI-SQUARE VIOLATION ONLY")
    print("   (Digit-1 within threshold, but overall distribution bad)")
    
    analyzer = BenfordAnalyzer()
    # Create data where digit-1 is ~30% but other digits are uniform
    digit_1_trans = np.random.uniform(100, 199, 150).tolist()  # ~30% digit-1
    other_trans = np.random.uniform(200, 999, 350).tolist()     # Uniform for rest
    transactions = digit_1_trans + other_trans
    np.random.shuffle(transactions)
    
    result = analyzer.analyze(transactions)
    print_result("Expected: ⚠️ FRAUD (Chi-square fails, Digit-1 OK)", result)


def test_case_3_digit1_too_low():
    """Test Case 3: Digit-1 too low (< 25%)"""
    print("\n" + "🧪 TEST CASE 3: DIGIT-1 TOO LOW")
    print("   (Digit-1 < 25% - suspicious under-reporting)")
    
    analyzer = BenfordAnalyzer()
    # Only 20% digit-1, rest distributed
    digit_1_trans = np.random.uniform(100, 199, 100).tolist()  # 20% digit-1
    other_trans = np.random.uniform(200, 999, 400).tolist()    # 80% others
    transactions = digit_1_trans + other_trans
    np.random.shuffle(transactions)
    
    result = analyzer.analyze(transactions)
    print_result("Expected: 🚨 RED FLAG (Digit-1 too low)", result)


def test_case_4_digit1_too_high():
    """Test Case 4: Digit-1 too high (> 35%)"""
    print("\n" + "🧪 TEST CASE 4: DIGIT-1 TOO HIGH")
    print("   (Digit-1 > 35% - suspicious over-reporting or rounding)")
    
    analyzer = BenfordAnalyzer()
    # 40% digit-1
    digit_1_trans = np.random.uniform(100, 199, 200).tolist()  # 40% digit-1
    other_trans = np.random.uniform(200, 999, 300).tolist()    # 60% others
    transactions = digit_1_trans + other_trans
    np.random.shuffle(transactions)
    
    result = analyzer.analyze(transactions)
    print_result("Expected: 🚨 RED FLAG (Digit-1 too high)", result)


def test_case_5_both_violations():
    """Test Case 5: Both violations (Critical fraud)"""
    print("\n" + "🧪 TEST CASE 5: CRITICAL - BOTH VIOLATIONS")
    print("   (Uniform distribution - worst case)")
    
    analyzer = BenfordAnalyzer()
    transactions = np.random.uniform(100, 999, 500).tolist()
    result = analyzer.analyze(transactions)
    
    print_result("Expected: 🚨🚨 CRITICAL FRAUD (Both checks fail)", result)


def test_case_6_edge_case_boundary():
    """Test Case 6: Digit-1 exactly at boundary (25%)"""
    print("\n" + "🧪 TEST CASE 6: BOUNDARY TEST")
    print("   (Digit-1 exactly at 25% threshold)")
    
    analyzer = BenfordAnalyzer()
    # Exactly 25% digit-1
    digit_1_trans = np.random.uniform(100, 199, 125).tolist()  # 25% digit-1
    # Distribute rest to follow rough Benford
    digit_2_trans = np.random.uniform(200, 299, 88).tolist()   # ~17.6%
    digit_3_trans = np.random.uniform(300, 399, 62).tolist()   # ~12.4%
    other_trans = np.random.uniform(400, 999, 225).tolist()    # Rest
    
    transactions = digit_1_trans + digit_2_trans + digit_3_trans + other_trans
    np.random.shuffle(transactions)
    
    result = analyzer.analyze(transactions)
    print_result("Expected: Borderline (25% exactly - should pass)", result)


def main():
    """Run all test cases"""
    print("\n" + "="*80)
    print("🚀 ENHANCED BENFORD FRAUD DETECTION - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print("\n📋 Testing dual fraud detection logic:")
    print("   1. Chi-square test (p-value < 0.05)")
    print("   2. Digit-1 threshold (must be within 25-35%)")
    print("   Fraud flagged if ANY condition violated (OR logic)")
    
    test_case_1_legitimate()
    test_case_2_chi_square_only()
    test_case_3_digit1_too_low()
    test_case_4_digit1_too_high()
    test_case_5_both_violations()
    test_case_6_edge_case_boundary()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED!")
    print("="*80)
    print("\n📚 KEY INSIGHTS:")
    print("   • System detects fraud via TWO independent methods")
    print("   • Digit-1 threshold catches specific manipulation patterns")
    print("   • Chi-square test catches overall distribution anomalies")
    print("   • Combined approach increases fraud detection accuracy")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
