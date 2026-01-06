# 🌐 Deploy lên Sepolia Testnet - Hướng dẫn từng bước

## Bước 1: Lấy Sepolia ETH (Test token)

### Option 1: Alchemy Faucet (Khuyến nghị)
1. Truy cập: https://www.alchemy.com/faucets/ethereum-sepolia
2. Đăng nhập với email/wallet
3. Nhập địa chỉ MetaMask của bạn
4. Nhận 0.5 SepoliaETH

### Option 2: Cloud Faucet
1. https://cloud.google.com/application/web3/faucet/ethereum/sepolia
2. Login với Google account
3. Claim test ETH

### Option 3: Sepolia POW Faucet
1. https://sepolia-faucet.pk910.de/
2. Mining POW để lấy test ETH

---

## Bước 2: Setup RPC URL (Alchemy/Infura)

### Option A: Alchemy (Khuyến nghị)

1. Truy cập: https://www.alchemy.com/
2. Sign up/Login
3. Click "Create new app"
4. Chọn:
   - Chain: Ethereum
   - Network: Sepolia
   - Name: StreamCredit
5. Click "Create app"
6. Vào app → "View key" → Copy "HTTPS URL"
7. URL dạng: `https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY`

### Option B: Infura

1. Truy cập: https://infura.io/
2. Sign up/Login
3. Create new project
4. Chọn Ethereum → Sepolia
5. Copy HTTPS endpoint

---

## Bước 3: Lấy Private Key từ MetaMask

⚠️ **CẢNH BÁO BẢO MẬT:**
- Chỉ dùng wallet test, KHÔNG dùng wallet chứa tiền thật
- KHÔNG bao giờ share private key
- KHÔNG commit .env vào Git

### Cách lấy Private Key:

1. Mở MetaMask
2. Click vào account icon (góc phải)
3. Chọn "Account details"
4. Click "Show private key"
5. Nhập password MetaMask
6. Click "Confirm"
7. Copy private key (bắt đầu với 0x...)

---

## Bước 4: Tạo file .env

**Trong thư mục `contracts`, tạo file `.env`:**

```bash
cd E:\fese_main\contracts
```

**Tạo file `.env` với nội dung:**

```env
# Sepolia RPC URL (từ Alchemy/Infura)
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY

# Private Key (từ MetaMask - BỎ ĐI prefix 0x nếu có)
PRIVATE_KEY=your_64_character_private_key_here

# Etherscan API Key (optional - để verify contracts)
ETHERSCAN_API_KEY=your_etherscan_api_key
```

**Ví dụ thực tế:**
```env
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/abc123def456ghi789
PRIVATE_KEY=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
ETHERSCAN_API_KEY=ABC123XYZ789
```

---

## Bước 5: Verify Setup

**Kiểm tra balance:**

```bash
cd E:\fese_main\contracts
npx hardhat run scripts/check-balance.js --network sepolia
```

Nếu chưa có script, tạo `scripts/check-balance.js`:

```javascript
async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Balance:", hre.ethers.formatEther(balance), "ETH");
  
  if (parseFloat(hre.ethers.formatEther(balance)) < 0.1) {
    console.log("⚠️  Warning: Low balance! Get more from faucet");
  }
}

main();
```

---

## Bước 6: Deploy lên Sepolia

```bash
cd E:\fese_main\contracts

# Compile contracts
npx hardhat compile

# Deploy
npx hardhat run scripts/deploy-mock.js --network sepolia
```

**Output sẽ hiện:**
```
🚀 Deploying StreamCredit with MockVerifier...

📍 Deploying with account: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0
💰 Account balance: 0.5 ETH

1️⃣ Deploying MockUSDC...
✅ MockUSDC deployed to: 0x1234...5678

2️⃣ Deploying MockVerifier...
✅ MockVerifier deployed to: 0xabcd...efgh

3️⃣ Deploying StreamCredit...
✅ StreamCredit deployed to: 0x9876...4321

✅ Addresses saved to deployed-addresses-mock.json
```

