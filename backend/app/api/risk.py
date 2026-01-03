"""
Risk Analysis API endpoints
Provides fraud detection and credit risk assessment services
"""
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.risk_engine import BenfordAnalyzer


router = APIRouter(prefix="/risk", tags=["Risk Analysis"])


class TransactionAnalysisRequest(BaseModel):
    """Request model for transaction analysis"""
    transactions: List[float] = Field(
        ...,
        description="List of transaction amounts to analyze",
        min_items=1,
        example=[123.45, 234.56, 345.67, 456.78, 567.89]
    )
    significance_level: float = Field(
        default=0.05,
        description="Significance level for fraud detection (default: 0.05)",
        ge=0.001,
        le=0.1
    )


class TransactionAnalysisResponse(BaseModel):
    """Response model for transaction analysis"""
    chi_square_stat: float
    p_value: float
    is_fraud: bool
    details: List[dict]
    total_transactions: int
    fraud_probability: float
    interpretation: str


@router.post("/analyze-transactions", response_model=TransactionAnalysisResponse)
async def analyze_transactions(request: TransactionAnalysisRequest):
    """
    Analyze transactions using Benford's Law to detect potential fraud.
    
    Benford's Law states that in many naturally occurring datasets,
    the first digit follows a specific probability distribution.
    Deviations from this distribution may indicate fraudulent activity.
    
    **Algorithm:**
    1. Extract first significant digit from each transaction
    2. Compare observed vs. expected frequency (Benford distribution)
    3. Perform chi-square statistical test
    4. Flag as fraud if p-value < significance level
    
    **Returns:**
    - Statistical analysis results
    - Fraud probability score
    - Detailed digit-by-digit comparison
    """
    try:
        analyzer = BenfordAnalyzer(significance_level=request.significance_level)
        result = analyzer.analyze(request.transactions)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/benford-expected")
async def get_benford_expected():
    """
    Get the expected frequency distribution according to Benford's Law.
    
    Returns the theoretical probability for each first digit (1-9).
    Useful for understanding the baseline for fraud detection.
    """
    return {
        "law": "Benford's Law",
        "formula": "P(d) = log₁₀(1 + 1/d)",
        "expected_frequencies": {
            str(digit): {
                "probability": round(BenfordAnalyzer.BENFORD_EXPECTED[digit], 4),
                "percentage": round(BenfordAnalyzer.BENFORD_EXPECTED[digit] * 100, 2)
            }
            for digit in range(1, 10)
        }
    }


@router.post("/quick-fraud-check")
async def quick_fraud_check(transactions: List[float]):
    """
    Quick fraud check endpoint (simplified response).
    
    Returns only the essential fraud detection result without detailed statistics.
    """
    analyzer = BenfordAnalyzer()
    result = analyzer.analyze(transactions)
    
    return {
        "is_fraud": result.get("is_fraud", False),
        "confidence": result.get("fraud_probability", 0.0),
        "interpretation": result.get("interpretation", "Unknown"),
        "total_analyzed": result.get("total_transactions", 0)
    }
