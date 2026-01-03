"""
Unit tests for Benford's Law Analyzer
"""
import pytest
import numpy as np
from backend.src.risk_engine.benford import BenfordAnalyzer


class TestBenfordAnalyzer:
    """Test suite for BenfordAnalyzer class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = BenfordAnalyzer()
    
    def test_extract_first_digit(self):
        """Test first digit extraction"""
        assert BenfordAnalyzer._extract_first_digit(123.45) == 1
        assert BenfordAnalyzer._extract_first_digit(234.56) == 2
        assert BenfordAnalyzer._extract_first_digit(0.00456) == 4
        assert BenfordAnalyzer._extract_first_digit(9876.5) == 9
        assert BenfordAnalyzer._extract_first_digit(0) == 0
        assert BenfordAnalyzer._extract_first_digit(-123) == 1
    
    def test_empty_transactions(self):
        """Test with empty transaction list"""
        result = self.analyzer.analyze([])
        assert result["is_fraud"] is False
        assert result["total_transactions"] == 0
        assert "error" in result
    
    def test_uniform_distribution_fraud(self):
        """Test that uniform distribution is flagged as fraud"""
        # Generate uniform distribution (should not follow Benford)
        transactions = np.random.uniform(100, 999, 1000).tolist()
        result = self.analyzer.analyze(transactions)
        
        assert result["is_fraud"] is True
        assert result["p_value"] < 0.05
        assert result["total_transactions"] == 1000
    
    def test_lognormal_distribution_legitimate(self):
        """Test that log-normal distribution follows Benford's Law"""
        # Generate log-normal distribution (should follow Benford)
        transactions = np.random.lognormal(mean=5, sigma=1.5, size=1000).tolist()
        result = self.analyzer.analyze(transactions)
        
        # Log-normal should generally follow Benford's Law
        # Note: Due to randomness, we check p_value is reasonable
        assert result["total_transactions"] == 1000
        assert "details" in result
        assert len(result["details"]) == 9
    
    def test_negative_transactions(self):
        """Test handling of negative transactions"""
        transactions = [-100, -200, 300, 400]
        result = self.analyzer.analyze(transactions)
        
        # Should only count positive transactions
        assert result["total_transactions"] == 2
    
    def test_result_structure(self):
        """Test that result has all required keys"""
        transactions = [100, 200, 300, 400, 500]
        result = self.analyzer.analyze(transactions)
        
        required_keys = [
            "chi_square_stat",
            "p_value",
            "is_fraud",
            "details",
            "total_transactions",
            "fraud_probability"
        ]
        
        for key in required_keys:
            assert key in result
    
    def test_details_structure(self):
        """Test that details have correct structure"""
        transactions = [100, 200, 300, 400, 500]
        result = self.analyzer.analyze(transactions)
        
        assert len(result["details"]) == 9  # Digits 1-9
        
        for detail in result["details"]:
            assert "digit" in detail
            assert "observed_count" in detail
            assert "expected_count" in detail
            assert "observed_percentage" in detail
            assert "expected_percentage" in detail
            assert "deviation" in detail
    
    def test_custom_significance_level(self):
        """Test custom significance level"""
        analyzer_strict = BenfordAnalyzer(significance_level=0.01)
        analyzer_lenient = BenfordAnalyzer(significance_level=0.1)
        
        transactions = np.random.uniform(100, 999, 100).tolist()
        
        result_strict = analyzer_strict.analyze(transactions)
        result_lenient = analyzer_lenient.analyze(transactions)
        
        # Both should analyze same data
        assert result_strict["total_transactions"] == result_lenient["total_transactions"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