---

## Bước 7: Verify Contracts trên Etherscan

### Lấy Etherscan API Key:

1. Truy cập: https://etherscan.io/
2. Sign up/Login
3. My Profile → API Keys
4. Create new API key
5. Copy key

### Verify:

```bash
# Verify MockUSDC
npx hardhat verify --network sepolia 0xYourMockUSDCAddress

# Verify MockVerifier
npx hardhat verify --network sepolia 0xYourMockVerifierAddress

# Verify StreamCredit
npx hardhat verify --network sepolia 0xYourStreamCreditAddress "0xVerifierAddress" "0xUSDCAddress"
```

---

## Bước 8: Update Frontend Config

**File: `frontend/config/constants.js`**

Thay thế addresses bằng addresses vừa deploy:

```javascript
export const CONTRACTS = {
  streamCredit: '0xYourNewStreamCreditAddress',
  mockUSDC: '0xYourNewMockUSDCAddress',
  groth16Verifier: '0xYourNewMockVerifierAddress'
}
```

**Hoặc tự động update:**

Script deploy đã tự động lưu vào `deployed-addresses-mock.json`. Copy addresses từ file đó.

---

## Bước 9: Cấu hình MetaMask

1. **Thêm Sepolia Network** (nếu chưa có):
   - Network Name: Sepolia Testnet
   - RPC URL: https://rpc.sepolia.org
   - Chain ID: 11155111
   - Currency: ETH
   - Block Explorer: https://sepolia.etherscan.io

2. **Switch sang Sepolia** trong MetaMask

3. **Đảm bảo có Sepolia ETH** trong account

---

## Bước 10: Test trên Frontend

```bash
cd E:\fese_main\frontend
npm run dev
```

1. Mở http://localhost:3000
2. Connect wallet (phải ở Sepolia network)
3. Click "Launch App"
4. Test các scenarios

**Verify on Etherscan:**
- Mỗi transaction sẽ có link đến Sepolia Etherscan
- Click để xem chi tiết transaction

---

## ✅ Checklist

- [ ] Có Sepolia ETH (>= 0.1 ETH)
- [ ] Đã tạo Alchemy/Infura app
- [ ] Đã lấy RPC URL
- [ ] Đã export Private Key
- [ ] Đã tạo file `.env` với đúng thông tin
- [ ] Contracts compile thành công
- [ ] Deploy thành công lên Sepolia
- [ ] Đã verify contracts (optional)
- [ ] Đã update frontend config
- [ ] MetaMask đang ở Sepolia network
- [ ] Frontend connect được với wallet

---

## 🐛 Troubleshooting

### "Insufficient funds for gas"
→ Lấy thêm Sepolia ETH từ faucet

### "Invalid API key"
→ Check lại SEPOLIA_RPC_URL trong .env

### "Network not found"
→ Check hardhat.config.js có network sepolia

### "Nonce too high"
→ Reset MetaMask account: Settings → Advanced → Reset Account

### Deploy bị stuck
→ Check gas price, có thể thêm `gasPrice` trong hardhat.config.js

---

## 📊 Chi phí ước tính (Sepolia - FREE)

- MockUSDC: ~0.001 ETH
- MockVerifier: ~0.0005 ETH  
- StreamCredit: ~0.003 ETH
- **Tổng: ~0.0045 ETH** (miễn phí trên testnet)

---

## 🔗 Links hữu ích

- Sepolia Faucet: https://www.alchemy.com/faucets/ethereum-sepolia
- Sepolia Explorer: https://sepolia.etherscan.io
- Alchemy: https://www.alchemy.com/
- Infura: https://infura.io/
- MetaMask: https://metamask.io/

---

**Sau khi hoàn thành, bạn sẽ có:**
- ✅ Contracts chạy trên Sepolia testnet thật
- ✅ Frontend connect với testnet
- ✅ Transaction có thể view trên Etherscan
- ✅ Demo hoàn chỉnh cho investor/judge

**Chúc may mắn! 🚀**
