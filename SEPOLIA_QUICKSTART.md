# ⚡ CHẠY TRÊN SEPOLIA TESTNET - 3 BƯỚC NHANH

## 🎯 Mục tiêu: Deploy lên Sepolia để demo thật với testnet

---

## Bước 1: Lấy Sepolia ETH (2 phút)

```
1. Vào: https://www.alchemy.com/faucets/ethereum-sepolia
2. Login với email
3. Nhập địa chỉ MetaMask
4. Nhận 0.5 SepoliaETH
```

---

## Bước 2: Setup .env (3 phút)

**Tạo file `contracts/.env`:**

```bash
# 1. Lấy RPC URL từ Alchemy
# Vào: https://www.alchemy.com/
# Create App → Ethereum Sepolia → Copy HTTPS URL

SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY

# 2. Lấy Private Key từ MetaMask
# MetaMask → Account Details → Export Private Key

PRIVATE_KEY=your_private_key_here

# 3. Etherscan API (optional - để verify)
ETHERSCAN_API_KEY=your_key
```

**Ví dụ:**
```env
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/abc123xyz
PRIVATE_KEY=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
ETHERSCAN_API_KEY=ABC123
```

---

## Bước 3: Deploy (2 phút)

### Option A: Dùng Script (Khuyến nghị)

```bash
deploy-sepolia.bat
```

Script sẽ tự động:
- Check balance
- Compile contracts
- Deploy lên Sepolia
- Save addresses

### Option B: Manual

```bash
cd contracts

# Check balance
npx hardhat run scripts/check-balance.js --network sepolia

# Compile
npx hardhat compile

# Deploy
npx hardhat run scripts/deploy-mock.js --network sepolia
```

---

## Bước 4: Update Frontend (1 phút)

**Copy addresses từ `contracts/deployed-addresses-mock.json`**

**Paste vào `frontend/config/constants.js`:**

```javascript
export const CONTRACTS = {
  streamCredit: '0xYourNewAddress',
  mockUSDC: '0xYourNewAddress',
  groth16Verifier: '0xYourNewAddress'
}
```

---

## Bước 5: Test! (2 phút)

```bash
# Start frontend
cd frontend
npm run dev
```

1. Mở http://localhost:3000
2. **Switch MetaMask sang Sepolia Testnet**
3. Connect Wallet
4. Launch App
5. Test scenarios

**Mỗi transaction sẽ có link Etherscan để verify!**

---

## ✅ Checklist

- [ ] Có >= 0.1 Sepolia ETH
- [ ] Đã tạo .env với RPC URL và Private Key
- [ ] Deploy thành công (xem addresses)
- [ ] Update frontend config
- [ ] MetaMask ở Sepolia network
- [ ] Frontend connect được

---

## 🔗 Quick Links

- Get ETH: https://www.alchemy.com/faucets/ethereum-sepolia
- Alchemy: https://www.alchemy.com/
- Explorer: https://sepolia.etherscan.io
- Check deployed contracts: `contracts/deployed-addresses-mock.json`

---

## 🐛 Nếu gặp lỗi:

**"Cannot connect"**
→ Check .env file, RPC URL đúng chưa

**"Insufficient funds"**
→ Lấy thêm ETH từ faucet

**"Nonce too high"**
→ MetaMask Settings → Advanced → Reset Account

---

**Chi tiết đầy đủ: Xem `DEPLOY_SEPOLIA.md`**

**Tổng thời gian: ~10 phút**

**Sau khi xong, bạn sẽ có app chạy trên testnet thật! 🚀**
