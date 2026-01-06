# 🚀 StreamCredit - Quick Setup Guide

## Phương án 1: Setup Tự động (Khuyến nghị) ⚡

### Chạy script tự động:

```bash
setup-complete.bat
```

Script này sẽ:
- ✅ Install tất cả dependencies
- ✅ Compile smart contracts
- ✅ Deploy lên Hardhat local network
- ✅ Start tất cả services (Hardhat, Mock API, Frontend)
- ✅ Tự động mở browser

---

## Phương án 2: Setup Thủ công (Chi tiết) 🔧

### Bước 1: Install Dependencies

```bash
# Contracts
cd contracts
npm install

# Mock API
cd ../mock-api
npm install

# Frontend
cd ../frontend
npm install
```

### Bước 2: Compile & Deploy Contracts

#### Option A: Deploy Local (Testing)

**Terminal 1** - Start Hardhat Network:
```bash
cd contracts
npx hardhat node
```

Lưu lại private key của Account #0 (sẽ dùng để import vào MetaMask)

**Terminal 2** - Deploy:
```bash
cd contracts
npx hardhat run scripts/deploy-local.js --network localhost
```

Hoặc dùng script:
```bash
deploy-contracts.bat
# Chọn option 1
```

#### Option B: Deploy Sepolia (Production-like)

1. **Setup .env file:**
```bash
cd contracts
copy .env.example .env
# Edit .env và điền:
# - SEPOLIA_RPC_URL (từ Alchemy/Infura)
# - PRIVATE_KEY (từ MetaMask)
# - ETHERSCAN_API_KEY
```

2. **Get Sepolia ETH:**
- Faucet: https://sepoliafaucet.com
- Cloud Faucet: https://www.alchemy.com/faucets/ethereum-sepolia

3. **Deploy:**
```bash
npx hardhat run scripts/deploy-mock.js --network sepolia
```

### Bước 3: Cấu hình Frontend

Contract addresses được tự động update vào `frontend/config/constants.js`

Nếu cần update thủ công:

```javascript
// frontend/config/constants.js
export const CONTRACTS = {
  streamCredit: '0xYourStreamCreditAddress',
  mockUSDC: '0xYourMockUSDCAddress',
  groth16Verifier: '0xYourVerifierAddress'
}
```

### Bước 4: Start Services

**Terminal 3** - Mock API:
```bash
cd mock-api
npm start
# Running on http://localhost:3001
```

**Terminal 4** - Frontend:
```bash
cd frontend
npm run dev
# Running on http://localhost:3000
```

---

## 🦊 Cấu hình MetaMask

### Cho Local Network (Hardhat):

1. Mở MetaMask
2. Network dropdown → "Add Network" → "Add network manually"
3. Điền thông tin:
   - **Network Name:** Hardhat Local
   - **RPC URL:** http://localhost:8545
   - **Chain ID:** 31337
   - **Currency Symbol:** ETH
4. Save

5. Import Test Account:
   - Copy private key từ Hardhat node terminal (Account #0)
   - MetaMask → Account Menu → Import Account
   - Paste private key

### Cho Sepolia Network:

1. MetaMask đã có sẵn Sepolia
2. Chuyển sang Sepolia network
3. Đảm bảo có Sepolia ETH (dùng faucet nếu cần)

---

## ✅ Verification Checklist

- [ ] Node.js >= 18.0 installed
- [ ] All dependencies installed (npm install)
- [ ] Contracts compiled successfully
- [ ] Contracts deployed (check addresses in JSON files)
- [ ] Frontend config updated with contract addresses
- [ ] Mock API running (http://localhost:3001/health returns OK)
- [ ] Frontend running (http://localhost:3000)
- [ ] MetaMask connected to correct network
- [ ] MetaMask has test ETH

---

## 🎮 Test Flow

1. **Open Frontend:** http://localhost:3000
2. **Connect Wallet:** Click "Connect Wallet" → MetaMask
3. **Launch App:** Click "Launch App" or "Mở Demo App"
4. **Select Scenario:** Choose "Honest Merchant"
5. **Verify:** Watch console logs and see data analysis
6. **Generate Proof:** Click "Generate ZK Proof"
7. **Submit:** Click "Submit On-Chain" (requires MetaMask confirmation)
8. **Check Credit:** See credit limit updated
9. **Borrow:** Click "Borrow" to test borrowing

---

## 🐛 Troubleshooting

### Contracts không compile được:

```bash
cd contracts
rm -rf cache artifacts
npx hardhat clean
npx hardhat compile
```

### MetaMask không connect được:

- Check network (Hardhat Local hoặc Sepolia)
- Reset account: MetaMask Settings → Advanced → Reset Account
- Clear browser cache

### Frontend không load được:

```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### Transaction bị reject:

- Check có đủ ETH cho gas fee
- Check contract addresses đúng
- Verify network đúng (chainId)

### Mock API lỗi:

```bash
cd mock-api
npm start
# Check terminal cho error details
```

### Hardhat node crash:

```bash
# Restart node
cd contracts
npx hardhat node

# Redeploy
npx hardhat run scripts/deploy-local.js --network localhost
```

---

## 📝 Useful Commands

### Hardhat:

```bash
# Compile
npx hardhat compile

# Test
npx hardhat test

# Clean
npx hardhat clean

# Start node
npx hardhat node

# Deploy local
npx hardhat run scripts/deploy-local.js --network localhost

# Deploy Sepolia
npx hardhat run scripts/deploy-mock.js --network sepolia

# Verify on Etherscan
npx hardhat verify --network sepolia CONTRACT_ADDRESS
```

### Frontend:

```bash
# Dev server
npm run dev

# Build
npm run build

# Start production
npm start

# Lint
npm run lint
```

### Mock API:

```bash
# Start server
npm start

# Test endpoints
curl http://localhost:3001/health
curl http://localhost:3001/api/user/honest
```

---

## 📚 Important Files

- `contracts/deployed-addresses-local.json` - Local deployment addresses
- `contracts/deployed-addresses-mock.json` - Sepolia deployment addresses
- `frontend/config/constants.js` - Frontend contract configuration
- `contracts/.env` - Contract deployment secrets (KHÔNG COMMIT!)

---

## 🌐 URLs

- **Frontend:** http://localhost:3000
- **Mock API:** http://localhost:3001
- **Hardhat Node:** http://localhost:8545
- **Sepolia Explorer:** https://sepolia.etherscan.io

---

## 🎯 Next Steps

1. ✅ Complete setup
2. 🧪 Test locally with Hardhat
3. 🚀 Deploy to Sepolia
4. 🔒 Generate real ZK circuit (not mock)
5. 🌍 Deploy frontend to Vercel
6. 📱 Test with real users

---

**Need help? Check:**
- README.md - Project overview
- COMPLETE_GUIDE.md - Detailed usage guide
- contracts/README.md - Smart contract docs

**Happy Hacking! 🚀**
