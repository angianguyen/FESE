@echo off
echo ========================================
echo Deploy to Sepolia Testnet
echo ========================================
echo.

cd contracts

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file with:
    echo - SEPOLIA_RPC_URL
    echo - PRIVATE_KEY
    echo - ETHERSCAN_API_KEY
    echo.
    echo See DEPLOY_SEPOLIA.md for detailed instructions
    pause
    exit /b 1
)

echo Step 1: Checking account balance...
call npx hardhat run scripts/check-balance.js --network sepolia

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Cannot connect to Sepolia
    echo Check your .env file configuration
    pause
    exit /b 1
)

echo.
echo Step 2: Compiling contracts...
call npx hardhat compile

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Ready to Deploy!
echo ========================================
echo.
echo This will deploy:
echo - MockUSDC
echo - MockVerifier (Testing only)
echo - StreamCredit
echo.
echo Estimated cost: ~0.005 ETH (on Sepolia)
echo.
pause

echo.
echo Step 3: Deploying contracts...
call npx hardhat run scripts/deploy-mock.js --network sepolia

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Deployment failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Contract addresses saved to:
echo - deployed-addresses-mock.json
echo.
echo Next steps:
echo 1. Update frontend/config/constants.js with new addresses
echo 2. (Optional) Verify contracts on Etherscan
echo 3. Test on frontend with Sepolia network
echo.
echo View on Etherscan: https://sepolia.etherscan.io
echo.
pause

cd ..
