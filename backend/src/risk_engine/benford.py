"""
Benford's Law Fraud Detection Module - "The Brain"

This module implements fraud detection using Benford's Law, which states that
in many naturally occurring datasets, the first digit is more likely to be small.
Benford's Law probability: P(d) = log₁₀(1 + 1/d) for d ∈ {1,2,...,9}

The chi-square test is used to determine if the observed distribution significantly
deviates from the expected Benford distribution, which may indicate fraud.
"""

import math
from typing import List, Dict, Tuple
import numpy as np
from scipy.stats import chisquare


class BenfordAnalyzer:
    """
    Analyzer for detecting fraudulent transactions using Benford's Law.
    
    Benford's Law states that in many naturally occurring collections of numbers,
    the leading digit is likely to be small. For example, the number 1 appears
    as the first digit about 30% of the time, while 9 appears less than 5%.
    
    This class analyzes transaction amounts to detect anomalies that may indicate
    fraudulent activity.
    
    Fraud Detection Logic:
    1. Chi-square test: p_value < significance_level
    2. Digit-1 Threshold: First digit '1' frequency outside [25%, 35%] range
    
    System flags fraud if ANY condition is violated (OR logic).
    """
    
    # Expected frequencies according to Benford's Law
    BENFORD_EXPECTED = {
        1: math.log10(1 + 1/1),  # ≈ 0.301 (30.1%)
        2: math.log10(1 + 1/2),  # ≈ 0.176 (17.6%)
        3: math.log10(1 + 1/3),  # ≈ 0.125 (12.5%)
        4: math.log10(1 + 1/4),  # ≈ 0.097 (9.7%)
        5: math.log10(1 + 1/5),  # ≈ 0.079 (7.9%)
        6: math.log10(1 + 1/6),  # ≈ 0.067 (6.7%)
        7: math.log10(1 + 1/7),  # ≈ 0.058 (5.8%)
        8: math.log10(1 + 1/8),  # ≈ 0.051 (5.1%)
        9: math.log10(1 + 1/9),  # ≈ 0.046 (4.6%)
    }
    
    # Digit-1 threshold for fraud detection
    # Benford standard for digit '1' is ~30.1%
    # We flag as suspicious if outside the range [25%, 35%]
    DIGIT_1_MIN_THRESHOLD = 25.0  # Minimum acceptable percentage for digit 1
    DIGIT_1_MAX_THRESHOLD = 35.0  # Maximum acceptable percentage for digit 1
    
    def __init__(self, significance_level: float = 0.05):
        """
        Initialize the Benford Analyzer.
        
        Args:
            significance_level: The threshold for determining fraud (default: 0.05)
                              If p-value < significance_level, flag as potential fraud
        """
        self.significance_level = significance_level
    
    @staticmethod
    def _extract_first_digit(number: float) -> int:
        """
        Extract the first significant digit from a number.
        
        Args:
            number: The number to extract the first digit from
            
        Returns:
            The first significant digit (1-9), or 0 if invalid
            
        Examples:
            >>> BenfordAnalyzer._extract_first_digit(123.45)
            1
            >>> BenfordAnalyzer._extract_first_digit(0.00456)
            4
            >>> BenfordAnalyzer._extract_first_digit(9876.5)
            9
        """
        if number <= 0:
            return 0
        
        # Convert to string and remove decimal point
        num_str = f"{abs(number):.10e}"  # Scientific notation
        
        # Extract the first non-zero digit
        for char in num_str:
            if char.isdigit() and char != '0':
                return int(char)
        
        return 0
    
    def _calculate_observed_frequencies(self, transactions: List[float]) -> Tuple[np.ndarray, int]:
        """
        Calculate the observed frequency of each first digit (1-9).
        
        Args:
            transactions: List of transaction amounts
            
        Returns:
            Tuple of (observed_counts, total_valid_transactions)
        """
        digit_counts = {d: 0 for d in range(1, 10)}
        valid_count = 0
        
        for amount in transactions:
            first_digit = self._extract_first_digit(amount)
            if 1 <= first_digit <= 9:
                digit_counts[first_digit] += 1
                valid_count += 1
        
        # Convert to numpy array in order 1-9
        observed = np.array([digit_counts[d] for d in range(1, 10)])
        
        return observed, valid_count
    
    def _calculate_expected_frequencies(self, total_count: int) -> np.ndarray:
        """
        Calculate expected frequencies based on Benford's Law.
        
        Args:
            total_count: Total number of valid transactions
            
        Returns:
            Array of expected counts for digits 1-9
        """
        expected = np.array([
            self.BENFORD_EXPECTED[d] * total_count for d in range(1, 10)
        ])
        
        return expected
    
    def analyze(self, transactions: List[float]) -> Dict:
        """
        Analyze transactions using Benford's Law to detect potential fraud.
        
        Args:
            transactions: List of transaction amounts to analyze
            
        Returns:
            Dictionary containing:
                - chi_square_stat: Chi-square test statistic
                - p_value: P-value from the chi-square test
                - is_fraud: Boolean indicating if fraud is suspected (p_value < 0.05)
                - details: List of dictionaries with digit-by-digit comparison
                - total_transactions: Total number of valid transactions analyzed
                - fraud_probability: 1 - p_value (confidence of fraud)
                
        Example:
            >>> analyzer = BenfordAnalyzer()
            >>> transactions = [123.45, 234.56, 345.67, 456.78]
            >>> result = analyzer.analyze(transactions)
            >>> print(f"Is Fraud: {result['is_fraud']}")
        """
        if not transactions:
            return {
                "chi_square_stat": 0.0,
                "p_value": 1.0,
                "is_fraud": False,
                "details": [],
                "total_transactions": 0,
                "fraud_probability": 0.0,
                "error": "No transactions provided"
            }
        
        # Calculate observed frequencies
        observed, valid_count = self._calculate_observed_frequencies(transactions)
        
        if valid_count == 0:
            return {
                "chi_square_stat": 0.0,
                "p_value": 1.0,
                "is_fraud": False,
                "details": [],
                "total_transactions": 0,
                "fraud_probability": 0.0,
                "error": "No valid transactions (all zero or negative)"
            }
        
        # Calculate expected frequencies
        expected = self._calculate_expected_frequencies(valid_count)
        
        # Perform chi-square test
        chi_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
        
        # Calculate digit-1 percentage for threshold check
        digit_1_count = observed[0]  # First element is digit 1
        digit_1_percentage = (digit_1_count / valid_count) * 100 if valid_count > 0 else 0
        
        # Check fraud conditions
        chi_square_violation = p_value < self.significance_level
        digit_1_violation = (digit_1_percentage < self.DIGIT_1_MIN_THRESHOLD or 
                            digit_1_percentage > self.DIGIT_1_MAX_THRESHOLD)
        
        # Fraud detected if ANY condition is violated (OR logic)
        is_fraud = chi_square_violation or digit_1_violation
        
        # Track which conditions were violated (Red Flags)
        red_flags = {
            "chi_square_violation": chi_square_violation,
            "digit_1_threshold_violation": digit_1_violation
        }
        
        # Create detailed comparison
        details = []
        for digit in range(1, 10):
            idx = digit - 1
            observed_pct = (observed[idx] / valid_count) * 100 if valid_count > 0 else 0
            expected_pct = self.BENFORD_EXPECTED[digit] * 100
            
            details.append({
                "digit": digit,
                "observed_count": int(observed[idx]),
                "expected_count": round(expected[idx], 2),
                "observed_percentage": round(observed_pct, 2),
                "expected_percentage": round(expected_pct, 2),
                "deviation": round(observed_pct - expected_pct, 2)
            })
        
        return {
            "chi_square_stat": round(float(chi_stat), 4),
            "p_value": round(float(p_value), 4),
            "is_fraud": bool(is_fraud),
            "red_flags": red_flags,
            "digit_1_analysis": {
                "observed_percentage": round(digit_1_percentage, 2),
                "expected_percentage": round(self.BENFORD_EXPECTED[1] * 100, 2),
                "threshold_min": self.DIGIT_1_MIN_THRESHOLD,
                "threshold_max": self.DIGIT_1_MAX_THRESHOLD,
                "is_within_threshold": not digit_1_violation
            },
            "details": details,
            "total_transactions": valid_count,
            "fraud_probability": round((1 - p_value) * 100, 2),
            "interpretation": self._interpret_result(p_value, digit_1_percentage, red_flags)
        }
    
    def _interpret_result(self, p_value: float, digit_1_pct: float, red_flags: Dict) -> str:
        """
        Provide human-readable interpretation based on all fraud detection criteria.
        
        Args:
            p_value: The p-value from chi-square test
            digit_1_pct: Observed percentage of digit 1
            red_flags: Dictionary of violated conditions
            
        Returns:
            Interpretation string
        """
        chi_violation = red_flags.get("chi_square_violation", False)
        digit_1_violation = red_flags.get("digit_1_threshold_violation", False)
        
        # Both violations - Highest risk
        if chi_violation and digit_1_violation:
            return (f"🚨 CRITICAL: Multiple fraud indicators detected - "
                   f"Chi-square test failed (p={p_value:.4f}) AND "
                   f"Digit-1 outside threshold ({digit_1_pct:.2f}% not in [25%, 35%])")
        
        # Only digit-1 violation
        if digit_1_violation:
            if digit_1_pct < self.DIGIT_1_MIN_THRESHOLD:
                return (f"⚠️ RED FLAG: Digit-1 suspiciously low ({digit_1_pct:.2f}% < 25%) - "
                       f"Possible fabricated data or selective reporting")
            else:
                return (f"⚠️ RED FLAG: Digit-1 suspiciously high ({digit_1_pct:.2f}% > 35%) - "
                       f"Possible data manipulation or rounding bias")
        
        # Only chi-square violation
        if chi_violation:
            if p_value < 0.001:
                return f"⚠️ Strong statistical deviation from Benford (p={p_value:.4f}) - Investigation required"
            elif p_value < 0.01:
                return f"⚠️ Moderate statistical deviation from Benford (p={p_value:.4f}) - Review recommended"
            else:
                return f"⚠️ Weak statistical deviation from Benford (p={p_value:.4f}) - Monitor closely"
        
        # No violations
        return (f"✅ Data follows Benford's Law - No fraud detected "
               f"(p={p_value:.4f}, Digit-1={digit_1_pct:.2f}%)")


