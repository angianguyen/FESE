// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

// Import Verifier contract (sẽ được generate từ ZK circuit)
interface IVerifier {
    function verifyProof(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[1] memory input
    ) external view returns (bool);
}

/**
 * @title StreamCredit
 * @notice Lending protocol dựa trên dòng tiền thời gian thực với ZK fraud detection
 */
contract StreamCredit is Ownable, ReentrancyGuard {
    IVerifier public verifier;
    IERC20 public usdcToken;
    
    // Credit limit cho mỗi borrower
    mapping(address => uint256) public creditLimit;
    
    // Số tiền đã vay
    mapping(address => uint256) public borrowed;
    
    // Lãi suất (basis points - 1000 = 10%)
    uint256 public interestRate = 1200; // 12%
    
    // Tỷ lệ credit limit trên revenue (30%)
    uint256 public constant CREDIT_RATIO = 30;
    uint256 public constant BASIS_POINTS = 10000;
    
    // Liquidity pool
    uint256 public totalLiquidity;
    mapping(address => uint256) public liquidityProvided;
    
    // Events
    event CreditVerified(address indexed borrower, uint256 creditLimit, uint256 timestamp);
    event Borrowed(address indexed borrower, uint256 amount);
    event Repaid(address indexed borrower, uint256 amount);
    event LiquidityAdded(address indexed provider, uint256 amount);
    event LiquidityRemoved(address indexed provider, uint256 amount);
    
    constructor(address _verifier, address _usdcToken) Ownable(msg.sender) {
        verifier = IVerifier(_verifier);
        usdcToken = IERC20(_usdcToken);
    }
    
    /**
     * @notice Verify ZK proof và cập nhật credit limit
     * @param a, b, c: ZK proof components
     * @param input: Public inputs (isValid output)
     * @param revenue: Doanh thu (để tính credit limit nếu proof valid)
     */
    function verifyAndUpdateCredit(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[1] memory input,
        uint256 revenue
    ) external {
        // Verify ZK proof
        require(verifier.verifyProof(a, b, c, input), "Invalid ZK proof");
        
        // Check if proof is valid (input[0] should be 1)
        require(input[0] == 1, "Proof validation failed");
        
        // Calculate credit limit = 30% of revenue
        uint256 newCreditLimit = (revenue * CREDIT_RATIO) / 100;
        
        // Update credit limit
        creditLimit[msg.sender] = newCreditLimit;
        
        emit CreditVerified(msg.sender, newCreditLimit, block.timestamp);
    }
    
    /**
     * @notice Vay tiền
     * @param amount: Số tiền muốn vay
     */
    function borrow(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        require(creditLimit[msg.sender] > 0, "No credit limit");
        require(
            borrowed[msg.sender] + amount <= creditLimit[msg.sender],
            "Exceeds credit limit"
        );
        require(amount <= totalLiquidity, "Insufficient liquidity");
        
        borrowed[msg.sender] += amount;
        totalLiquidity -= amount;
        
        require(usdcToken.transfer(msg.sender, amount), "Transfer failed");
        
        emit Borrowed(msg.sender, amount);
    }
    
    /**
     * @notice Trả nợ
     * @param amount: Số tiền trả
     */
    function repay(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        require(borrowed[msg.sender] >= amount, "Repay exceeds debt");
        
        require(
            usdcToken.transferFrom(msg.sender, address(this), amount),
            "Transfer failed"
        );
        
        borrowed[msg.sender] -= amount;
        totalLiquidity += amount;
        
        emit Repaid(msg.sender, amount);
    }
    
    /**
     * @notice Thêm thanh khoản (liquidity provider)
     * @param amount: Số USDC cung cấp
     */
    function addLiquidity(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        
        require(
            usdcToken.transferFrom(msg.sender, address(this), amount),
            "Transfer failed"
        );
        
        liquidityProvided[msg.sender] += amount;
        totalLiquidity += amount;
        
        emit LiquidityAdded(msg.sender, amount);
    }
    
    /**
     * @notice Rút thanh khoản
     * @param amount: Số tiền muốn rút
     */
    function removeLiquidity(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        require(liquidityProvided[msg.sender] >= amount, "Insufficient balance");
        require(amount <= totalLiquidity, "Insufficient protocol liquidity");
        
        liquidityProvided[msg.sender] -= amount;
        totalLiquidity -= amount;
        
        require(usdcToken.transfer(msg.sender, amount), "Transfer failed");
        
        emit LiquidityRemoved(msg.sender, amount);
    }
    
    /**
     * @notice Lấy thông tin tài khoản
     */
    function getAccountInfo(address account) 
        external 
        view 
        returns (
            uint256 _creditLimit,
            uint256 _borrowed,
            uint256 _available
        ) 
    {
        _creditLimit = creditLimit[account];
        _borrowed = borrowed[account];
        _available = _creditLimit > _borrowed ? _creditLimit - _borrowed : 0;
    }
    
    /**
     * @notice Update verifier contract (owner only)
     */
    function updateVerifier(address _verifier) external onlyOwner {
        verifier = IVerifier(_verifier);
    }
    
    /**
     * @notice Update interest rate (owner only)
     */
    function updateInterestRate(uint256 _interestRate) external onlyOwner {
        require(_interestRate <= 5000, "Rate too high"); // Max 50%
        interestRate = _interestRate;
    }
}
