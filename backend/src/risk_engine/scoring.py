"""
Credit Scoring System and Mock Data Generator for FESE StreamCredit

This module provides:
1. Mock Shopify transaction data generator
2. Credit scoring logic based on revenue and transaction patterns
3. Integration with Benford's Law fraud detection
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass
import sys
from pathlib import Path

# Handle both direct execution and module import
try:
    from .benford import BenfordAnalyzer
except ImportError:
    # Add parent directory to path for direct execution
    backend_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(backend_dir))
    from src.risk_engine.benford import BenfordAnalyzer


@dataclass
class ScoringResult:
    """Data class for credit scoring results"""
    score: int
    decision: str  # "Approved" or "Rejected"
    credit_limit: float
    monthly_avg_revenue: float
    avg_order_value: float
    total_transactions: int
    fraud_check: Dict
    reasons: List[str]
    risk_level: str  # "Low", "Medium", "High"


def generate_mock_shopify_data(months: int = 12, is_healthy: bool = True) -> List[Dict]:
    """
    Generate mock Shopify transaction data for testing.
    
    Args:
        months: Number of months of data to generate (default: 12)
        is_healthy: If True, generate healthy business data with rising trend.
                   If False, generate suspicious/volatile data.
    
    Returns:
        List of transaction dictionaries with structure:
        {
            "date": "YYYY-MM-DD",
            "order_id": "ORD_xxxxx",
            "amount": float,
            "customer_id": "CUST_xxxxx",
            "product_count": int
        }
    
    Example:
        >>> data = generate_mock_shopify_data(months=6, is_healthy=True)
        >>> len(data)  # Should have ~900-1500 transactions
        1200
    """
    transactions = []
    start_date = datetime.now() - timedelta(days=30 * months)
    
    if is_healthy:
        # Healthy business: Log-normal distribution with rising trend
        for month in range(months):
            # Number of transactions per month (increasing trend)
            base_transactions = 100
            transaction_count = int(base_transactions + (month * 10) + np.random.normal(0, 20))
            transaction_count = max(50, transaction_count)  # At least 50 per month
            
            # Revenue growth trend
            growth_factor = 1 + (month * 0.05)  # 5% growth per month
            
            for _ in range(transaction_count):
                # Date within this month
                days_offset = month * 30 + np.random.randint(0, 30)
                transaction_date = start_date + timedelta(days=days_offset)
                
                # Amount follows log-normal distribution (natural for prices)
                # Adjusted parameters to follow Benford's Law better
                base_amount = np.random.lognormal(mean=4.5, sigma=1.2)  # Better Benford distribution
                amount = round(base_amount * growth_factor, 2)
                amount = max(10.0, amount)  # Minimum $10
                
                # Product count (1-5 items per order)
                product_count = int(np.random.lognormal(mean=0.5, sigma=0.5)) + 1
                product_count = min(product_count, 5)
                
                transactions.append({
                    "date": transaction_date.strftime("%Y-%m-%d"),
                    "order_id": f"ORD_{np.random.randint(10000, 99999)}",
                    "amount": round(amount, 2),
                    "customer_id": f"CUST_{np.random.randint(1000, 9999)}",
                    "product_count": product_count
                })
    
    else:
        # Suspicious business: Uniform distribution, volatile patterns
        for month in range(months):
            # Erratic transaction count
            transaction_count = int(np.random.uniform(20, 200))
            
            for _ in range(transaction_count):
                days_offset = month * 30 + np.random.randint(0, 30)
                transaction_date = start_date + timedelta(days=days_offset)
                
                # Uniform distribution (suspicious - not natural)
                amount = round(np.random.uniform(10, 500), 2)
                
                # Random product count
                product_count = np.random.randint(1, 10)
                
                transactions.append({
                    "date": transaction_date.strftime("%Y-%m-%d"),
                    "order_id": f"ORD_{np.random.randint(10000, 99999)}",
                    "amount": round(amount, 2),
                    "customer_id": f"CUST_{np.random.randint(1000, 9999)}",
                    "product_count": product_count
                })
    
    # Sort by date
    transactions.sort(key=lambda x: x["date"])
    
    return transactions


class CreditScorer:
    """
    Credit scoring engine for StreamCredit.
    
    Evaluates merchant creditworthiness based on:
    1. Revenue patterns (MAR - Monthly Average Revenue)
    2. Transaction health (AOV - Average Order Value)
    3. Fraud detection (Benford's Law)
    
    Scoring Rules:
    - MAR > $5,000 AND AOV > $30 → Score 750 (Approved)
    - Otherwise → Score 400 (Rejected)
    - Fraud detected → Score 0 (Auto-reject)
    """
    
    # Scoring thresholds
    MAR_THRESHOLD = 5000.0  # Monthly Average Revenue threshold
    AOV_THRESHOLD = 30.0    # Average Order Value threshold
    
    # Score values
    SCORE_APPROVED = 750
    SCORE_REJECTED = 400
    SCORE_FRAUD = 0
    
    # Credit limit settings
    CREDIT_MULTIPLIER = 2.0  # Credit limit = 2 * MAR
    MAX_CREDIT_LIMIT = 10000.0  # Cap at $10,000
    
    def __init__(self):
        """Initialize the credit scorer with fraud detection"""
        self.benford_analyzer = BenfordAnalyzer()
    
    def _calculate_mar(self, transactions: List[Dict]) -> float:
        """
        Calculate Monthly Average Revenue.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Monthly average revenue in dollars
        """
        if not transactions:
            return 0.0
        
        # Group by month and calculate revenue
        monthly_revenue = {}
        for txn in transactions:
            try:
                date = datetime.strptime(txn["date"], "%Y-%m-%d")
                month_key = date.strftime("%Y-%m")
                
                if month_key not in monthly_revenue:
                    monthly_revenue[month_key] = 0.0
                monthly_revenue[month_key] += float(txn["amount"])
            except (KeyError, ValueError) as e:
                # Skip invalid transactions
                continue
        
        # Calculate average
        if not monthly_revenue:
            return 0.0
        
        total_revenue = sum(monthly_revenue.values())
        months_count = len(monthly_revenue)
        
        return total_revenue / months_count if months_count > 0 else 0.0
    
    def _calculate_aov(self, transactions: List[Dict]) -> float:
        """
        Calculate Average Order Value.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Average order value in dollars
        """
        if not transactions:
            return 0.0
        
        total_amount = 0.0
        valid_count = 0
        
        for txn in transactions:
            try:
                amount = float(txn["amount"])
                total_amount += amount
                valid_count += 1
            except (KeyError, ValueError):
                continue
        
        return total_amount / valid_count if valid_count > 0 else 0.0
    
    def _run_fraud_check(self, transactions: List[Dict]) -> Dict:
        """
        Run Benford's Law fraud detection on transaction amounts.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Fraud detection results from BenfordAnalyzer
        """
        amounts = [txn["amount"] for txn in transactions if txn["amount"] > 0]
        return self.benford_analyzer.analyze(amounts)
    
    def _determine_credit_limit(self, mar: float, is_approved: bool) -> float:
        """
        Calculate credit limit based on MAR.
        
        Args:
            mar: Monthly Average Revenue
            is_approved: Whether the application is approved
            
        Returns:
            Credit limit in dollars
        """
        if not is_approved:
            return 0.0
        
        # Credit limit = 2 * MAR, capped at $10,000
        limit = mar * self.CREDIT_MULTIPLIER
        return min(limit, self.MAX_CREDIT_LIMIT)
    
    def _assess_risk_level(self, score: int, fraud_check: Dict) -> str:
        """
        Determine risk level based on score and fraud indicators.
        
        Args:
            score: Credit score
            fraud_check: Fraud detection results
            
        Returns:
            Risk level: "Low", "Medium", or "High"
        """
        if score == self.SCORE_FRAUD:
            return "High"
        
        if fraud_check.get("is_fraud", False):
            return "High"
        
        if score >= self.SCORE_APPROVED:
            return "Low"
        
        return "Medium"
    
    def calculate_score(self, transactions: List[Dict]) -> Dict:
        """
        Calculate credit score for a merchant based on transaction history.
        
        Args:
            transactions: List of transaction dictionaries from Shopify
            
        Returns:
            Dictionary with scoring results:
            {
                "score": int,
                "decision": str ("Approved" or "Rejected"),
                "credit_limit": float,
                "monthly_avg_revenue": float,
                "avg_order_value": float,
                "total_transactions": int,
                "fraud_check": dict,
                "reasons": list[str],
                "risk_level": str
            }
        
        Example:
            >>> scorer = CreditScorer()
            >>> data = generate_mock_shopify_data(months=12, is_healthy=True)
            >>> result = scorer.calculate_score(data)
            >>> print(f"Decision: {result['decision']}")
        """
        reasons = []
        
        # Validation
        if not transactions:
            return {
                "score": self.SCORE_REJECTED,
                "decision": "Rejected",
                "credit_limit": 0.0,
                "monthly_avg_revenue": 0.0,
                "avg_order_value": 0.0,
                "total_transactions": 0,
                "fraud_check": {},
                "reasons": ["No transaction data provided"],
                "risk_level": "High"
            }
        
        # Step 1: Calculate metrics FIRST (always calculate to show data)
        mar = self._calculate_mar(transactions)
        aov = self._calculate_aov(transactions)
        
        # Step 2: Run fraud detection
        fraud_check = self._run_fraud_check(transactions)
        
        if fraud_check.get("is_fraud", False):
            # Auto-reject if fraud detected
            fraud_flags = fraud_check.get("red_flags", {})
            fraud_reasons = []
            
            if fraud_flags.get("chi_square_violation"):
                fraud_reasons.append("Statistical anomaly detected in transaction distribution")
            if fraud_flags.get("digit_1_threshold_violation"):
                digit_1_pct = fraud_check.get("digit_1_analysis", {}).get("observed_percentage", 0)
                fraud_reasons.append(f"Digit-1 frequency suspicious ({digit_1_pct}% outside 25-35% range)")
            
            return {
                "score": self.SCORE_FRAUD,
                "decision": "Rejected",
                "credit_limit": 0.0,
                "monthly_avg_revenue": round(mar, 2),  # Show actual MAR
                "avg_order_value": round(aov, 2),      # Show actual AOV
                "total_transactions": len(transactions),
                "fraud_check": fraud_check,
                "reasons": ["🚨 FRAUD DETECTED"] + fraud_reasons,
                "risk_level": "High"
            }
        
        # Step 3: Apply scoring rules
        score = self.SCORE_REJECTED
        decision = "Rejected"
        
        if mar > self.MAR_THRESHOLD and aov > self.AOV_THRESHOLD:
            score = self.SCORE_APPROVED
            decision = "Approved"
            reasons.append(f"✅ Strong revenue: MAR ${mar:,.2f} > ${self.MAR_THRESHOLD:,.2f}")
            reasons.append(f"✅ Healthy AOV: ${aov:.2f} > ${self.AOV_THRESHOLD:.2f}")
        else:
            if mar <= self.MAR_THRESHOLD:
                reasons.append(f"❌ Insufficient revenue: MAR ${mar:,.2f} ≤ ${self.MAR_THRESHOLD:,.2f}")
            if aov <= self.AOV_THRESHOLD:
                reasons.append(f"❌ Low order value: AOV ${aov:.2f} ≤ ${self.AOV_THRESHOLD:.2f}")
        
        # Step 4: Calculate credit limit
        credit_limit = self._determine_credit_limit(mar, decision == "Approved")
        
        if decision == "Approved":
            reasons.append(f"💰 Credit limit: ${credit_limit:,.2f} (2x MAR, capped at $10K)")
        
        # Step 5: Assess risk level
        risk_level = self._assess_risk_level(score, fraud_check)
        
        return {
            "score": score,
            "decision": decision,
            "credit_limit": round(credit_limit, 2),
            "monthly_avg_revenue": round(mar, 2),
            "avg_order_value": round(aov, 2),
            "total_transactions": len(transactions),
            "fraud_check": fraud_check,
            "reasons": reasons,
            "risk_level": risk_level
        }


def main():
    """Test the credit scoring system with mock data"""
    print("\n" + "="*80)
    print("🏦 STREAMCREDIT - CREDIT SCORING SYSTEM TEST")
    print("="*80)
    
    scorer = CreditScorer()
    
    # Test Case 1: Healthy business (should be approved)
    print("\n📊 TEST CASE 1: Healthy Business")
    print("-" * 80)
    healthy_data = generate_mock_shopify_data(months=12, is_healthy=True)
    
    # Debug: Check sample data
    print(f"Sample transaction: {healthy_data[0]}")
    print(f"Total transactions generated: {len(healthy_data)}")
    
    result = scorer.calculate_score(healthy_data)
    
    print(f"Transactions Analyzed: {result['total_transactions']}")
    print(f"Monthly Avg Revenue: ${result['monthly_avg_revenue']:,.2f}")
    print(f"Avg Order Value: ${result['avg_order_value']:.2f}")
    print(f"\n🎯 CREDIT SCORE: {result['score']}")
    print(f"📋 Decision: {result['decision']}")
    print(f"💰 Credit Limit: ${result['credit_limit']:,.2f}")
    print(f"⚠️  Risk Level: {result['risk_level']}")
    print(f"\n📝 Reasons:")
    for reason in result['reasons']:
        print(f"   {reason}")
    
    fraud = result['fraud_check']
    print(f"\n🔍 Fraud Check:")
    print(f"   Fraud Detected: {'❌ YES' if fraud.get('is_fraud') else '✅ NO'}")
    print(f"   P-value: {fraud.get('p_value', 0):.4f}")
    print(f"   Digit-1: {fraud.get('digit_1_analysis', {}).get('observed_percentage', 0):.2f}%")
    
    # Test Case 2: Struggling business (should be rejected)
    print("\n\n📊 TEST CASE 2: Struggling Business (Low Revenue)")
    print("-" * 80)
    # Generate small amount of data to simulate low revenue
    struggling_data = generate_mock_shopify_data(months=3, is_healthy=True)
    struggling_data = struggling_data[:100]  # Limit to small dataset
    result2 = scorer.calculate_score(struggling_data)
    
    print(f"Transactions Analyzed: {result2['total_transactions']}")
    print(f"Monthly Avg Revenue: ${result2['monthly_avg_revenue']:,.2f}")
    print(f"Avg Order Value: ${result2['avg_order_value']:.2f}")
    print(f"\n🎯 CREDIT SCORE: {result2['score']}")
    print(f"📋 Decision: {result2['decision']}")
    print(f"💰 Credit Limit: ${result2['credit_limit']:,.2f}")
    print(f"⚠️  Risk Level: {result2['risk_level']}")
    print(f"\n📝 Reasons:")
    for reason in result2['reasons']:
        print(f"   {reason}")
    
    # Test Case 3: Suspicious business (fraud detected)
    print("\n\n📊 TEST CASE 3: Suspicious Business (Fraud Pattern)")
    print("-" * 80)
    suspicious_data = generate_mock_shopify_data(months=12, is_healthy=False)
    result3 = scorer.calculate_score(suspicious_data)
    
    print(f"Transactions Analyzed: {result3['total_transactions']}")
    print(f"Monthly Avg Revenue: ${result3['monthly_avg_revenue']:,.2f}")
    print(f"Avg Order Value: ${result3['avg_order_value']:.2f}")
    print(f"\n🎯 CREDIT SCORE: {result3['score']}")
    print(f"📋 Decision: {result3['decision']}")
    print(f"💰 Credit Limit: ${result3['credit_limit']:,.2f}")
    print(f"⚠️  Risk Level: {result3['risk_level']}")
    print(f"\n📝 Reasons:")
    for reason in result3['reasons']:
        print(f"   {reason}")
    
    fraud3 = result3['fraud_check']
    print(f"\n🔍 Fraud Check:")
    print(f"   Fraud Detected: {'❌ YES' if fraud3.get('is_fraud') else '✅ NO'}")
    if fraud3.get('is_fraud'):
        print(f"   Red Flags:")
        flags = fraud3.get('red_flags', {})
        print(f"      Chi-square violation: {'Yes' if flags.get('chi_square_violation') else 'No'}")
        print(f"      Digit-1 violation: {'Yes' if flags.get('digit_1_threshold_violation') else 'No'}")
    
    print("\n" + "="*80)
    print("✅ All test cases completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