def main():
    """
    Test the BenfordAnalyzer with dummy data.
    
    Tests two scenarios:
    1. Uniform distribution (should be flagged as fraud)
    2. Log-normal distribution (should follow Benford's Law)
    """
    print("=" * 70)
    print("BENFORD'S LAW FRAUD DETECTION - TEST MODULE")
    print("=" * 70)
    
    analyzer = BenfordAnalyzer()
    
    # Test 1: Uniform distribution (fraudulent)
    print("\n📊 TEST 1: Uniform Distribution (Expected: FRAUD)")
    print("-" * 70)
    uniform_transactions = np.random.uniform(100, 999, 1000).tolist()
    result_uniform = analyzer.analyze(uniform_transactions)
    
    print(f"Total Transactions: {result_uniform['total_transactions']}")
    print(f"Chi-square Statistic: {result_uniform['chi_square_stat']}")
    print(f"P-value: {result_uniform['p_value']}")
    print(f"Fraud Detected: {result_uniform['is_fraud']} ({'YES' if result_uniform['is_fraud'] else 'NO'})")
    print(f"Fraud Probability: {result_uniform['fraud_probability']}%")
    print(f"Interpretation: {result_uniform['interpretation']}")
    
    print("\n📈 Digit Distribution:")
    print(f"{'Digit':<6} {'Observed %':<12} {'Expected %':<12} {'Deviation':<10}")
    print("-" * 50)
    for detail in result_uniform['details']:
        print(f"{detail['digit']:<6} {detail['observed_percentage']:<12.2f} "
              f"{detail['expected_percentage']:<12.2f} {detail['deviation']:>+9.2f}")
    
    # Test 2: Log-normal distribution (legitimate)
    print("\n\n📊 TEST 2: Log-Normal Distribution (Expected: LEGITIMATE)")
    print("-" * 70)
    lognormal_transactions = np.random.lognormal(mean=5, sigma=1.5, size=1000).tolist()
    result_lognormal = analyzer.analyze(lognormal_transactions)
    
    print(f"Total Transactions: {result_lognormal['total_transactions']}")
    print(f"Chi-square Statistic: {result_lognormal['chi_square_stat']}")
    print(f"P-value: {result_lognormal['p_value']}")
    print(f"Fraud Detected: {result_lognormal['is_fraud']} ({'YES' if result_lognormal['is_fraud'] else 'NO'})")
    print(f"Fraud Probability: {result_lognormal['fraud_probability']}%")
    print(f"Interpretation: {result_lognormal['interpretation']}")
    
    print("\n📈 Digit Distribution:")
    print(f"{'Digit':<6} {'Observed %':<12} {'Expected %':<12} {'Deviation':<10}")
    print("-" * 50)
    for detail in result_lognormal['details']:
        print(f"{detail['digit']:<6} {detail['observed_percentage']:<12.2f} "
              f"{detail['expected_percentage']:<12.2f} {detail['deviation']:>+9.2f}")
    
    # Test 3: Real-world example with mixed patterns
    print("\n\n📊 TEST 3: Mixed Pattern (Some Fraud)")
    print("-" * 70)
    # Mix of legitimate (70%) and fraudulent (30%) transactions
    legit_trans = np.random.lognormal(mean=4, sigma=1, size=700).tolist()
    fraud_trans = np.random.uniform(500, 599, 300).tolist()  # Artificially starting with 5
    mixed_transactions = legit_trans + fraud_trans
    np.random.shuffle(mixed_transactions)
    
    result_mixed = analyzer.analyze(mixed_transactions)
    
    print(f"Total Transactions: {result_mixed['total_transactions']}")
    print(f"Chi-square Statistic: {result_mixed['chi_square_stat']}")
    print(f"P-value: {result_mixed['p_value']}")
    print(f"Fraud Detected: {result_mixed['is_fraud']} ({'YES' if result_mixed['is_fraud'] else 'NO'})")
    print(f"Fraud Probability: {result_mixed['fraud_probability']}%")
    print(f"Interpretation: {result_mixed['interpretation']}")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
